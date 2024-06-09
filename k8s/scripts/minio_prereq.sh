mkdir /data
chmod -R 777 /data
kubectl apply -f k8s/prereqs/storageclass.yaml 
kubectl apply -f k8s/prereqs/pv-minio.yaml 