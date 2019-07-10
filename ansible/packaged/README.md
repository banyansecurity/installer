# Installer - Netagent - Ansible - Deploy using DEB/RPM package

This deployment method provides a convenient and scalable way to deploy the Banyan Netagent using DEB/RPM repo packages for your Linux operating system.

---

### Pre-requisites (on Command Host)

* Ansible 2.7
* Curl 


### Step 1 - Inventory and Configuration

Create an inventory file and specify cluster configuration using inventory variables. Your `refresh_token` and your org clusters' `cluster_name` are available via the Banyan Web Console.

Example inventory `my_inventory`:
```
[all:vars]
cluster_name=cluster1
refresh_token=<refresh token copied from banyan console>

[group1]
host1.example.com
host2.example.com
```


### Step 2 - Deploy Netagent to all inventory hosts

The latest Netagent version will get installed on all inventory hosts.

```
ansible-playbook -i my_inventory netagent_playbook.yml
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