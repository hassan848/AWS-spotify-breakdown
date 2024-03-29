# AWS Spotify Breakdown

## Project Description
An ETL pipeline which is used to analyse Spotify albums, artists and playlists - hosted on the cloud (AWS). The script is written in Python and makes use of the 'Spotipy' API to extract data. I hosted the script on AWS Lambda, I have created an AWS Event schedular rule and attached it to the Lambda so that the Lambda is only triggered/invoked once a week, every Thursday at 5:42pm. The purpose of the ETL is that every week it automatically Extracts, Transforms and Loads the relevant new data from spotify to the storage service (s3) which can then be evaluated, analysed and be used to make reports. 

In my code, I was looking at album length over the years and whether there is a trend or change from albums of some of the most successful artists in the music industry. In the first script I looked at the average albums length of albums from the artists 'Drake', 'Micahel Jackson' and 'Bruno Mars'. In the second script I was looking at albums length of artists from a famous spotify pop playlist - and this retreived album data from the last 50 years (See csv files in data folder and visualisations). I found that many of successful albums are getting shorter and shorter in duration of the years.

## Project Infrastructure & Architecture
The Project is running on the AWS cloud and the entire project infrastructure was created using code and executing a bash script that I made (using YAML files & Cloudformation) to deploy. The infrastructure consists of a deployment S3 bucket which was used to store all the YAML files which are used to build:
* The Lambda function with code, package dependencies & environment variables
* IAM role - as the lambda execution role with the correct policies & properties
* EventBridge schedular - with a CRON expression to attach a weekly trigger to the lambda
* Cloudwatch Rule.

This bucket also stores the code for the lambda with the correct packages. I then created a second s3 bucket for storing the clean data as part of the load stage. (see below of project architecture):

![Spotify-ETL-Architecture drawio](https://github.com/hassan848/AWS-spotify-breakdown/assets/72468804/78a72032-dcb9-4d52-9600-42027cab5abe)

### How To Run

This entire infrastructure was deployed through code that I wrote (bash script and YAML file), all the commands are in the bash script above in the 'IaC' folder with the YAML file. To execute this script be sure to have the code in the same folder as the bash script and yaml file. Also be sure to configure the AWS CLI settings to your AWS account user by executing the following command:

```
aws configure
```
then execute the following two commands, to run the bash scripts:

```
chmod +x build-infrastructure.sh
```
This command simply sets the executable permission on the bash script. Now run:
```
sh build-infrastructure.sh
```
or
```
./build-infrastructure.sh
```
This command will now execute the bash script to build and deploy the entire project infrastructure on the cloud.

### Bash Instructions
The bash script being executed makes use of the YAML file and some aws cli services/commands here is a list of what the bash script does:
1. A create bucket function that will create a new AWS S3 bucket eveytime it is invoked.
2. Invokes the create-bucket function to create a deployment s3 bucket.
3. Invokes the create-bucket function to create a clean data s3 bucket.
4. Copies the local YAML file from directory to the Deployment s3 bucket in AWS cloud.
5. PIP install the necessary package dependecies for the lambda code into a new 'packages' folder.
6. Copies the lambda code/files into that same 'packages' folder.
7. cd/move into this 'packages' subdirectory.
8. ZIP the current directory => that contains the code and packages.
9. Moves this zip file to the deployment s3 bucket in the aws cloud (matching the location assigned to the lambda code in the YAML file)
10. Finally creates a CLOUDFORMATION STACK which executes the YAML file in the S3 thus deploying the lambda and rest of the cloud infrastructure.

## Prerequisites
* Python 3.x
* AWS account - to build, deploy cloud infrastructure and use AWS resources
* Spotify account (free) to use 'Spotipy' API - provides API account key
* AWS CLI Installation

## Languages, Tools & Services
<p align="left">
  <a href="https://www.python.org/" target="_blank">
    <img src="https://www.vectorlogo.zone/logos/python/python-icon.svg" alt="python" width="40" height="40"/>
  </a>
  <a href="https://aws.amazon.com/lambda/" target="_blank">
    <!-- AWS Lambda logo -->
    <img src="https://symbols.getvecta.com/stencil_9/36_lambda-function.b2a8536bdb.svg" alt="aws-lambda" width="40" height="40"/>
  </a>
  <a href="https://www.spotify.com/" target="_blank">
    <!-- Spotify logo -->
    <img src="https://www.vectorlogo.zone/logos/spotify/spotify-icon.svg" alt="spotify" width="40" height="40"/>
  </a>
  <a href="https://aws.amazon.com/cloudformation/" target="_blank">
    <!-- AWS CloudFormation logo -->
    <img src="https://symbols.getvecta.com/stencil_16/5_aws-cloudformation.14fbb098b1.svg" alt="aws-cloudformation" width="40" height="40"/>
  </a>
  <a href="https://aws.amazon.com/s3/" target="_blank">
    <!-- AWS S3 logo -->
    <img src="https://symbols.getvecta.com/stencil_24/7_amazon-s3-bucket.b7a1cbdb89.svg" alt="aws-s3" width="40" height="40"/>
  </a>
</p>


