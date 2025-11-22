eval $(minikube docker-env)
docker build -t ingestor:latest ./cloud/ingestor
docker build -t save_data:latest ./cloud/pipelines/save_data
docker build -t clean_data:latest ./cloud/pipelines/clean_data

ssh -L 8001:localhost:8001 -L 8086:localhost:8086 -L 8080:localhost:8080 annam@192.168.1.127
