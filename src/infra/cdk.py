# cdk.py /path/to/file
from aws_cdk import (
    App,
    Stack,
)
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticache as elasticache
import aws_cdk.aws_iam as iam
import aws_cdk.aws_kms as kms
import aws_cdk.aws_ssm as ssm

# ----------------------------------------------------------------------
# VPN VPC Stack – holds all VPN resources
# ----------------------------------------------------------------------
class VpnVpcStack(Stack):
    """
    A stack that creates:
      • a VPC (default 1 AZ, 2 subnets)
      • an Amazon Linux 2 t3.micro instance
      • a security group that allows SSH (22) from anywhere
    """

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # VPC for server
        vpc = ec2.Vpc(
            self,
            "VpnVpc",
            max_azs=1,               # Only 1 AZ – keeps costs low
            nat_gateways=0,          # No NAT – instance can reach the internet via public IP
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                ),
            ],
        )

        # Security Group for server
        sg = ec2.SecurityGroup(
            self,
            "VpnServerSG",
            vpc=vpc,
            description="Allow SSH inbound",
            allow_all_outbound=True,
        )
        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22),
            "Allow SSH from anywhere",
        )
        sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(8000),
            "Allow requests over 8000 from anywhere",
        )

        # Server for VPN service
        ec2.Instance(
            self,
            "MyInstance",
            instance_type=ec2.InstanceType("t4g.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),
            vpc=vpc,
            security_group=sg,
            key_name="my-ssh-key",
            instance_name="VPNServer",
        )

# ----------------------------------------------------------------------
# CDK App – instantiate both stacks
# ----------------------------------------------------------------------
app = App()

vpn_stack = VpnVpcStack(app, "VpnVpcStack")

app.synth()