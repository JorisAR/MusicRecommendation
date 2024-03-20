import json
from collections import defaultdict
from collections import Counter


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def get_song_occurrences(data):
    song_to_playlists = defaultdict(set)
    for playlist in data["playlists"]:
        for track in playlist["tracks"]:
            song_to_playlists[track["track_uri"]].add(playlist["pid"])

    return song_to_playlists

def recommend_songs(playlist, data):
    song_to_playlists = get_song_occurrences(data)
    playlist_sets = [song_to_playlists[song] for song in playlist if song in song_to_playlists]
    common_playlists = set.intersection(*playlist_sets)

    song_occurrences = Counter()
    for playlist_id in common_playlists:
        for track in data["playlists"][playlist_id]["tracks"]:
            if track["track_uri"] not in playlist:
                song_occurrences[track["track_uri"]] += 1

    recommendations = song_occurrences.most_common(10)
    return recommendations

def main():
    file_path = "data/challenge_set.json"
    data = load_json_file(file_path)
    playlist = ["spotify:track:3W3KtDwAIg3mAruSpnfG3Q", "spotify:track:0zREtnLmVnt8KUJZZbSdla",
                "spotify:track:4rHZZAmHpZrA3iH5zx8frV", "spotify:track:3MAgQuClHcAV8E9CbeBS6f", "spotify:track:4ybvIvKdvfkdsIYYAiaTiG"]
    recommendations = recommend_songs(playlist, data)
    print("Recommended songs:")
    for song, count in recommendations:
        print(f"Song: {song}, Count: {count}")

if __name__ == '__main__':
    main()
