kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d && echo
kubectl -n argowf exec -it $(kubectl get pods -n argowf | grep argo-workflows-server | awk '{print $1}') -- argo auth token

# Kill prior services running on the ports
for port in 9090 8080 9093 8501 5000 2746; do
  fuser -k $port/tcp
done

kubectl -n argocd port-forward svc/argocd-server 8080:80 &
kubectl -n minio port-forward svc/minio-console 9001 &
kubectl -n minio port-forward svc/minio 9000 &
kubectl -n mlflow port-forward svc/mlflow 5000 &
kubectl -n postgresql port-forward svc/postgres-postgresql 5432 &
kubectl -n argowf port-forward svc/argowf-argo-workflows-server 2746 &

# psql -h localhost -p 5432 -U postgresw
# kubectl -n mlflow delete pods --all --grace-period=0 --force
# fuser -k 5000/tcp && kubectl -n mlflow port-forward svc/mlflow 5000 &
