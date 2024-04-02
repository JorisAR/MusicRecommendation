import json
import time
import os

from user_based_filter import UserBasedFilter
from item_based_filter import ItemBasedFilter
import pandas as pd
from evaluation_metrics import EvaluationMetrics
import concurrent.futures


def load_csv_file(file_path, limit=50000):
    return pd.read_csv(file_path, nrows=limit)


def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def load_json_folder(directory, limit):
    combined_data = {"playlists": []}
    for filename in os.listdir(directory):
        if len(combined_data["playlists"]) >= limit:
            break
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            data = load_json_file(filepath)
            combined_data["playlists"].extend(data["playlists"])
    return combined_data


def evaluate_playlist(playlist_data, N, user_based_filter, item_based_filter):
    # Extract tracks from the playlist data
    playlist_tracks = [track["track_uri"] for track in playlist_data["tracks"]]

    # Subtract the first N tracks from the playlist
    input_playlist = playlist_tracks[:N]
    playlist_tracks = playlist_tracks[N:]

    # Make recommendations using user-based and item-based filters
    user_recommendations = user_based_filter.recommend_songs(input_playlist, 40)
    item_recommendations = item_based_filter.recommend_songs(input_playlist, 40)

    # Evaluate user-based recommendations
    user_based_precision = EvaluationMetrics.precision(playlist_tracks, user_recommendations)
    user_based_recall = EvaluationMetrics.recall(playlist_tracks, user_recommendations)
    user_based_f1_score = EvaluationMetrics.f1_score(playlist_tracks, user_recommendations)
    user_based_map = EvaluationMetrics.average_precision(playlist_tracks, user_recommendations)
    user_based_mrr = EvaluationMetrics.mean_reciprocal_rank([playlist_tracks], [user_recommendations])

    # Evaluate item-based recommendations
    item_based_precision = EvaluationMetrics.precision(playlist_tracks, item_recommendations)
    item_based_recall = EvaluationMetrics.recall(playlist_tracks, item_recommendations)
    item_based_f1_score = EvaluationMetrics.f1_score(playlist_tracks, item_recommendations)
    item_based_map = EvaluationMetrics.average_precision(playlist_tracks, item_recommendations)
    item_based_mrr = EvaluationMetrics.mean_reciprocal_rank(playlist_tracks, item_recommendations)

    return {
        "Playlist Name": playlist_data["name"],
        "User-based Precision": user_based_precision,
        "User-based Recall": user_based_recall,
        "User-based F1 Score": user_based_f1_score,
        "User-based MAP": user_based_map,
        "User-based MRR": user_based_mrr,
        "Item-based Precision": item_based_precision,
        "Item-based Recall": item_based_recall,
        "Item-based F1 Score": item_based_f1_score,
        "Item-based MAP": item_based_map,
        "Item-based MRR": item_based_mrr
    }


def run_test_threaded(test_count=100, playlist_sample_size=5):
    data_rows = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(evaluate_playlist, playlist_data, playlist_sample_size, user_based_filter,
                                   item_based_filter)
                   for playlist_data in testing_playlist_data["playlists"][:test_count]]

        for future in concurrent.futures.as_completed(futures):
            data_rows.append(future.result())

    elapsed_time = time.time() - start_time
    print(f"Multithreaded execution time: {elapsed_time:.4f} seconds")

    scores_df = pd.DataFrame(data_rows)
    return scores_df


def run_test(test_count=100, playlist_sample_size=5):
    data_rows = []
    start_time = time.time()

    for playlist_data in testing_playlist_data["playlists"][:test_count]:
        result = evaluate_playlist(playlist_data, playlist_sample_size, user_based_filter, item_based_filter)
        data_rows.append(result)

    elapsed_time = time.time() - start_time
    print(f"Sequential execution time: {elapsed_time:.4f} seconds")

    scores_df = pd.DataFrame(data_rows)
    return scores_df


def dataframe_mean(dataframe):
    average_scores = dataframe.drop(columns=["Playlist Name"]).mean()
    return average_scores


def main():
    # set the number of tests, and the amount of songs sampled the playlist as input for the filters.
    n_tests = 5416
    n_tests = 1
    n_samples = 10
    scores_df = run_test(n_tests, n_samples)

    # print(dataframe_mean(scores_df))


if __name__ == '__main__':
    playlist_file_path = "data/challenge_set.json"
    playlist_folder_path = "data/completePlaylists"
    song_file_path = "data/dataset_90k.csv"
    testing_playlist_file_path = "final_data/TestSet.json"

    # playlist_data = load_json_file(playlist_file_path)
    limit = 1000
    playlist_data = load_json_folder(playlist_folder_path, limit=limit)
    song_data = load_csv_file(song_file_path, limit=limit)
    testing_playlist_data = load_json_file(testing_playlist_file_path)

    user_based_filter = UserBasedFilter(playlist_data)
    item_based_filter = ItemBasedFilter(song_data)
    # main()

    print(f"SongDataShape:  {song_data.shape}")
    playlists = playlist_data["playlists"]
    print(f"PlaylistDataShape:  {len(playlists)}")

    start_time = time.time()
    item_based_filter.recommend_songs(["5aDpULK8MbJmHl42kR5KNI", "6ivkBaxvclVhwZDE2uwldj", "34dnNAUoIPcwnK0RtVMBWZ", "6IF2P93LkyW4GqDQu1yS7H", "38YgZVHPWOWsKrsCXz6JyP"], 40)
    elapsed_time = time.time() - start_time
    print(f"Item based execution time: {elapsed_time:.4f} seconds")

    # start_time = time.time()
    # user_based_filter.recommend_songs(["4rHZZAmHpZrA3iH5zx8frV", "1NpW5kyvO4XrNJ3rnfcNy3", "2GcSQZ1TmuRvqp3r4fWOZO", "6nHqns54LRqDNjeqKDF3v8", "1XGmzt0PVuFgQYYnV2It7A"], 40)
    # elapsed_time = time.time() - start_time
    # print(f"User based execution time: {elapsed_time:.4f} seconds")
