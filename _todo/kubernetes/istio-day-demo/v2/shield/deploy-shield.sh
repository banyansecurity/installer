#!/usr/bin/env bash
set -x

# Sanity check for input
if [ "$#" -lt 1 ]; then
 	echo "Usage: deploy-shield.sh <ORG_ID> <CM> <CLUSTER_NAME> <BANYAN_URL> <TLSNOVERIFY> <GROUPTYPE>"
	exit 1
fi


# Registry & version info
export pubregistry=pub.banyanops.com
export version=0.4.2

# Input parameters
orgid=$1
cm=$2
cname=$3
banyanurl=$4
tlsnoverify=$5
grouptype=$6

SUDO=sudo
# Pull from registry and start shield
echo "Starting shield"
$SUDO docker pull ${pubregistry}/shield:${version}
PORTS="-p 1200:1200"
$SUDO docker ${DOCKERCFG} run -d ${PORTS} --name shield \
        --net=host \
        --label com.banyanops.app="banyan-platform" \
        --log-opt max-size=1g --log-opt max-file=5 \
	-v /var/run/docker.sock:/var/run/docker.sock \
	-v $HOME/.banyan:/banyandir \
	-e BANYAN_HOST_DIR=/root/.banyan \
	-e ORG_ID=${orgid} \
	${pubregistry}/shield:${version} \
	--banyanURL=${banyanurl} \
        --banyanTLSNoVerify=${tlsnoverify} \
	--clustermanager=${cm} \
	--clustername=${cname} \
	--groupType=${grouptype} \
        --cloglevel=ERR \
	--floglevel=INFO   #log levels are ERR, WARN, INFO, DEBUG

if [ "$?" != 0 ]; then
	echo "NOTE: If you are using an older version of docker, please remove the log-opt options from the docker run command in deploy-shield.sh; run ./stop-deploy-ca.sh and ./start-deploy-ca.sh again"
	exit 1
fi

sleep 5
exit 0
