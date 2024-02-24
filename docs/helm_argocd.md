curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod +x get_helm.sh
./get_helm.sh

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

if kubectl > /dev/null 2>&1; then
  source <(kubectl completion bash)
fi
source ~/.bashrc

sudo apt-get install postgresql-client
psql --version

