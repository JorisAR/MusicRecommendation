import json
import pandas as pd

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def load_million_set(file_path="data/challenge_set_10k_millionplaylist.json"):
    # https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/data
    # https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files
    data = load_json_file(file_path)

    # print("Date:", data["date"])
    # print("Version:", data["version"])
    # print("Playlists:")
    # for playlist in data["playlists"]:
        # print("\tName:", playlist["name"])
        # print("\tNumber of Holdouts:", playlist["num_holdouts"])
        # print("\tPID:", playlist["pid"])
        # print("\tNumber of Tracks:", playlist["num_tracks"])
        # print("\tNumber of Samples:", playlist["num_samples"])
        # print()

    # print(data)
    return data

def load_90k_set(datapath="data/dataset_90k.csv"):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(datapath)

    # Display the DataFrame
    # print(df)
    return df

import json

def match_data(json_data, csv_data, output_file):
    print("Matching data")

    matched_data = []

    # Create a set to store track IDs from the CSV data for faster lookup
    csv_track_ids = set(csv_data['track_id'])

    # Initialize variables to track progress and matches
    total_matches = 0

    # Iterate over the playlists in the JSON data
    for index, playlist in enumerate(json_data["playlists"]):
        filtered_tracks = []
        for track in playlist["tracks"]:
            track_id = track["track_uri"].split(":")[-1]  # Extract track ID
            if track_id in csv_track_ids:
                # Track ID found in CSV data, add it to matched data
                csv_index = csv_data[csv_data['track_id'] == track_id].index[0]  # Get index in CSV
                matched_data.append({
                    "pos": track["pos"],
                    "track_uri": track_id,
                    "index_in_csv": int(csv_index),  # Convert int64 to Python int
                })
                track["index_in_csv"] = int(csv_index)  # Add index to track metadata
                filtered_tracks.append(track)
                total_matches += 1
        playlist["tracks"] = filtered_tracks

        # Update progress bar
        progress = (index + 1) / len(json_data["playlists"]) * 100
        print(f"Progress: {progress:.2f}%, Matches found: {total_matches}", end='\r')
        
        # Break if progress > 1
        if progress > 1:
            break

    print("\nTotal matches found:", total_matches)

    # Write matched data to the output file
    with open(output_file, 'w') as f:
        json.dump(json_data, f, indent=4)

    print("Matched data saved to:", output_file)





def filter_playlists_with_tracks(json_data, output_file):
    print("Filter playlists with zero tracks and remove unused fields")

    filtered_playlists = []

    for playlist in json_data["playlists"]:
        # Filter out playlists with zero tracks
        if len(playlist["tracks"]) == 0:
            continue

        filtered_tracks = []
        for track in playlist["tracks"]:
            filtered_track = {"pos": track["pos"], "track_uri": track["track_uri"]}
            filtered_tracks.append(filtered_track)

        # Append filtered playlist along with other fields
        filtered_playlist = {
            "name": playlist.get("name", ""),
            "num_holdouts": playlist["num_holdouts"],
            "pid": playlist["pid"],
            "num_tracks": playlist["num_tracks"],
            "tracks": filtered_tracks
        }
        filtered_playlists.append(filtered_playlist)

    filtered_data = {"date": json_data["date"], "version": json_data["version"], "playlists": filtered_playlists}

    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=4)

    print("Filtered data saved to:", output_file)





def main():
    print("loading data")
    json_data = load_million_set()
    csv_data = load_90k_set()

    filter_playlists_with_tracks(json_data, "data/filtered_data.json")

    
    json_data_filtered = load_million_set("data/filtered_data.json")


    match_data(json_data_filtered, csv_data, "data/interesected.json")


if __name__ == "__main__":
    main()
