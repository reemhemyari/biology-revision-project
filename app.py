#!/usr/bin/env python3
import os

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDKs core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from biology_revision_project.biology_revision_project_stack import BiologyRevisionProjectStack
from biology_revision_project.vpc_stack import VpcStack

app = core.App()

vpc_stack = VpcStack(app, "CustomVpcStack",
                     env=core.Environment(account='674312706772', region='eu-west-1')
                     )

BiologyRevisionProjectStack(app, "BiologyRevisionProjectStack",
                            # If you don't specify 'env', this stack will be environment-agnostic.
                            # Account/Region-dependent features and context lookups will not work,
                            # but a single synthesized template can be deployed anywhere.

                            # Uncomment the next line to specialize this stack for the AWS Account
                            # and Region that are implied by the current CLI configuration.

                            # env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv(
                            # 'CDK_DEFAULT_REGION')),

                            # Uncomment the next line if you know exactly what Account and Region you
                            # want to deploy the stack to. */

                            env=core.Environment(account='674312706772', region='eu-west-1'),
                            vpc=vpc_stack.vpc

                            # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                            )

app.synth()
