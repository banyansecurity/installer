# Installer - Netagent - Kubernetes - Deploy using DaemonSet

### Supported OS

Currently, the Banyan Netagent is supported on the following Linux distros when run with an officially released kernel:

- Amazon-Linux (2011.09 thru 2018.03) and Amazon-Linux-2
- CentOS 7.x
- Ubuntu 12.04, 14.04, 16.04, 18.04 (-generic, -virtual, -gcp, -azure, -aws kernels)

---

### Prerequisites

* `kubectl` installed
* `kubectl` authenticated with your Kubernetes cluster 


### Step 1 - Create Config File

```
cp config.yaml.tpl config.yaml
```

Set these properties in the `config.yaml` file.
```
shield_address
secure_bootstrap
one_time_key
visibility_only
```

### Step 2 - Create DaemonSet

```
kubectl create secret generic netagent-config --from-file=./gpg_password --from-file=./config.yaml
   
kubectl create -f netagent-daemonset.yaml 
```

You may add additional (optional) config params via the `cidrs.txt` and `exceptions.txt` files
```
  --from-file=./cidrs.txt
  --from-file=./exceptions.txt
```

---

### Remove the Netagent DaemonSet

```
kubectl delete -f netagent-daemonset.yaml 

kubectl delete secret netagent-config
```