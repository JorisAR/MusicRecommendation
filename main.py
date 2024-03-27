import json
from user_based_filter import UserBasedFilter
from item_based_filter import ItemBasedFilter
from evaluation_metrics import EvaluationMetrics
import pandas as pd

def load_csv_file(file_path):
    return pd.read_csv(file_path, nrows=50000)

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def main():
    playlist_file_path = "data/intersected.json"
    song_file_path = "data/csv_filtered.csv"

    playlist_data = load_json_file(playlist_file_path)
    song_data = load_csv_file(song_file_path)

    user_based_filter = UserBasedFilter(playlist_data)
    item_based_filter = ItemBasedFilter(song_data)

    playlist = ["3W3KtDwAIg3mAruSpnfG3Q", "0zREtnLmVnt8KUJZZbSdla",
                "4rHZZAmHpZrA3iH5zx8frV", "3MAgQuClHcAV8E9CbeBS6f", "4ybvIvKdvfkdsIYYAiaTiG", "5vjLSffimiIP26QG5WcN2K"]

    user_recommendations = user_based_filter.recommend_songs(playlist, 10)
    item_recommendations = item_based_filter.recommend_songs(playlist, 10)
    
    user_based_precision = EvaluationMetrics.precision(playlist, user_recommendations)
    user_based_recall = EvaluationMetrics.recall(playlist, user_recommendations)
    user_based_f1_score = EvaluationMetrics.f1_score(playlist, user_recommendations)
    user_based_map = EvaluationMetrics.average_precision(playlist, user_recommendations)
    user_based_mrr = EvaluationMetrics.mean_reciprocal_rank([playlist], [user_recommendations])
    
    item_based_precision = EvaluationMetrics.precision(playlist, item_recommendations)
    item_based_recall = EvaluationMetrics.recall(playlist, item_recommendations)
    item_based_f1_score = EvaluationMetrics.f1_score(playlist, item_recommendations)
    item_based_map = EvaluationMetrics.average_precision(playlist, item_recommendations)

    
    print("User-based Precision:", user_based_precision)
    print("User-based Recall:", user_based_recall)
    print("User-based F1 Score:", user_based_f1_score)
    print("User-based MAP:", user_based_map)
    print("User-based MRR:", user_based_mrr)
    
    print("Item-based Precision:", item_based_precision)
    print("Item-based Recall:", item_based_recall)
    print("Item-based F1 Score:", item_based_f1_score)
    print("Item-based MAP:", item_based_map)

    
    


if __name__ == '__main__':
    main()
