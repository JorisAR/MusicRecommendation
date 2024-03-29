from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

class ItemBasedFilter:
    data = ""

    def __init__(self, data):
        self.data = data

    def recommend_songs(self, playlist, N):
        data = self.data[~self.data['track_id'].isin(playlist)]

        features = ['danceability', 'explicit', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness',
                    'liveness', 'valence']
        X = data[features]

        # Apply PCA and transform the data
        pca = PCA(n_components=3)
        X_pca = pca.fit_transform(X)

        sim_matrix = cosine_similarity(X_pca, X_pca)

        indices = [self.data.index[self.data['track_id'] == id][0] for id in playlist if
                   id in self.data['track_id'].values]

        if not indices:
            print("None of the songs in the playlist are in the data.")
            return

        mean_sim_scores = sim_matrix[indices].mean(axis=0)

        top_indices = mean_sim_scores.argsort()[-N:][::-1]

        recommended_songs = self.data.iloc[top_indices]

        #print(f"Recommended songs: {recommended_songs['track_id'].tolist()}")
        recommended_songs = recommended_songs['track_id'].tolist()

        return recommended_songs
