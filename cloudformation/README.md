# Installer - AccessTier - AWS - Deploy using CloudFormation

### Prerequisites

* `Amazon Web Services (AWS)` account
* Permissions to launch `EC2` instances, manage `AutoScaling` and set `Security Groups`.

### Step 1 - Ensure AWS Networking

Ensure that your VPC has an Internet Gateway attached and a Public Subnet where you can deploy the AccessTier.


### Step 2 - Create the AccessTier Stack using CloudFormation in the AWS Console

Navigate in the AWS Console to CloudFormation > Create stack.

Upload the `banyan-elastic-access-tier.json` file.


### Step 3 - Enter the Parameters required and deploy AccessTier

Provide a `Stack name`, specify the `VPC` into which the AccessTier should be deployed as well other relevant details.

Click Start to deploy the AccessTier.


---


### Set up AWS networking on a brand new VPC

A quick option to try the AccessTier CloudFormation deployment on a brand new VPC is to use the `banyan-network-stack.json` file to provision all the requisite AWS Networking.

You can then immediately launch the AccessTier Stack using CloudFormation.