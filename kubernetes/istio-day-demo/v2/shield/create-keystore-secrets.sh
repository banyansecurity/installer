#/usr/bin/env bash

kubectl create secret generic keystore-secrets --from-file=./ca.pem --from-file=./root_config.json --from-file=./ca-key.pem
