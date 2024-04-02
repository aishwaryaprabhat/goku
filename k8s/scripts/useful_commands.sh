kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
kubectl -n argowf exec -it $(kubectl get pods -n argowf | grep argo-workflows-server | awk '{print $1}') -- argo auth token

# Kill prior services running on the ports
for port in 8080 9001 9000 5000 2746 8081 8082; do
  fuser -k $port/tcp
done

kubectl -n argocd port-forward svc/argocd-server 8080:80 &
kubectl -n minio port-forward svc/minio-console 9001 &
kubectl -n minio port-forward svc/minio 9000 &
kubectl -n mlflow port-forward svc/mlflow 5000 &
kubectl -n argowf port-forward svc/argowf-argo-workflows-server 2746 &
kubectl -n postgresql port-forward svc/postgres-postgresql 5432 &
kubectl -n kuberay port-forward svc/kuberay-apiserver-service 8082:8888 &

# psql -h localhost -p 5432 -U postgresw
# kubectl -n <ns> delete <resource> --all --grace-period=0 --force
# fuser -k 5000/tcp && kubectl -n mlflow port-forward svc/mlflow 5000 &
curl https://localhost:2746/api/v1/workflows/argo -H "Authorization: $ARGO_TOKEN"
# 200 OK
