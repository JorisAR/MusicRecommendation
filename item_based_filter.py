from sklearn.neighbors import NearestNeighbors

from memory_profiler import profile

class ItemBasedFilter:
    def __init__(self, data):
        self.data = data
        self.features = ['danceability', 'explicit', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence']
        self.nearest_neighbors = NearestNeighbors(n_neighbors=50, algorithm='auto', metric='cosine')
        self.fit()

    def fit(self):
        X = self.data[self.features]
        self.nearest_neighbors.fit(X)

    @profile
    def recommend_songs(self, playlist, N):
        # Transform input playlist features
        input_features = self.data[self.data['track_id'].isin(playlist)][self.features]

        if input_features.shape[0] == 0:
            print("Input features are empty. Cannot recommend songs.")
            return []

        # Query NearestNeighbors for similar items
        _, indices = self.nearest_neighbors.kneighbors(input_features)

        # Get recommended songs
        recommended_songs = self.data.iloc[indices[0]]['track_id'].tolist()

        recommended_songs = [song for song in recommended_songs if song not in playlist]

        return recommended_songs[:N]
