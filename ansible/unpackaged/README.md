# Installer - Netagent - Ansible - Deploy using Tarball

This deployment method may be desirable for very large clusters, environments where bandwidth is limited or where target 
hosts do not have access to download packages from a public repository.

The ansible playbook `netagent_deploy.yml` downloads a tarball to the local command host and then uses that to deploy netagent to all hosts 
listed in the inventory. 

---

### Pre-requisites (command host)

* Ansible 2.7
* Curl 


### Step 1 - Inventory and Configuration

Create an inventory file and specify cluster configuration using inventory variables. Your `refresh_token` and your org clusters' `cluster_name` are available via the Banyan Web Console. 

**You need to update the `package_name` with the version of Netagent you wish to install.**

Example inventory `my_inventory`:
```
[all:vars]
package_name=netagent-<version>.tar.gz
cluster_name=cluster1
refresh_token=<refresh token>

[group1]
host1.example.com
host2.example.com
```

### Step 2 - Deploy Netagent to all inventory hosts

The Netagent version you specified in `package_name` will get installed on all inventory hosts.

```
ansible-playbook -i my_inventory netagent_deploy.yml
```

---

### Debugging with Vagrant on your localhost

A quick option to try Netagent deployment on your local machine is to use Vagrant. You will need `Ansible`, `Vagrant` and a Virtual Machine provider (such as `Fusion`, `Workstation` or `VirtualBox`) installed on your local system.

First, make sure you update the `vagrant_inventory` variables including `netagent_version`, `cluster_name` and `refresh_token`.**

The commands below will bring up a VM and deploy netagent. 

```
vagrant up
ansible-playbook -i vagrant_inventory netagent_playbook.yml
```
  


