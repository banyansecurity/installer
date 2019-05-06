# Deploying netagent using daemonset on kubernetes (gke)

### Supported OS
Currently, the Banyan Netagent is supported on the following Linux distros when run with an officially released kernel:

- Amazon-Linux (2011.09 thru 2018.03) and Amazon-Linux-2
- CentOS 7.x
- Ubuntu 12.04, 14.04, 16.04, 18.04 (-generic, -virtual, -gcp, -azure, -aws kernels)

### Prerequisites

- `kubectl` installed and authenticated with the kubernetes cluster 

###Update Config
```
cp config.yaml.tpl config.yaml
```
Set these properties in config.yaml
 - shield_address
 - secure_bootstrap
 - one_time_key
 - visibility_only

###Create daemonset
```
$ kubectl create secret generic netagent-config \
  --from-file=./gpg_password \
  --from-file=./config.yaml
   
$ kubectl create -f netagent-daemonset.yaml 
```

Additional optional config
```
  --from-file=./cidrs.txt
  --from-file=./exceptions.txt
```

###Remove daemonset
```
$ kubectl delete -f netagent-daemonset.yaml 
$ kubectl delete secret netagent-config
```