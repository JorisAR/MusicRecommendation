import json
from collections import defaultdict
from collections import Counter


class UserBasedFilter:
    data = ""

    def __init__(self, data):
        self.data = data

    def get_song_occurrences(self):
        song_to_playlists = defaultdict(set)
        for playlist in self.data["playlists"]:
            for track in playlist["tracks"]:
                song_to_playlists[track["track_uri"]].add(playlist["pid"])

        return song_to_playlists

    def recommend_songs(self, playlist):
        song_to_playlists = self.get_song_occurrences(self.data)

        playlist_sets = [song_to_playlists[song] for song in playlist if song in song_to_playlists]
        common_playlists = set.intersection(*playlist_sets)

        song_occurrences = Counter()
        for playlist_id in common_playlists:
            for track in self.data["playlists"][playlist_id]["tracks"]:
                if track["track_uri"] not in playlist:
                    song_occurrences[track["track_uri"]] += 1

        recommendations = song_occurrences.most_common(10)
        return recommendations