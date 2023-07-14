#!/bin/bash

# Defina as variáveis ​​de ambiente
DOCKER_USERNAME=w3ll1n9t0n  # Nome de usuário do Docker Hub
DOCKER_IMAGE_TAG=w3ll1n9t0n/votacao-app  # Tag da imagem Docker

# Build da imagem Docker
docker build -t $DOCKER_IMAGE_TAG .  # Constrói a imagem Docker usando a tag definida

# Push da imagem Docker para o Docker Hub
docker push $DOCKER_IMAGE_TAG  # Faz o push da imagem para o Docker Hub

kubectl apply -f deployment.yaml  # Aplica o arquivo de configuração do Kubernetes (deployment.yaml)

kubectl delete pods -l app=my-app  # Deleta os pods com o rótulo "app=my-app"

watch -n 1 kubectl get pods  # Observa os pods atualizados a cada 1 segundo
