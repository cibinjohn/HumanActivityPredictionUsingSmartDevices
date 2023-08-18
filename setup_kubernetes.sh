#!/bin/bash
kubectl apply -f flaskapi-secrets.yml 
kubectl apply -f mysql-pv.yml 
kubectl apply -f mysql-deployment.yml
kubectl apply -f flaskapp-deployment.yml 
kubectl apply -f frontend-deployment.yml
watch kubectl get po

