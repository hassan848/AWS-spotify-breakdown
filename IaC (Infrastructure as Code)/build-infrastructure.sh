#!/bin/bash

# AWS CLI command to create S3 bucket
create_bucket() {
  aws s3 mb s3://"$1" --region "$2"
}

# I'm going to create a deployment bucket first and then a clean data bucket to store the clean, transformed data bucket.
bucket1="build-deployment-bucket848"
bucket2="spotify-clean-data"

# My region is eu-west-2
region="eu-west-2"

# Create the first deployment bucket
create_bucket "$bucket1" "$region"
echo "Bucket $bucket1 created successfully."

# Create the second bucket
create_bucket "$bucket2" "$region"
echo "Bucket $bucket2 created successfully."


# store IaC YAML file in deployment bucket
# This YAML file is used to create the CLOUDFORMATION STACK for the lambda function 
# with CLOUDWATCH EVENTBRIDGE to automatically invoke/trigger the lambda once a week
aws s3 cp create-lambda-schedular.yaml s3://build-deployment-bucket848/templates/create-lambda-schedular.yaml


# Install the dependecies for the lambda function into a new sub-directory
pip install spotipy==2.16.1 urllib3==1.25.11 --target ./new-packages
# copy the lambda code from the current directory to the packages subdirectory
cp lambda_function.py new-packages/lambda_function.py

# MOVE into the subdirectory
cd new-packages

# zip the current directory => with the code and packages 
zip -r lambda_function_code.zip .

# Move the zip file to the deployment s3 bucket
aws s3 cp lambda_function_code.zip s3://build-deployment-bucket848/code/


# create CLOUDFORMATION STACK
aws cloudformation create-stack --stack-name build-spotify-stack --template-url https://build-deployment-bucket848.s3.eu-west-2.amazonaws.com/templates/create-lambda-schedular.yaml --region eu-west-2 --capabilities CAPABILITY_NAMED_IAM
