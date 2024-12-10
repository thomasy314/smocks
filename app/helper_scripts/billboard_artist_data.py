import json
import pathlib
import requests

from config import GoogleConfig

def get_artist_index_json(start_page=1, number_of_pages=10):

    query = "%22ARTIST+INDEX%22+filetype:pdf"
    key = GoogleConfig.SEARCH_KEY
    search_engine = GoogleConfig.SEARCH_BILLBOARD_ENGINE

    cur_page = start_page

    artist_index_json = []

    for page_number in range(0, number_of_pages):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={key}=&cx={search_engine}&start={cur_page}"
        response = requests.get(url)
        data = response.json()

        artist_index_json += data['items']

        cur_page = data['queries']['nextPage'][0]['startIndex']

    return artist_index_json

if __name__ == "__main__":
    artist_index_json = get_artist_index_json(number_of_pages=10)
    file_path = pathlib.Path(__file__).parent.resolve()
    with open(f"{file_path}/artist_index_files.js", "w") as f:
        f.write(json.dumps(artist_index_json))



