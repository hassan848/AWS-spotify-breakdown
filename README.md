# AWS Spotify Breakdown

## Project Description
An ETL pipeline which is used to analyse Spotify albums, artists and playlists - hosted on the cloud (AWS). The script is written in Python and makes use of the 'Spotipy' API to extract data. I hosted the script on AWS Lambda, I have created an AWS Event schedular rule and attached it to the Lambda so that the Lambda is only triggered/invoked once a week, every Thursday at 5:42pm. The purpose of the ETL is that every week it automatically Extracts, Transforms and Loads the relevant new data from spotify to the storage service (s3) which can then be evaluated, analysed and be used to make reports. 

In my code, I was looking at album length over the years and whether there is a trend or change from albums of some of the most successful artists in the music industry. In the first script I looked at the average albums length of albums from the artists 'Drake', 'Micahel Jackson' and 'Bruno Mars'. In the second script I was looking at albums length of artists from a famous spotify pop playlist - and this retreived album data from the last 50 years (See csv files in data folder and visualisations). I found that many of successful albums are getting shorter and shorter in duration of the years.

## Project Infrastructure & Architecture
The Project is running on the AWS cloud and the entire project infrastructure was created using code and executing a bash script that I made (using YAML files & Cloudformation) to deploy. The infrastructure consists of a deployment S3 bucket which was used to store all the YAML files to build the Lambda, IAM role, EventBridge schedular and Cloudwatch Rule. This bucket also stores the code for the lambda with the correct packages. I then created a second s3 bucket for storing the clean data as part of the load stage. (see below of project architecture):

![Spotify-ETL-Architecture drawio](https://github.com/hassan848/AWS-spotify-breakdown/assets/72468804/78a72032-dcb9-4d52-9600-42027cab5abe)

This entire infrastructure was deployed through code that I wrote (bash script and YAML file), all the commands are in the bash script above in the 'IaC' folder with the YAML file. To execute this script be sure to have the code in the same folder as the bash script and yaml file, then execute the following two commands:

```chmod +x build-infrastructure.sh
```
This command simply sets the executable permission on the bash script.
```sh build-infrastructure.sh
```
or
```./build-infrastructure.sh
```

