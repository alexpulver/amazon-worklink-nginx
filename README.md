This is a basic Amazon ECS/AWS Fargate load balanced service to demo with Amazon WorkLink

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