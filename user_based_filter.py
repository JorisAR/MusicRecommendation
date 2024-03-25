class UserBasedFilter:
    data = ""

    def __init__(self, data):
        self.data = data

    def id_to_uri(self, id):
        return "" + id

    def get_shared_playlists(self, track_id):
        playlists = []
        for playlist in self.data["playlists"]:
            for track in playlist["tracks"]:
                if track["track_uri"] == self.id_to_uri(track_id):
                    playlists.append(playlist)
                    break
        return playlists

    def count_song_occurrences(self, playlists):
        song_counts = {}
        for playlist in playlists:
            for track in playlist["tracks"]:
                if track["track_uri"] not in song_counts:
                    song_counts[track["track_uri"]] = 0
                song_counts[track["track_uri"]] += 1
        return song_counts

    def recommend_songs(self, playlist, N):
        shared_playlists = []
        for track_uri in playlist:
            shared_playlists.extend(self.get_shared_playlists(track_uri))

        song_counts = self.count_song_occurrences(shared_playlists)
        sorted_songs = sorted(song_counts.items(), key=lambda item: item[1], reverse=True)

        recommended_songs = [song[0] for song in sorted_songs if song[0] not in playlist][:N]
        print(f"Recommended songs: {recommended_songs}")
        return recommended_songs
