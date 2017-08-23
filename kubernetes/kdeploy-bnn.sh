#!/usr/bin/env bash
set -x

kubectl create -f banyan/shield/shield-ca.yaml
cat gobany@n > banyan/netagent/gpg_password
cat '10.0.0.0/16' > banyan/netagent/cidrs.txt
cat '10.244.0.0/16' >> banyan/netagent/cidrs.txt
cat '10.0.0.1' >> banyan/netagent/exceptions.txt
kubectl create secret generic bnn-secrets --from-file=./banyan/netagent/gpg_password --from-file=./banyan/netagent/cidrs.txt --from-file=./banyan/netagent/exceptions.txt
kubectl create -f banyan/netagent/netagent-daemonset.yaml

