import json
from user_based_filter import UserBasedFilter


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def main():
    file_path = "data/challenge_set.json"
    data = load_json_file(file_path)
    user_based_filter = UserBasedFilter(data)
    playlist = ["spotify:track:3W3KtDwAIg3mAruSpnfG3Q", "spotify:track:0zREtnLmVnt8KUJZZbSdla",
                "spotify:track:4rHZZAmHpZrA3iH5zx8frV", "spotify:track:3MAgQuClHcAV8E9CbeBS6f", "spotify:track:4ybvIvKdvfkdsIYYAiaTiG"]

    recommendations = user_based_filter.recommend_songs(playlist, data)
    print("Recommended songs:")
    for song, count in recommendations:
        print(f"Song: {song}, Count: {count}")

if __name__ == '__main__':
    main()
