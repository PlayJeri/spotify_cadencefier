import requests
import base64
import json
  


def get_token(client_id, client_secret, spotify_token, redirect_uri):
    encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": spotify_token,
        "redirect_uri": redirect_uri
    }

    r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    token = r.json()['access_token']

    return token


def get_username(token):
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'}

    response = requests.get('https://api.spotify.com/v1/me', headers=headers)

    return response


def create_list(token, playlist_name, username):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    json_data = {
        'name': f'{playlist_name}',
        'description': 'New playlist description',
        'public': False,
    }

    requests.post(f'https://api.spotify.com/v1/users/{username}/playlists', headers=headers, json=json_data)

  
def get_list_id(token, playlist_name):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    params = {
        'limit': "30",
    }

    response = requests.get('https://api.spotify.com/v1/me/playlists', params=params, headers=headers)
    playlists = (json.loads(response.text))

    for playlist in playlists['items']:
        playlist_name = playlist['name']
        if playlist_name == playlist_name:
            list_id = (playlist['id'])
            return list_id


def get_song(token, genre, offset, tempo):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    params = {
        'q': f'genre:{genre}',
        'type': 'track',
        'limit': '50',
        'offset': f'{offset}'
    }

    response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)
    tracks = (json.loads(response.text))

    songs = []
    song_ids = []
    for track in tracks['tracks']['items']:
        song_ids.append(track['id'])

    song_id_str = ','.join(song_ids)    

    tempo_matched_songs = song_info(token, song_id_str, tempo)

    for song in tempo_matched_songs:    
        songs.append(song)

    return songs

def song_info(token, song_id_str, tempo):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    response = requests.get(f'https://api.spotify.com/v1/audio-features?ids={song_id_str}', headers=headers)
    info = (json.loads(response.text))
    song_ids = []

    # for song in info['audio_features']:
    #     if min_tempo < float(song['tempo']) < max_tempo or ((min_tempo*2) < float(song['tempo']) < (max_tempo*2)):
    #         song_ids.append(song['id'])

    for song in info['audio_features']:
        if tempo - 2 < float(song['tempo']) < tempo + 2 or (tempo * 2 - 2) < float(song['tempo']) < (tempo * 2 - 2) or (tempo / 2 - 2) < float(song['tempo']) < (tempo / 2 + 2):
            song_ids.append(song['id'])

    return song_ids

def send_songs(token, songs, list_id):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    song_id_string = ''

    for song_list in songs:
        for song_id in song_list:
            song_id_string += f'spotify:track:{song_id},'
            

    params = {
        'uris': song_id_string
    }

    requests.post(f'https://api.spotify.com/v1/playlists/{list_id}/tracks', params=params, headers=headers)
  
    print("LIST CREATED")



def get_song_artist(token, artist, offset, tempo):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }

    params = {
        'q': f'artist:{artist}',
        'type': 'track',
        'limit': '50',
        'offset': f'{offset}'
    }

    response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)
    tracks = (json.loads(response.text))

    songs = []
    song_ids = []
    for track in tracks['tracks']['items']:
        song_ids.append(track['id'])

    song_id_str = ','.join(song_ids)    

    tempo_matched_songs = song_info(token, song_id_str, tempo)

    for song in tempo_matched_songs:    
        songs.append(song)

    return songs