# Deploy Access Tier using AWS CloudFormation

### Prerequisites

* `Amazon Web Services (AWS)` account
* Permissions to launch `EC2` instances, manage `AutoScaling` and set `Security Groups`.

### Ensure AWS Networking

Ensure that your VPC has all of the following:
   *  An Internet Gateway
   *  A Public Subnet where you can deploy the AccessTier

For a new VPC, a quick option to try the Access Tier CloudFormation deployment is to use the `network/banyan-network-stack.json` stack
to provision all the requisite AWS Networking.

### Choose the Access Tier stack to deploy

To deploy Access Tier using the latest `netagent-2.x.x`, use the stacks in the `netagent2` folder.

To deploy Access Tier using legacy `netagent-1.x.x`, use the stacks in the `netagent1` folder.

Each folder has a README explaining how to deploy the stack.
