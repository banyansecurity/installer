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