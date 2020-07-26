import os
from spotify_client import SpotifyClient


def run(auth, pID, word, genre, limit):
    spotify_client = SpotifyClient(auth, pID)
    randomtracks = spotify_client.get_random_tracks(word, genre, limit)
    tracks_uri = [track['uri'] for track in randomtracks]

    addedtolib = spotify_client.added_to_lib(tracks_uri)
    if addedtolib:
        return True
    return False
