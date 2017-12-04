#!/usr/bin/env bash
set -x

CURDIR=${PWD}
KEYDIR=${CURDIR}/etc/cfssl
DKEYDIR=/etc/cfssl 
genkey=$1
if [ "$genkey" = "true" ]; then
    sudo docker run --rm -v ${KEYDIR}:${DKEYDIR} cfssl/cfssl genkey -initca ${DKEYDIR}/root_csr.json | \
      sudo docker run --rm -i -v ${KEYDIR}:${DKEYDIR} -w ${DKEYDIR} --entrypoint cfssljson cfssl/cfssl -bare ca
fi

sudo docker run -d -v ${KEYDIR}:${DKEYDIR} --net=host --name cfssl cfssl/cfssl:1.2.0 serve -config=${DKEYDIR}/root_config.json -ca=${DKEYDIR}/ca.pem -ca-key=${DKEYDIR}/ca-key.pem
