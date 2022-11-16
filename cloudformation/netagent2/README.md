# Deploy Access Tier with Netagent v2 using AWS CloudFormation

> :warning: **Note: Netagent v2 has been released, simplifying the process of installing and configuring an Access Tier. If you need to use Netagent v1, use the [legacy v1 guides](../netagent1).**

### Prerequisites

* `Amazon Web Services (AWS)` account
* Permissions to launch `EC2` instances, manage `AutoScaling` and set `Security Groups`.

### Step 1 - Ensure AWS Networking

Ensure that your VPC has an Internet Gateway attached and a Public Subnet where you can deploy the AccessTier.


### Step 2 - Register your Access Tier in the Banyan Command Center

Create an Access Tier in the Command Center (console UI or API).


### Step 3 - Create the AccessTier Stack using CloudFormation in the AWS Console

Navigate in the AWS Console to CloudFormation > Create stack.

Upload the file `banyan-access-tier-v2-ubuntu.json` or `banyan-access-tier-v2-amazon-linux.json`.

In this template, use the access tier name as the `Stack name`, and specify the `VPC` into which the AccessTier should be deployed as well other relevant details.

Click Start to deploy the AccessTier.


---


### Set up AWS networking on a brand new VPC

A quick option to try the AccessTier CloudFormation deployment on a brand new VPC is to use the `banyan-network-stack.json` file to provision all the requisite AWS Networking.

You can then immediately launch the AccessTier Stack using CloudFormation.

---

## DataDog metrics integration

Real-time connection metrics can be sent to DataDog (enabled through command center access tier settings).
Each instance of the Access Tier will send the following metrics:

| Name | Description |
| :--- | :---------- |
| `banyan.connections` | Total number of incoming connections |
| `banyan.receive_rate` | Received bytes per second |
| `banyan.transmit_rate` | Transmitted bytes per second |
| `banyan.decision_time` | Time required to make authorization decisions, in seconds |
| `banyan.response_time` | Total time required to send response to the user, in seconds |
| `banyan.unauthorized_attemps` | Number of connections rejected due to missing client certificates or policy decisions |

The metrics are tagged with `hostname`, `port`, `service`, and `site_name` so you can filter metrics for a particular Access Tier, host, or service.

Support for other protocols (e.g. statsd, prometheus) and monitoring systems will be added in the future.

To enable the DataDog agent, paste your [DataDog API Key][] into the parameter `BanyanDDAPIKey`.

[DataDog API Key]: https://docs.datadoghq.com/account_management/api-app-keys/#add-an-api-key-or-client-token
