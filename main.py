import json

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def main():
    file_path = "data/challenge_set.json"  # Replace 'your_file_path.json' with the actual file path
    data = load_json_file(file_path)
    print("Date:", data["date"])
    print("Version:", data["version"])
    print("Playlists:")
    print(len(data["playlists"]))
    count = 0
    track_uri = "spotify:track:3W3KtDwAIg3mAruSpnfG3Q"
    for playlist in data["playlists"]:
        for track in playlist["tracks"]:
            if track["track_uri"] == track_uri:
                count += 1



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
