mkdir /data
kubectl apply -f k8s/prereqs/storageclass.yaml 
kubectl apply -f k8s/prereqs/pv-minio.yaml 
chmod -R 777 /data