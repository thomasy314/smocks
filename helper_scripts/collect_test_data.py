import json
import logging
import os
import sys
from datetime import datetime, timezone
from time import sleep

file_path = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(file_path, '..')))

from app.music_api.music_api import MusicAPI

artist_id = '381086ea-f511-4aba-bdf9-71c753dc5077' # kendrick lamar
music_api = MusicAPI()
file_name = "artist_test_data.txt"
file_loc = os.path.join(file_path, file_name)

while(True):
    artist_data = music_api.get_artist(artist_id).serialize
    logging.info(f"Fetched data for artist ID {artist_id} at {datetime.now(timezone.utc).isoformat(timespec="seconds")}")
    logging.info(artist_data)

    with open(file_loc, "a+") as file:
        file.write(json.dumps(artist_data) + "\n")

    sleep(60)