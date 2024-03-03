mkdir /data
kubectl apply -f k8s/storageclass.yaml 
kubectl apply -f k8s/pv-minio.yaml 
chmod -R 777 /data