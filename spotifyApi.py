import requests
import os
from dotenv import load_dotenv

# "Norman Fucking Rockwell": 0
# "A Deeper Understanding": 1
# "Puberty2": 2

albumUrls = {
    0: "5XpEKORZ4y6OrCZSKsi46A",
    1: "4TkmrrpjlPoCPpGyDN3rkF",
    2: "4Coa8Eb9SzjrkwWEom963Q",
}

albumTitles = {
    0: "Norman Fucking Rockwell",
    1: "A Deeper Understanding",
    2: "Puberty2"
}

load_dotenv()

SPOTIFY_GET_DEVICES_URL = "https://api.spotify.com/v1/me/player/devices"

def get_available_devices(access_token):
    response = requests.get(
        SPOTIFY_GET_DEVICES_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    resp_json = response.json()

    device_id = resp_json["devices"][0]["id"]

    return device_id

SPOTIFY_PLAY_ALBUM_URL = f"https://api.spotify.com/v1/me/player/play?device_id={get_available_devices(os.getenv('ACCESS_TOKEN_DEVICE'))}"

def play_album(albumId):
    requests.put(
        SPOTIFY_PLAY_ALBUM_URL,
        headers={
            "Authorization": f"Bearer {os.getenv('ACCESS_TOKEN_PLAY')}"
        },
        json={
            "context_uri": f"spotify:album:{albumUrls[albumId]}",
            "offset": {
                "position": 1 #taking position 1 because I like those songs more
            },
            "position_ms": 0
        }            
    )

    print(f"{albumTitles[albumId]} is now playing")