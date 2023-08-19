#!/bin/bash
kubectl delete all,pv,pvc,service,configmap,secret --all
watch kubectl get po
