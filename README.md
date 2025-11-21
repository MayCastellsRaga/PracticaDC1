eval $(minikube docker-env)
docker build -t ingestor:latest ./cloud/ingestor
docker build -t save_data:latest ./cloud/pipelines/save_data
docker build -t clean_data:latest ./cloud/pipelines/clean_data