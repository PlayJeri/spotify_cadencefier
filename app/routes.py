from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from urllib.parse import urlencode
from dotenv import load_dotenv
import json, os

from .APIhelpers import get_list_id, get_song, get_token, get_username, create_list, send_songs, get_song_artist
from .forms import PlayListForm

load_dotenv()


client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
scope = "playlist-modify-public playlist-modify-private playlist-read-private"
redirect_uri = os.getenv('REDIRECT_URI')


routes = Blueprint('routes', __name__)


@routes.route('/')
def home():
  return render_template('home.html')


@routes.route('/request_spotify_token')
def request_spotify_token():
  auth_headers = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    "scope": scope
  }
  
  return redirect("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))


@routes.route('/getcode')
def getcode():
  spotify_token = request.args.get('code')

  access_token = get_token(client_id, client_secret, spotify_token, redirect_uri)
  session['spotify_token'] = access_token
  username = get_username(access_token)
  info_dic = json.loads(username.text)
  session['username'] = info_dic['id']

  return redirect(url_for('routes.playlist'))


@routes.route('/playlist', methods=['GET', 'POST'])
def playlist():
  token = session['spotify_token']
  username = session['username']
  form = PlayListForm()

  if form.validate_on_submit():
    playlist_name = form.playlist_name.data
    genre = form.genre.data
    tempo = form.tempo.data
    genre_or_artist = form.genre_or_artist.data
    create_list(token, playlist_name, username)

    list_id = get_list_id(token, playlist_name)

    offset = 0
    songs = []
    number_of_songs = 0

    while offset < 500:
    # while number_of_songs < 30:
      print(genre_or_artist)
      print(genre)
      try:
        if genre_or_artist == "Artist":
          song_ids = get_song_artist(token, genre, offset, tempo)
        elif genre_or_artist == "Genre":
          song_ids = get_song(token, genre, offset, tempo)
        songs.append(song_ids)
        offset += 50
        number_of_songs += len(song_ids)
        print(number_of_songs)
      except:
        flash('Something went wrong', 'warning')
    send_songs(token, songs, list_id)
    flash(f'Tempofier found {number_of_songs} songs for your list. Enjoy!')

  return render_template('playlist.html', form=form)