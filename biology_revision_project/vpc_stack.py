from aws_cdk import(
    core as cdk,aws_rds,aws_lambda,aws_apigateway,
    aws_route53,aws_route53_targets, aws_ec2,
    aws_certificatemanager
)


class VpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = aws_ec2.Vpc(
            self, "custom-vpc",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(name="Isolated", cidr_mask=26, subnet_type=aws_ec2.SubnetType.ISOLATED)
            ],

        )

        ingressSecurityGroup = aws_ec2.SecurityGroup(self, "ingress-security-group",
                                                     vpc=self.vpc, allow_all_outbound=False,
                                                     security_group_name="IngressSecurityGroup")
        ingressSecurityGroup.add_ingress_rule(peer=aws_ec2.Peer.ipv4("10.0.0.0/16"),
                                              connection=aws_ec2.Port(string_representation="Postgres",
                                                                      protocol=aws_ec2.Protocol.TCP,
                                                                      from_port=5432, to_port=5432))
