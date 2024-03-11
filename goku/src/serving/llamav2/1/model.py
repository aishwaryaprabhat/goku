import app
import os
import json
import triton_python_backend_utils as pb_utils
import numpy as np
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM,TextIteratorStreamer, BitsAndBytesConfig
import huggingface_hub
from threading import Thread


# model_path = '/model_path/models--google--gemma-2b-it/snapshots/718cb189da9c5b2e55abe86f2eeffee9b4ae0dad/'
model_path = '/model_path/models--mistralai--Mistral-7B-Instruct-v0.2/snapshots/cf47bb3e18fe41a5351bc36eef76e9c900847c89/'

class TritonPythonModel:
    def initialize(self, args):
        # quant_conf = BitsAndBytesConfig(
        #     load_in_4bit=True,
        #     bnb_4bit_use_double_quant=True,
        #     bnb_4bit_quant_type="fp4",
        #     bnb_4bit_compute_dtype=torch.float16,
        # )
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path, 
                                                        #   quantization_config=quant_conf,
                                                          device_map='auto')


    def get_prompt(self, message: str, 
                   chat_history: list[tuple[str, str]],
                   system_prompt: str) -> str:
        texts = [f'\n{system_prompt}\n']
        # The first user input is _not_ stripped
        do_strip = False
        for user_input, response in chat_history:
            user_input = user_input.strip() if do_strip else user_input
            do_strip = True
            texts.append(f'{user_input} {response.strip()} ')
        message = message.strip() if do_strip else message
        texts.append(f'{message}')
        return ''.join(texts)

    def execute(self, requests):
        responses = []
        for request in requests:
            # Decode the Byte Tensor into Text 
            inputs = pb_utils.get_input_tensor_by_name(request, "prompt")
            
            inputs = inputs.as_numpy()
            # Call the Model pipeline 
            DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant. Keep short answers of no more than 2 sentences."""
            
            # prompts = [self.get_prompt(i[0].decode(), [], DEFAULT_SYSTEM_PROMPT) for i in inputs]
            prompts = [self.get_prompt(i.decode() if isinstance(i, bytes) else str(i), [], DEFAULT_SYSTEM_PROMPT) for i in inputs.flatten()]
            # self.tokenizer.pad_token = "[PAD]"
            # self.tokenizer.padding_side = "left"
            inputs = self.tokenizer(prompts, return_tensors='pt')


            streamer = TextIteratorStreamer(
                tokenizer=self.tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True
            )
            generate_kwargs = dict(
                    **inputs,
                    max_new_tokens=512,
                    streamer=streamer,
                    do_sample=False,
                    num_beams=1,
                    temperature=0.0,
                    top_k=30,
                    top_p=30,
                    repetition_penalty=1.0,
                    length_penalty=1.0,
                    no_repeat_ngram_size=5,
            )
            output_sequences = self.model.generate(**generate_kwargs)
            # output = self.tokenizer.batch_decode(output_sequences, skip_special_tokens=True)
            output = self.tokenizer.decode(output_sequences[0])
            print("my output: ", output)
            # Encode the text to byte tensor to send back
            inference_response = pb_utils.InferenceResponse(
            output_tensors=[
                pb_utils.Tensor(
                    "generated_text",
                    np.array([[o.encode() for o in output]]),
                    )
            ]
            )
            responses.append(inference_response)
        
        return responses

    def finalize(self, args):
        self.generator = None