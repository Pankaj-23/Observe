#!/bin/bash

echo "Building Docker Image..."
docker build -t observability-app ../docker

echo "Pushing Image to ECR..."
docker tag observability-app:latest 754317098062.dkr.ecr.ap-south-1.amazonaws.com/observability-app:latest
docker push 754317098062.dkr.ecr.ap-south-1.amazonaws.com/observability-app:latest

echo "Deploying to Kubernetes..."
kubectl apply -f ../kubernetes/

echo "Deploying Monitoring Stack..."
kubectl apply -f ../monitoring/

echo "Deployment Completed!"