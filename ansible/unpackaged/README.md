# Deploy using tarball package

This deployment method may be desirable for very large clusters, environments where bandwidth is limited or where target 
hosts do not have access to download packages from a public repository.

The ansible playbook `netagent_deploy.yml` downloads a tarball to the local command host and then uses that to deploy netagent to all hosts 
listed in the inventory. 

###Pre-requisites (command host)
* Ansible 2.7
* Curl 


### Configuration
Specify cluster configuration using inventory variables as shown below. Your refresh token is available in the banyan console

Example inventory `my_inventory`:
```
[all:vars]
package_name=netagent-0.7.1.tar.gz
cluster_name=cluster1
refresh_token=<refresh token>

[group1]
myhost.example.com
```

Deploy:
```
ansible-playbook -i my_inventory netagent_deploy.yml
```

### Vagrant *(localhost trial option)*
A quick option to try netagent deployment on your local machine is to use Vagrant and a VM provider such as VirtualBox.
The commands below will bring up a VM and deploy netagent. 
* Make sure you update the `refresh_token` variable in `vagrant_inventory` first.  

```
vagrant up
ansible-playbook -i vagrant_inventory netagent_deploy.yml
```
  


