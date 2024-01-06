# AWS Spotify Breakdown

## Project Description
An ETL pipeline which is used to analyse Spotify albums, artists and playlists - hosted on the cloud (AWS). The script is written in Python and makes use of the 'Spotipy' API to extract data. I hosted the script on AWS Lambda, I have created an AWS Event schedular rule and attached it to the Lambda so that the Lambda is only triggered/invoked once a week, every Thursday at 5:42pm. The purpose of the ETL is that every week it automatically Extracts, Transforms and Loads the relevant new data from spotify to the storage service (s3) which can then be evaluated, analysed and be used to make reports. 

In my code, I was looking at album length over the years and whether there is a trend or change from albums of some of the most successful artists in the music industry. In the first script I looked at the average albums length of albums from the artists 'Drake', 'Micahel Jackson' and 'Bruno Mars'. In the second script I was looking at albums length of artists from a famous spotify pop playlist - and this retreived album length data of around 50 years.
