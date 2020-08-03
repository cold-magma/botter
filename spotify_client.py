import random
import sys
import requests
import urllib


class SpotifyClient():
    def __init__(self, token, playlistID):
        self.playlistID = playlistID
        self.auth_token = token

    def get_random_tracks(self, word, genre, limit):
        offset = random.randint(0, 2000)
        url = 'https://api.spotify.com/v1/search?q={}&offset={}&limit={}&type=track'.format(word, offset, limit)

        response = requests.get(url,
                                headers={
                                    "Content-Type": "application/json",
                                    "Authorization": "Bearer {}".format(self.auth_token)
                                })

        response_json = response.json()
        tracks = [track for track in response_json['tracks']['items']]
        return tracks

    def added_to_lib(self, trackids):
        uris = ','.join(trackids)
        url = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(self.playlistID, uris)

        response = requests.post(url,
                                 headers={
                                     "Content-Type": "application/json",
                                     "Authorization": "Bearer {}".format(self.auth_token)
                                 })
        return response.ok
