# Deploy using repo package

A convenient and scalable way to deploy the banyan netagent with Ansible.

###Pre-requisites (command host)
* Ansible 2.7
* Curl 

###Step 1
Create an inventory file. 

example_inventory
```
[group1]
host1.example.com
host2.example.com

[group1:vars]
cluster_name=cluster1
refresh_token=<refresh token copied from banyan console>
```

###Step 2 
Deploy netagent to all inventory hosts using a single command

```
ansible-playbook -i example_inventory netagent_playbook.yml
```