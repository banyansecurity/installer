# Installer - Netagent - Ansible

This section contains 2 deployment methods to install the Banyan Netagent using Ansible - **DEB/RPM package** and **Tarball**.

---

## Deploy using DEB/RPM package

The **DEB/RPM package** deployment method provides a convenient and scalable way to deploy the Banyan Netagent using DEB/RPM repo packages for your Linux operating system.

Review the details in the [Ansible DEB/RPM Packaged section](packaged).


## Deploy using Tarball

The **Tarball** deployment method may be desirable for very large clusters, environments where bandwidth is limited or where target hosts do not have access to download packages from a public repository.

In this deployment method the Ansible playbook downloads a `tarball` to the local command host and then uploads that to all hosts listed in the inventory to deploy the Netagent. 

Review the details in the [Ansible Tarball Unpackaged section](unpackaged).
