from aws_cdk import (
    aws_certificatemanager as certificatemanager,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_route53 as route53,
    core
)


class Nginx(core.Stack):
    
    def __init__(self, scope: core.Construct, id: str, config: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        certificate = certificatemanager.Certificate.from_certificate_arn(
            self, 'certificate', config['certificate_arn'])
        hosted_zone = route53.HostedZone.from_lookup(
            self, 'hosted_zone', domain_name=config['domain_name'], 
            private_zone=True, vpc_id=config['vpc_id'])
        vpc = ec2.Vpc.from_lookup(self, 'vpc', vpc_id=config['vpc_id'])
        cluster = ecs.Cluster(self, 'cluster', vpc=vpc)
        
        load_balanced_fargate_service = ecs_patterns.LoadBalancedFargateService(
            self, 'fargate_service', cluster=cluster,
            certificate=certificate,
            domain_name=config['nginx_domain_name'],
            domain_zone=hosted_zone,
            image=ecs.ContainerImage.from_registry(config['container_image']),
            public_load_balancer=False
        )
        self._set_subnets(load_balanced_fargate_service, config['subnet_ids'])
    
    def _set_subnets(
            self, 
            load_balanced_fargate_service: ecs_patterns.LoadBalancedFargateService,
            subnet_ids: list) -> None:
        cfn_load_balancer = load_balanced_fargate_service.node.find_child(
            'LB/Resource')
        cfn_load_balancer.add_property_override('Subnets', subnet_ids)
        
        cfn_fargate_service = load_balanced_fargate_service.node.find_child(
            'Service/Service')
        cfn_fargate_service.add_property_override(
            'NetworkConfiguration.AwsvpcConfiguration.Subnets', subnet_ids)
