import spotipy
import csv
from datetime import datetime

from config.playlists import pop_playlists


spotipy_object = spotipy.Spotify(client_credentials_manager=spotipy.oauth2.SpotifyClientCredentials())

PLAYLIST_NAME = 'top 100 pop'

def get_artists_from_spotify_playlist(uri_link):
    artists = {}
    # First get all the songs in the playlist using URI 
    songs_in_playlist = spotipy_object.playlist_tracks(uri_link)
    
    # Now iterate through the songs list and return the artist and it's URI as a dictionary
    # E.G. artists = {'uri-link89845989548954': 'Drake'}
    for song in songs_in_playlist['items']:
        if song['track']:
            artists[song['track']['artists'][0]['uri']] = song['track']['artists'][0]['name']
            
    return artists

 
def get_artists_albums():
    playlist_uri = pop_playlists()[PLAYLIST_NAME]
    artists_dict = get_artists_from_spotify_playlist(playlist_uri)
    
    albums = []
    album_data_list = []
    
    for artist_uri in list(artists_dict.keys()):
        artists_albums = spotipy_object.artist_albums(artist_uri, album_type='album', limit=50)
        # iterate through the artists albums
        for album in artists_albums['items']:
            if 'GB' and 'US' in album['available_markets']:
                key = album['name'] + album['artists'][0]['name'] + album['release_date'][:4]
                if key not in albums:
                    albums.append(key)
                    album_data = spotipy_object.album(album['uri'])
                    
                    album_duration = 0
                    for song in album_data['tracks']['items']:
                        album_duration = song['duration_ms'] + album_duration
                    # writer.writerow({'Year Released': album_data['release_date'][:4],
                    #                     'Album Length': album_duration,
                    #                     'Album Name': album_data['name'],
                    #                     'Artist': album_data['artists'][0]['name']})
                    album_dict = {
                        'Artist': album_data['artists'][0]['name'],
                        'Album Name': album_data['name'],
                        'Album Duration MS': album_duration,
                        'Year Released': album_data['release_date'][:4]
                    }
                    album_data_list.append(album_dict)
                    
    return album_data_list


def sort_by_year(e):
    return e['Year Released']

def sort_albums_by_year(albums_data_list):
    albums_data_list.sort(key=sort_by_year)
    
    return albums_data_list


def load_to_csv(albums_sorted_list):
    headers = list(albums_sorted_list[0].keys())
    
    with open('top-100-pop.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        # Iterate through album list and write to csv
        for album in albums_sorted_list:
            writer.writerow(album)

albums_data_list = get_artists_albums()
albums_sorted_list = sort_albums_by_year(albums_data_list)
load_to_csv(albums_sorted_list)
