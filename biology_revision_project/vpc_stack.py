from aws_cdk import(
    core as cdk, aws_ec2
)


class VpcStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = aws_ec2.Vpc(
            self, "custom-vpc",
            cidr="10.0.0.0/16",
            max_azs=2,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(name="Isolated", cidr_mask=26, subnet_type=aws_ec2.SubnetType.ISOLATED),
                aws_ec2.SubnetConfiguration(name="Public", cidr_mask=26, subnet_type=aws_ec2.SubnetType.PUBLIC)
            ],

        )
