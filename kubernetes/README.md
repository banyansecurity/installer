# Install Banyan on a Kubernetes cluster

## Install instructions

Please see the Banyan Docs site for the latest documentation: https://docs.banyanops.com/docs/install/v05kube/

---

The `shield.yaml` and `netagent.yaml` files provided here can be used to automaically deploy the Banyant agents across your Kubernetes cluster.

## Debugging

1. Make sure your Kubernetes cluster can communicate with the Banyan Cloud controller

```
$> kubectl create -f busybox.yaml
pod "busybox" created

# exec into the container
$> kubectl exec -it busybox sh

# try ping from inside the busybox container
/ # ping net.banyanops.com
PING net.banyanops.com (137.135.42.62): 56 data bytes
^C
--- net.banyanops.com ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss
/ # wget net.banyanops.com
Connecting to net.banyanops.com (137.135.42.62:80)
Connecting to net.banyanops.com (137.135.42.62:443)
index.html           100% |***************************************************************************************|  7693   0:00:00 ETA
/ # 
```

If your Busybox pod is unable to communicate with the Banyan Cloud Controller, please ask your admin to enable egress.

2. Make sure the Banyan Shield can communicate with the Kubernetes API Server

```
$> kubectl get pods --selector=com.banyanops.agent=shield
/banyanshield # 
```