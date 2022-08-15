from aws_cdk import (
    aws_ec2 as ec2,
    aws_rds as rds,
    aws_apigatewayv2_integrations_alpha as aws_ag,
    aws_lambda
)
import aws_cdk as cdk
from constructs import Construct

class CellmapApiAwsStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, public: bool = True, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        instance_identifier = 'cellmap-db'
        credsSecretName = f'/{construct_id}/rds/creds/{instance_identifier}'.lower();
        creds = rds.DatabaseSecret(self, id='cellmap-rds-creds', username='postgres', secret_name=credsSecretName)
        subnet_config =[ec2.SubnetConfiguration(name='ingress', 
                                                subnet_type=ec2.SubnetType.PUBLIC,
                                                cidr_mask=24),
                        ec2.SubnetConfiguration(name='rds', 
                                                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED,
                                                cidr_mask=28)]
        vpc = ec2.Vpc(self, id='cellmap-rds-vpc', subnet_configuration=subnet_config)

        rds_instance = rds.DatabaseInstance(self,
                                            id='cellmap-rds-instance',
                                            vpc=vpc,
                                            vpc_subnets={'subnet_type': ec2.SubnetType.PUBLIC},
                                            engine=rds.DatabaseInstanceEngine.postgres(version = rds.PostgresEngineVersion.VER_14_2),
                                            instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE3, ec2.InstanceSize.MICRO),
                                            database_name='cellmap',
                                            instance_identifier=instance_identifier,
                                            credentials=rds.Credentials.from_secret(creds),
                                            multi_az=False,
                                            allocated_storage=20,
                                            max_allocated_storage=35,
                                            allow_major_version_upgrade=False,
                                            auto_minor_version_upgrade=True,
                                            delete_automated_backups=True,
                                            removal_policy=cdk.RemovalPolicy.DESTROY,
                                            deletion_protection=False,
                                            publicly_accessible=public
                                            )
        rds_instance.connections.allow_from_any_ipv4(ec2.Port.tcp(5432))
        cdk.CfnOutput(self, 'dbEndpoint', value=rds_instance.instance_endpoint.hostname)
        cdk.CfnOutput(self, 'secretName', value=rds_instance.secret.secret_name)

        

