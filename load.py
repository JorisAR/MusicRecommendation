import json
import pandas as pd

def load_json_file(file_path):
    """
    Load JSON data from a file.

    Args:
    - file_path (str): Path to the JSON file.

    Returns:
    - dict: Loaded JSON data.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def load_million_set(file_path="data/challenge_set_10k_millionplaylist.json"):
    """
    Load the million playlist dataset from a JSON file.

    Args:
    - file_path (str): Path to the JSON file.

    Returns:
    - dict: Loaded JSON data.
    """
    data = load_json_file(file_path)
    return data

def load_90k_set(datapath="data/dataset_90k.csv"):
    """
    Load the 90k dataset from a CSV file.

    Args:
    - datapath (str): Path to the CSV file.

    Returns:
    - pandas.DataFrame: Loaded CSV data as a DataFrame.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(datapath)
    return df


def filter_playlists_with_tracks(json_data, output_file):
    """
    Filter out playlists with zero tracks and remove unused fields.

    Args:
    - json_data (dict): JSON data containing playlists and tracks.
    - output_file (str): Path to save the filtered data.

    Returns:
    - None
    """
    print("Filter playlists with zero tracks and remove unused fields")

    filtered_playlists = []

    for playlist in json_data["playlists"]:
        # Filter out playlists with zero tracks
        if len(playlist["tracks"]) == 0:
            continue

        filtered_tracks = []
        for track in playlist["tracks"]:
            # Extract track ID from track_uri
            track_id = track["track_uri"].split(":")[-1]
            filtered_track = {"pos": track["pos"], "track_uri": track_id}
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


def match_data(json_data, csv_data, output_file, limit_progress=True):
    """
    Match tracks from the JSON data with those in the CSV data.

    Args:
    - json_data (dict): JSON data containing playlists and tracks.
    - csv_data (pandas.DataFrame): CSV data containing track information.
    - output_file (str): Path to save the matched data.

    Returns:
    - None
    """
    print("Matching data")

    matched_data = []

    # Create a set to store track IDs from the CSV data for faster lookup
    csv_track_ids = set(csv_data['track_id'])

    # Initialize variables to track progress and matches
    total_matches = 0

    # Iterate over the playlists in the JSON data
    filtered_playlists = []
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
        if filtered_tracks:  # If there are tracks in the playlist
            # Append the playlist with filtered tracks
            filtered_playlist = {
                "name": playlist.get("name", ""),
                "num_holdouts": playlist["num_holdouts"],
                "pid": playlist["pid"],
                "num_tracks": playlist["num_tracks"],
                "tracks": filtered_tracks
            }
            filtered_playlists.append(filtered_playlist)

        # Update progress bar
        progress = (index + 1) / len(json_data["playlists"]) * 100
        print(f"Progress: {progress:.2f}%, Matches found: {total_matches}", end='\r')
        
        # Break if progress > 1
        if limit_progress:
            if progress > 1:
                break

    print("\nTotal matches found:", total_matches)

    # Write matched data to the output file
    filtered_json_data = {"date": json_data["date"], "version": json_data["version"], "playlists": filtered_playlists}
    with open(output_file, 'w') as f:
        json.dump(filtered_json_data, f, indent=4)

    print("Matched data saved to:", output_file)



def main():
    print("loading data")
    json_data = load_million_set()
    csv_data = load_90k_set()

    # Filter playlists with zero tracks and save to a file
    filter_playlists_with_tracks(json_data, "data/filtered_data.json")
    
    # Load the filtered JSON data
    json_data_filtered = load_million_set("data/filtered_data.json")

    # Match the filtered JSON data with the CSV data and save to a file
    match_data(json_data_filtered, csv_data, "data/interesected.json", False)




if __name__ == "__main__":
    main()
