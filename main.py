import json
from user_based_filter import UserBasedFilter
from item_based_filter import ItemBasedFilter
import pandas as pd
from evaluation_metrics import EvaluationMetrics

def load_csv_file(file_path):
    return pd.read_csv(file_path, nrows=50000)

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def main():
    playlist_file_path = "final_data/EvalSet.json"
    
    song_file_path = "final_data/csv_filtered.csv"
    
    playlist_data = load_json_file(playlist_file_path)
    song_data = load_csv_file(song_file_path)
    
    testing_playlist_file_path = "final_data/TestSet.json"
    testing_playlist_data = load_json_file(testing_playlist_file_path)

    user_based_filter = UserBasedFilter(playlist_data)
    item_based_filter = ItemBasedFilter(song_data)
    


    # playlist = ["3W3KtDwAIg3mAruSpnfG3Q", "0zREtnLmVnt8KUJZZbSdla",
    #             "4rHZZAmHpZrA3iH5zx8frV", "3MAgQuClHcAV8E9CbeBS6f", "4ybvIvKdvfkdsIYYAiaTiG", "5vjLSffimiIP26QG5WcN2K"]

    # user_based_filter.recommend_songs(playlist, 10)
    # item_based_filter.recommend_songs(playlist, 10)
    
    # # Extract tracks from the testing playlist
    # playlists = [track["track_uri"] for track in testing_playlist_data["playlists"][0]["tracks"]]

    # # Subtract the first 10 numbers from the playlist
    # playlist = playlists[10:]

    # # Make recommendations using user-based and item-based filters
    # user_recommendations = user_based_filter.recommend_songs(playlist, 40)
    # item_recommendations = item_based_filter.recommend_songs(playlist, 40)

    # print(type(user_recommendations))
    # print(type(item_recommendations))
    
    # user_based_precision = EvaluationMetrics.precision(playlists, user_recommendations)
    # user_based_recall = EvaluationMetrics.recall(playlists, user_recommendations)
    # user_based_f1_score = EvaluationMetrics.f1_score(playlists, user_recommendations)
    # user_based_map = EvaluationMetrics.average_precision(playlists, user_recommendations)
    # user_based_mrr = EvaluationMetrics.mean_reciprocal_rank([playlists], [user_recommendations])
    
    # item_based_precision = EvaluationMetrics.precision(playlists, item_recommendations)
    # item_based_recall = EvaluationMetrics.recall(playlists, item_recommendations)
    # item_based_f1_score = EvaluationMetrics.f1_score(playlists, item_recommendations)
    # item_based_map = EvaluationMetrics.average_precision(playlists, item_recommendations)

    
    # print("User-based Precision:", user_based_precision)
    # print("User-based Recall:", user_based_recall)
    # print("User-based F1 Score:", user_based_f1_score)
    # print("User-based MAP:", user_based_map)
    # print("User-based MRR:", user_based_mrr)
    
    # print("Item-based Precision:", item_based_precision)
    # print("Item-based Recall:", item_based_recall)
    # print("Item-based F1 Score:", item_based_f1_score)
    # print("Item-based MAP:", item_based_map)
   

    data_rows = []

    for playlist_data in testing_playlist_data["playlists"][:200]:
        # Extract tracks from the playlist data
        playlist_tracks = [track["track_uri"] for track in playlist_data["tracks"]]
        
        # Subtract the first 10 tracks from the playlist
        playlist = playlist_tracks[10:]
        
        # Make recommendations using user-based and item-based filters
        user_recommendations = user_based_filter.recommend_songs(playlist, 40)
        item_recommendations = item_based_filter.recommend_songs(playlist, 40)
        
        # Evaluate user-based recommendations
        user_based_precision = EvaluationMetrics.precision(playlist_tracks, user_recommendations)
        user_based_recall = EvaluationMetrics.recall(playlist_tracks, user_recommendations)
        user_based_f1_score = EvaluationMetrics.f1_score(playlist_tracks, user_recommendations)
        user_based_map = EvaluationMetrics.average_precision(playlist_tracks, user_recommendations)
        user_based_mrr = EvaluationMetrics.mean_reciprocal_rank([playlist_tracks], [user_recommendations])
        
        # # Evaluate item-based recommendations
        # item_based_precision = EvaluationMetrics.precision(playlist_tracks, item_recommendations)
        # item_based_recall = EvaluationMetrics.recall(playlist_tracks, item_recommendations)
        # item_based_f1_score = EvaluationMetrics.f1_score(playlist_tracks, item_recommendations)
        # item_based_map = EvaluationMetrics.average_precision(playlist_tracks, item_recommendations)
        
        # Append scores to the list
        data_rows.append({
            "Playlist Name": playlist_data["name"],
            "User-based Precision": user_based_precision,
            "User-based Recall": user_based_recall,
            "User-based F1 Score": user_based_f1_score,
            "User-based MAP": user_based_map,
            "User-based MRR": user_based_mrr,
            # "Item-based Precision": item_based_precision,
            # "Item-based Recall": item_based_recall,
            # "Item-based F1 Score": item_based_f1_score,
            # "Item-based MAP": item_based_map
        })

        # Create a DataFrame from the list of dictionaries
    scores_df = pd.DataFrame(data_rows)
    print(scores_df)


if __name__ == '__main__':
    main()
