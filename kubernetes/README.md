# Install Banyan on a Kubernetes cluster

## Install instructions

Please see the Banyan Docs site for the latest documentation: https://docs.banyanops.com/docs/install/

The `shield.yaml` and `netagent.yaml` files provided here can be used to automaically deploy the Banyant agents across your Kubernetes cluster.

---

## Debugging

#### 1. Can a pod in your Kubernetes cluster can communicate with the Banyan Cloud controller

```shell
#
# we'll create a busybox container and exec into it
# using ping to check DNS resolution and wget to check reachability
#

$> kubectl create -f busybox.yaml
pod "busybox" created

$> kubectl exec -it busybox sh

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


#### 2. Can a pod in your Kubernetes cluster can communicate with the Kubernetes API Server

```shell
#
# we'll create a busybox container and exec into it
# using ping to check DNS resolution and wget to check reachability
#

$> kubectl create -f busybox.yaml
pod "busybox" created

$> kubectl exec -it busybox sh

/ # ping kubernetes
PING kubernetes (10.233.0.1): 56 data bytes
^C
--- kubernetes ping statistics ---
2 packets transmitted, 0 packets received, 100% packet loss

/ # wget https://kubernetes:443
Connecting to kubernetes:443 (10.233.0.1:443)
wget: TLS error from peer (alert code 40): handshake failure
wget: error getting response: Connection reset by peer
```

If your Busybox pod is unable to reach the Kubernetes API server, there might be an issue with your cluster setup.


#### 3. Make sure the Banyan Shield can communicate with the Kubernetes API Server

```shell
#
# check Shield logs for any EROR messages
#

$ kubectl get pods --selector=com.banyanops.agent=shield
NAME                                READY     STATUS    RESTARTS   AGE
banyan-shield-ca-3481444276-6ct7x   2/2       Running   0          22m

$ kubectl logs banyan-shield-ca-3481444276-6ct7x -c shield
Initializing Shield (ver: 0.5.0)...
[19:54:16 2017/09/19 +0000] [EROR] (kubemgr.readInClusterKubeConfig:456) dial tcp 10.0.0.1:443: i/o timeout : Kube api server: %s is not reachable from within cluster using cluster ip 10.0.0.1
```

If you see EROR messages as above, there might be an issue communicating with the Kubernetes API server