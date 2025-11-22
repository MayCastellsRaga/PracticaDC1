#!/bin/bash

# Script per desplegar tota l'aplicació a Kubernetes amb Minikube
# Ús: bash deploy.sh

set -e


# 1. Verificar que Minikube està instal·lat
if ! command -v minikube &> /dev/null; then
    echo "Minikube no trobat. Instal·la'l primer:"
    echo "curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
    echo "sudo install minikube-linux-amd64 /usr/local/bin/minikube"
    exit 1
fi

echo "Minikube trobat"

# 2. Verificar que Minikube està en marxa
if ! minikube status &> /dev/null; then
    echo "Iniciant Minikube..."
    minikube start --driver=docker
else
echo "Minikube ja està en marxa"
fi

# 3. Habilitar Ingress addon
echo "Habilitant Ingress NGINX..."
minikube addons enable ingress

# 4. Configurar Docker per usar el daemon de Minikube
echo "Configurant Docker per usar Minikube..."
eval $(minikube docker-env)

# 4. Construir imatges Docker dins de Minikube
echo "Construint imatges Docker dins de Minikube..."
cd ..
docker build -t ingestor:latest ./ingestor
docker build -t save_data:latest ./pipelines/save_data
docker build -t clean_data:latest ./pipelines/clean_data
docker build -t actuate:latest ./pipelines/actuate
docker build -t aggregate:latest ./pipelines/aggregate

echo "Imatges construïdes"

# 5. Desplegar serveis en l'ordre correcte
echo "Desplegant serveis d'infraestructura..."
cd k8s
kubectl apply -f influxdb.yml
kubectl apply -f zookeeper.yml
kubectl apply -f kafka.yml
kubectl apply -f mosquitto-cloud.yml

echo "Esperant que els serveis d'infraestructura estiguin llestos..."
sleep 15

# 6. Desplegar pipelines
echo "Desplegant pipelines..."
kubectl apply -f ingestor.yml
kubectl apply -f save-data.yml
kubectl apply -f clean-data.yml
kubectl apply -f actuate.yml
kubectl apply -f aggregate.yml

# 7. Desplegar Ingress
echo "Desplegant Ingress..."
kubectl apply -f ingress.yml

# 8. Desplegar Kafka UI
echo "Desplegant Kafka UI..."
kubectl apply -f kafka-ui.yml

# 9. Mostrar estat
echo ""
echo "Desplegament completat!"
echo ""
echo "Estat dels pods:"
kubectl get pods

echo ""
echo "Estat dels serveis:"
kubectl get services

echo ""
echo "Ingress:"
kubectl get ingress

echo " K8s Dashboard: http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/"
echo " InfluxDB:      http://localhost:8086 (user: mayandanna / pass: 12341234)"
echo " Kafka UI:      http://localhost:8080"