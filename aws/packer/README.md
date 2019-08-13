# Packer can bake Banyan Netagent into an AMI image

## prequisites

- [packer](https://www.packer.io/)
- [ansible](https://www.ansible.com/)
- aws credentials access key & secret key

## usage 

AMI Build:
```shell
packer validate packer.json && \
packer build \
-var 'aws_access_key=${AWS_ACCESS_KEY}' \
-var 'aws_secret_key=${AWS_SECRET_KEY}' \
-var 'netagent_version=1-5-0' \
packer.json
```

## notes

- This packer script will generate an AMI image based on the latest Amazon Linux 2 AMI
- The AMI produced only installs the netagent package and still must be configured for the environment 
- For an example of how to use the AMI see: https://bitbucket.org/banyanops/installer/src/master/cloudformation/