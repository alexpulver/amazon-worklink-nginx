This is a basic Amazon ECS/AWS Fargate load balanced service to demo with Amazon WorkLink

The idea is to expose a fully private service externally. Hence all resources created
by this code are not exposed externally, only through WorkLink.

First, you should follow [Getting Started with Amazon WorkLink](https://docs.aws.amazon.com/worklink/latest/ag/getting-started.html) to configure the service
for the `nginx.example.com` domain. Then follow the instructions below to establsih routing
from WorkLink to the application.

In order to provision the application, install [AWS Cloud Development Kit](https://docs.aws.amazon.com/cdk/index.html) (CDK),
create Python virtual environment (recommended) and install the dependencies:
```bash
npm install -g aws-cdk
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

You should pre-create the following resources and provide their details in the configuration below:
* [AWS Certificate Manager](https://aws.amazon.com/certificate-manager/) certificate for `nginx.example.com` (wildcard will do as well)
* [Amazon Route 53](https://aws.amazon.com/route53/) Private Hosted Zone for `example.com`
* [Amazon Virtual Private Cloud](https://aws.amazon.com/vpc/) (VPC) with at least 2 private subnets and a NAT Gateway

The application expects a `config.json` in the root directory of the project with the following fields:
```json
{
    "account": "****",
    "certificate_arn": "arn:aws:acm:eu-west-1:****:certificate/****",
    "container_image": "nginx",
    "domain_name": "example.com",
    "hosted_zone_id":  "****",
    "nginx_domain_name": "nginx.example.com",
    "region": "eu-west-1",
    "subnet_ids": [
        "subnet-****", 
        "subnet-****"
    ],
    "vpc_id": "vpc-****"
}
```

Once the above is all sorted out, test your code by generating [AWS CloudFormation](https://aws.amazon.com/cloudformation/)
template locally:
```bash
cdk synthesize
```

If there are no errors, you can proceed to deploy the application:
```bash
cdk deploy
```
