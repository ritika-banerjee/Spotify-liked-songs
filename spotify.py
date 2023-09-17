import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = "24848505dfc745aa91921b8673a5e098"
client_secret = "2bd9cbb51d254c088c44aebe2a340172"
redirect_uri = "http://localhost:8080"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-library-read playlist-modify-public"))

# Retrieve liked songs
liked_songs = sp.current_user_saved_tracks()

# Create a dictionary to organize songs by genres
genre_dict = {}

for track in liked_songs['items']:
    artist_name = track['track']['artists'][0]['name']
    track_uri = track['track']['uri']
    
    # Retrieve artist information to infer genre (you may need external sources for genre info)
    artist_info = sp.search(q=f'artist:{artist_name}', type='artist')
    
    if artist_info['artists']['items']:
        artist_genre = artist_info['artists']['items'][0]['genres']
    else:
        artist_genre = ['Unknown']  # Assign 'Unknown' genre if no information is available
    
    for genre in artist_genre:
        if genre not in genre_dict:
            genre_dict[genre] = [track_uri]
        else:
            genre_dict[genre].append(track_uri)

# Create playlists for each genre and add songs
for genre, track_uris in genre_dict.items():
    playlist_name = f'Liked Songs - {genre}'
    sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=True)
    
    playlist_id = None
    for playlist in sp.current_user_playlists()['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            break
    
    if playlist_id:
        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
