# Provisioning code using AWS API and boto
# Author: Rui Shu

# pip install boto3 awscli

# Refered resources:
# https://blog.shikisoft.com/accessing-aws-resources-using-python-scripts/
# https://www.slsmk.com/getting-started-with-amazon-aws-and-boto3/
# https://blog.ipswitch.com/how-to-create-an-ec2-instance-with-python

import boto3

# create a file to store the key locally
# outfile = open('rshu-ec2-keypair.pem','w')

# # call the boto ec2 function to create a key pair
# key_pair = ec2.create_key_pair(KeyName='rshu-ec2-keypair')

# # capture the key and store it in a file
# KeyPairOut = str(key_pair.key_material)
# print(KeyPairOut)
# outfile.write(KeyPairOut)

ec2 = boto3.resource('ec2')
ec2client = boto3.client('ec2')

vpc = ec2.Vpc('vpc-0176993a3d93b2a48')
# Attributes
print(vpc.cidr_block)
print(vpc.state)
print(vpc.id)

vpclist = vpc.instances.all()
for instance in vpclist:
    print(instance)

subnets = list(vpc.subnets.all())
if len(subnets) > 0:
	print("\nSubnets:")
	for subnet in subnets:
		print(subnet.id, "-", subnet.cidr_block)
else:
	print("There is no subnet in this VPC!")


# create a new EC2 instance
instances = ec2.create_instances(
     ImageId='ami-0080e4c5bc078760e',
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.micro',
     KeyName='rshu-ec2-keypair',
     NetworkInterfaces=[{'SubnetId': 'subnet-0b518d5b7e5c66570', 'DeviceIndex': 0, 'AssociatePublicIpAddress': True}]
 )

# for instance in instances:
response = ec2client.describe_instances()
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        # This sample print will output entire Dictionary object
        print(instance)
        # This will print will output the value of the Dictionary key 'InstanceId'
        # print(instance["InstanceId"])
        if instance[u'State'][u'Name'] == 'running' and instance.get(u'PublicIpAddress') is not None:
        	print(instance.get(u'PublicIpAddress'))
