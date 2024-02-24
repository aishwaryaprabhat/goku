mkdir /data
chmod -R 777 /data


kubectl apply -f k8s/storageclass.yaml 
kubectl apply -f k8s/pv-15gi.yaml 