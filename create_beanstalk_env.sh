#!/bin/bash

ENV_NAME=pdbv-dev
VPC_ID=$(aws ec2 describe-vpcs --query 'Vpcs[].VpcId' --output text)
VPC_SUBNETS=$(aws ec2 describe-subnets --query 'Subnets[].SubnetId' --output text | sed -E 's/[[:space:]]+/,/g')
VPC_SECURITYGROUPS=$(aws ec2 describe-security-groups --query 'SecurityGroups[?GroupName==`default`].GroupId' --output text)
DB_NAME=peeringdb
DB_PASS=$(openssl rand -hex 16)

eb create --platform python-2.7 \
          --vpc \
          --vpc.id $VPC_ID \
          --database \
          --database.username $DB_NAME \
          --database.password $DB_PASS \
          --vpc.publicip \
          --vpc.ec2subnets $VPC_SUBNETS \
          --vpc.elbsubnets $VPC_SUBNETS \
          --vpc.securitygroups $VPC_SECURITYGROUPS \
          --vpc.elbpublic \
          --vpc.dbsubnets $VPC_SUBNETS \
          $ENV_NAME 
