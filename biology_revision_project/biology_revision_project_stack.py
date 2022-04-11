from aws_cdk import (
    core as cdk,
    aws_rds, aws_lambda, aws_apigateway, aws_route53,
    aws_route53_targets, aws_certificatemanager, aws_ec2, aws_s3, core, aws_s3_deployment
)
from aws_cdk.aws_lambda_python import PythonFunction, PythonLayerVersion


class BiologyRevisionProjectStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, vpc: aws_ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        db_cluster = self.aurora_serverless_db(vpc)

        # Defining an AWS lambda resource
        project_lambda = PythonFunction(
            self, "aurora-serverless-db",
            entry="lambda/api_lambda",
            index="api_lambda.py",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            vpc=vpc,
            environment={
                'username': db_cluster.secret.secret_value_from_json('username').to_string(),
                'password': db_cluster.secret.secret_value_from_json('password').to_string(),
                'db_endpoint': db_cluster.cluster_endpoint.hostname
            },
            layers=[PythonLayerVersion(
                self, 'api-lambda-layer',
                compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
                entry='lambda/api_lambda_layer',  # point this to library directory
            )]
        )

        domain_name = "reemhemyari.com"
        # creates a hosted zone using route 53
        zone = self.route53_zone(domain_name)
        self.api_creation(project_lambda, domain_name, zone)
        self.frontend_creation(domain_name, zone)

    def route53_zone(self, domain_name: str) -> aws_route53.HostedZone:
        # return a hosted zone using route 53
        return aws_route53.HostedZone.from_lookup(
            self, "base-zone",
            # hosted_zone_id='Z071843118NRMFRKTL1OY'
            domain_name=domain_name
        )

    def api_creation(self, project_lambda: aws_lambda.Function, domain_name: str, zone: aws_route53.HostedZone):
        # storing my domain name & certificate in variables as I will be using them more than once
        certificate = aws_certificatemanager.Certificate.from_certificate_arn(self, "domain-certificate",
                                                                              "arn:aws:acm:eu-west-1:674312706772"
                                                                              ":certificate/bc9a8d93-3b31-48b5-8f12"
                                                                              "-e146a2dcd494")

        # defining an api endpoint that uses my lambda function
        api = aws_apigateway.LambdaRestApi(
            self, "endpoint",
            rest_api_name='biology-revision-project',
            domain_name=aws_apigateway.DomainNameOptions(
                domain_name=f"*.{domain_name}",
                certificate=certificate,
                security_policy=aws_apigateway.SecurityPolicy.TLS_1_2
            ),
            handler=project_lambda,
            endpoint_types=[aws_apigateway.EndpointType.REGIONAL]
        )

        # adds a base path
        api.domain_name.add_base_path_mapping(
            api,
            base_path="biologyrevision"
        )

        aws_route53.ARecord(
            self, "api-dns-api",
            zone=zone,
            record_name=f"api.{domain_name}",
            target=aws_route53.RecordTarget.from_alias(
                aws_route53_targets.ApiGateway(api)
            )
        )

    def aurora_serverless_db(self, vpc: aws_ec2.IVpc) -> aws_rds.ServerlessCluster:
        parameter_group = aws_rds.ParameterGroup(
            self, "parameter-group",
            engine=aws_rds.DatabaseClusterEngine.aurora_postgres(
                version=aws_rds.AuroraPostgresEngineVersion.VER_10_4
            ),
            parameters={
                "rds.force_ssl": "1"
            }
        )

        database_security_group = aws_ec2.SecurityGroup(self, "database-security-group",
                                                        vpc=vpc, allow_all_outbound=False,
                                                        security_group_name="DatabaseSecurityGroup")
        database_security_group.add_ingress_rule(peer=aws_ec2.Peer.ipv4("10.0.0.0/16"),
                                                 connection=aws_ec2.Port(string_representation="Postgres",
                                                                         protocol=aws_ec2.Protocol.TCP,
                                                                         from_port=5432, to_port=5432))
        database_security_group.add_ingress_rule(peer=aws_ec2.Peer.ipv4("86.22.20.90/32"),
                                                 connection=aws_ec2.Port(string_representation="MyHouse",
                                                                         protocol=aws_ec2.Protocol.TCP,
                                                                         from_port=5432, to_port=5432))
        database_security_group.add_egress_rule(peer=aws_ec2.Peer.ipv4("10.0.0.0/16"),
                                                connection=aws_ec2.Port(string_representation="Postgres",
                                                                        protocol=aws_ec2.Protocol.TCP,
                                                                        from_port=5432, to_port=5432))

        aurora_db_cluster = aws_rds.ServerlessCluster(
            self, 'database',
            engine=aws_rds.DatabaseClusterEngine.AURORA_POSTGRESQL,
            vpc=vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.ISOLATED),
            security_groups=[database_security_group],
            parameter_group=parameter_group
        )

        return aurora_db_cluster

    def frontend_creation(self, domain_name: str, zone: aws_route53.HostedZone):
        bucket_name = f"biorevise.{domain_name}"
        website_bucket = aws_s3.Bucket(self, "website-s3-bucket",
                                       bucket_name=bucket_name,
                                       website_index_document='index.html',
                                       website_error_document='index.html',
                                       public_read_access=True,
                                       removal_policy=core.RemovalPolicy.DESTROY)

        aws_s3_deployment.BucketDeployment(self, "website-s3-deploy",
                                           sources=[aws_s3_deployment.Source.asset("front_end/build")],
                                           destination_bucket=website_bucket)

        aws_route53.ARecord(
            self, "website-dns-www",
            zone=zone,
            record_name=bucket_name,
            target=aws_route53.RecordTarget.from_alias(
                aws_route53_targets.BucketWebsiteTarget(website_bucket)
            )
        )
