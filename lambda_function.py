import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials
import csv
import boto3
import os
from io import StringIO
from datetime import datetime

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

artists = ['Drake', 'Michael Jackson', 'Bruno Mars']
s3_bucket = 'spotify-clean-data'

def get_artists_uri():
    uri_dict = {}
    for artist in artists:
        if len(sys.argv) > 1:
            name = ' '.join(sys.argv[1:])
        else:
            name = artist   

        results = spotify.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
       
        uri_dict[name] = items[0]['uri']
        
        # print(items[0]['name'], ' - ', items[0]['uri'])
    return uri_dict

def get_artist_albums_data(artist_data_dict, artists_uri_dict):
    for artist in artists_uri_dict: # Loop through the different artists from the dict
        # first get all the albums of the current artist
        artist_albums = spotify.artist_albums(artists_uri_dict[artist], album_type='album', limit=50)
        
        artist_data_dict[artist] = [] 
        # set the dict list for the artist
        
        # now loop through each album of the current artist
        for album in artist_albums['items']:
            if 'GB' in artist_albums['items'][0]['available_markets']:
                album_data = spotify.album(album['uri'])
                # loop through each song in the current album sum together their lengths
                
                album_duration_ms = 0
                for song in album_data['tracks']['items']:
                    album_duration_ms += song['duration_ms']
                
                album_data = {
                    'Artist': artist,
                    'Album Name': album_data['name'],
                    'Album Duration MS': album_duration_ms,
                    'Year Released': album_data['release_date'][:4] 
                    # Extract just the year from the full date using slicing  
                }
                artist_data_dict[artist].append(album_data)
                # append the album data to the artist data dict
                
    return artist_data_dict


# print(artist_data_dict[artists[0]])
# for album in artist_data_dict[artists[0]]:
#     print(album)

def sort_by_year(e):
    return e['Year Released']

def sort_albums_by_year(artist_data_dict):
    for artist in artists:
        artist_data_dict[artist].sort(key=sort_by_year)
    
    return artist_data_dict

def upload_to_s3(csv_content, s3_object_key):
    s3_client = boto3.client('s3')

    try:
        s3_client.put_object(Body=csv_content, Bucket=s3_bucket, Key=s3_object_key)
        print(f"CSV file uploaded to S3: s3://{s3_bucket}/{s3_object_key}")
    except Exception as e:
        print(f"Error uploading CSV file to S3: {e}")

def load_to_csv(artist_data_dict):
    headers = artist_data_dict[artists[0]][0].keys()
    # Write a different csv file for each artist
    
    date = datetime.now()
    
    for artist in artists:
        csv_content = StringIO()
        writer = csv.DictWriter(csv_content, fieldnames=headers)
        writer.writeheader()

        # for all albums in dict list write row for current artist
        for album in artist_data_dict[artist]:
            writer.writerow(album)
    
        s3_object_key = f'{date.year}/{date.month}/{date.day}/{artist}_albums_data.csv'
        upload_to_s3(csv_content.getvalue(), s3_object_key)

def lambda_handler(event, context):
    artists_uri_dict = get_artists_uri()
    artist_data_dict = {}
    artist_data_dict = get_artist_albums_data(artist_data_dict, artists_uri_dict)
    artists_uri_dict = sort_albums_by_year(artist_data_dict)
    load_to_csv(artist_data_dict)
    print('Data Loaded')
