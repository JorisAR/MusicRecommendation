import json
from user_based_filter import UserBasedFilter
from item_based_filter import ItemBasedFilter
import pandas as pd

def load_csv_file(file_path):
    return pd.read_csv(file_path, nrows=50000)

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def main():
    playlist_file_path = "data/challenge_set.json"
    song_file_path = "data/dataset.csv"

    playlist_data = load_json_file(playlist_file_path)
    song_data = load_csv_file(song_file_path)

    user_based_filter = UserBasedFilter(playlist_data)
    item_based_filter = ItemBasedFilter(song_data)

    playlist = ["3W3KtDwAIg3mAruSpnfG3Q", "0zREtnLmVnt8KUJZZbSdla",
                "4rHZZAmHpZrA3iH5zx8frV", "3MAgQuClHcAV8E9CbeBS6f", "4ybvIvKdvfkdsIYYAiaTiG", "5vjLSffimiIP26QG5WcN2K"]

    #user_based_filter.recommend_songs(playlist, 10)
    item_based_filter.recommend_songs(playlist, 10)

if __name__ == '__main__':
    main()
