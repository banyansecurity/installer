# Ansible Install

A convenient and scalable way to deploy netagent. 

## Overview

myhost_inventory:
```
[myhosts]
host1.example.com
host2.example.com

[myhosts:vars]
cluster_name=cluster1
refresh_token=<refresh token copied from banyan console>
```

netagent_playbook.yml
```yaml
- hosts: myhosts
  become: yes
  become_user: root
  become_method: sudo
  tasks:
    - name: Enable EPEL Repo
      yum:
        name: epel-release
        state: present
    - name: Install dependencies
      yum:
        name: jq
        state: present
    - name: Install RPM
      yum: 
        name: https://s3-us-west-2.amazonaws.com/www.banyanops.com/onramp/rpm/banyan-netagent-0.7.1-rc11.x86_64.rpm
        state: present
    - name: Run RPM post-install, install script
      shell: /opt/banyan-packages/install '{{refresh_token}}' {{cluster_name}}
```

Deploy netagent to all hosts listed in `myhost_inventory` with single command:

```
./ansible-playbook -i myhost_inventory netagent_playbook.yml
```