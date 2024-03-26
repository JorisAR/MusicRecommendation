import json
import pandas as pd
import os

def load_json(file_path):
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



def load_90k_set(datapath):
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


def filter_playlists_with_tracks(json_data, output_file, playlist_length_minimum=1, info=None):
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
        if len(playlist["tracks"]) < playlist_length_minimum:
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
            # "num_holdouts": playlist["num_holdouts"],
            "pid": playlist["pid"],
            "num_tracks": playlist["num_tracks"],
            "tracks": filtered_tracks
        }
        filtered_playlists.append(filtered_playlist)

   # Construct the filtered data based on the presence of info dictionary
    if info is not None:
        # If info is provided, use it to construct the filtered data
        filtered_data = {"info": info, "playlists": filtered_playlists}
    else:
        # Otherwise, use the original structure
        filtered_data = {"date": json_data["date"], "version": json_data["version"], "playlists": filtered_playlists}

    # Dump the filtered data
    with open(output_file, 'w') as f:
        json.dump(filtered_data, f, indent=4)
        
    print("Filtered data saved to:", output_file)


def match_data(json_data, csv_data, output_file, limit_progress=True, info=None, playlist_length_minimum=1):
    """
    Match tracks from the JSON data with those in the CSV data.

    Args:
    - json_data (dict): JSON data containing playlists and tracks.
    - csv_data (pandas.DataFrame): CSV data containing track information.
    - output_file (str): Path to save the matched data.
    - limit_progress (bool): Whether to limit the progress or not.
    - info (dict): Additional information to include in the filtered data.
    - playlist_length_minimum (int): Minimum length of playlists to consider.

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
        # Initialize filtered tracks for the current playlist
        filtered_tracks = []

        # Iterate over the tracks in the playlist
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
        
        # If there are tracks in the playlist after filtering
        if len(filtered_tracks) >= playlist_length_minimum:
            # Append the playlist with filtered tracks
            filtered_playlist = {
                "name": playlist.get("name", ""),
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

    # Construct the filtered data based on the presence of info dictionary
    if info is not None:
        # If info is provided, use it to construct the filtered data
        filtered_json_data = {"info": info, "playlists": filtered_playlists}
    else:
        # Otherwise, use the original structure
        filtered_json_data = {"date": json_data["date"], "version": json_data["version"], "playlists": filtered_playlists}

    # Write matched data to the output file
    with open(output_file, 'w') as f:
        json.dump(filtered_json_data, f, indent=4)

    print("Matched data saved to:", output_file)



def count_playlists(json_data):
    """
    Count the number of playlists in the JSON data.

    Args:
    - json_data (dict): The JSON data containing playlists.

    Returns:
    - int: The number of playlists.
    """
    if "playlists" in json_data:
        return len(json_data["playlists"])
    else:
        return 0



def remove_rows_not_in_list(csv_data, index_in_csv_list, output_file):
    """
    Remove rows from the CSV DataFrame that are not present in the given list of index_in_csv numbers and write to a new CSV file.

    Args:
    - csv_data (DataFrame): DataFrame containing the CSV data.
    - index_in_csv_list (list): List of index_in_csv numbers to keep.
    - output_file (str): Path to the output CSV file.

    Returns:
    - None
    """
    filtered_csv_data = csv_data[csv_data.index.isin(index_in_csv_list)]
    filtered_csv_data.to_csv(output_file, index=False)
    print("Filtered CSV data saved to:", output_file)

def get_index_in_csv_list(json_data):
    """
    Get a list of index_in_csv numbers from the JSON data.

    Args:
    - json_data (dict): JSON data containing playlists and tracks.

    Returns:
    - index_in_csv_list (list): List of index_in_csv numbers.
    """
    index_in_csv_list = []

    # Iterate over the playlists in the JSON data
    for playlist in json_data["playlists"]:
        for track in playlist["tracks"]:
            index_in_csv = track.get("index_in_csv")
            if index_in_csv is not None:
                index_in_csv_list.append(index_in_csv)

    return index_in_csv_list

def separate_playlists_by_name(json_final, jsons_folder):
    """
    Separate playlists by name based on whether they are present in json_final.

    Args:
    - json_final (dict): Loaded JSON data containing playlists.
    - jsons_folder (str): Path to the folder containing JSON files of complete dataset.

    Returns:
    - None
    """
    included_folder = "data/complete_adjusted/included"
    output_folder = "data/complete_adjusted/excluded"

    # Ensure the output folders exist
    os.makedirs(included_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over the JSON files in the folder
    for filename in os.listdir(jsons_folder):
        if filename.endswith(".json"):
            json_file_path = os.path.join(jsons_folder, filename)
            print("Processing JSON file:", json_file_path)

            # Load the JSON data
            json_data = load_json(json_file_path)

            # Extract base name of the JSON file without extension
            base_name = os.path.splitext(filename)[0]

            # Initialize lists to store included and excluded playlists
            included_playlists = []
            excluded_playlists = []

            # Iterate over the playlists in the JSON data
            for playlist in json_data["playlists"]:
                playlist_name = playlist.get("name", "")
                if any(item["name"] == playlist_name for item in json_final["playlists"]):
                    included_playlists.append(playlist)
                else:
                    excluded_playlists.append(playlist)

            # Save included playlists to the included folder
            included_output_file = os.path.join(included_folder, f"{base_name}_included.json")
            with open(included_output_file, 'w') as f:
                json.dump({"playlists": included_playlists}, f, indent=4)
            print("Included playlists saved to:", included_output_file)

            # Save excluded playlists to the output folder
            output_output_file = os.path.join(output_folder, f"{base_name}_excluded.json")
            with open(output_output_file, 'w') as f:
                json.dump({"playlists": excluded_playlists}, f, indent=4)
            print("Excluded playlists saved to:", output_output_file)

            print("SPLIT incl, excl:", len(included_playlists), len(excluded_playlists))

            print()  # Add an empty line for better readability



createEvalSet = True
dataslices_max = 10 # increase if you want more data

def main():
    if not os.path.exists("data/intersected.json"):
        print("Creating test dataset")

        print("loading data")
        json_data = load_json("data/challenge_set_10k_millionplaylist.json")
        csv_data = load_90k_set("data/dataset_90k.csv")

        # Filter playlists with zero tracks and save to a file
        filter_playlists_with_tracks(json_data, "data/filtered_data.json")
        
        # Load the filtered JSON data
        json_data_filtered = load_json("data/filtered_data.json")

        # Match the filtered JSON data with the CSV data and save to a file
        match_data(json_data_filtered, csv_data, "data/intersected.json", False)

        # # Count the number of datasets found in the final JSON
        json_final = load_json("data/intersected.json")
        print("amount of datasets found:", count_playlists(json_final))

        remove_rows_not_in_list(csv_data, get_index_in_csv_list(json_final), "data/csv_filtered.csv")

    if createEvalSet:

        print("Creating evaluation dataset")

        # Load the CSV data
        print("Loading CSV data")
        csv_data = load_90k_set("data/csv_filtered.csv")

        # Specify the folder containing JSON files
        jsons_folder = "data/completedataset"

        slice = 0

        # Iterate over the JSON files in the folder
        for filename in os.listdir(jsons_folder):
            if filename.endswith(".json"):
                json_file_path = os.path.join(jsons_folder, filename)
                print("\nLoading JSON file:", json_file_path)

                # Load the JSON data
                json_data = load_json(json_file_path)

                # Extract base name of the JSON file without extension
                base_name = os.path.splitext(filename)[0]

                # Match the filtered JSON data with the CSV data and save to a file
                output_file = f"data/complete_adjusted/{base_name}_adjusted.json"

                # Filter playlists with zero tracks and save to a file
                filter_playlists_with_tracks(json_data, output_file, playlist_length_minimum=10, info=True)
                
                # # Load the filtered JSON data
                json_data_filtered = load_json(output_file)

                # # Match the filtered JSON data with the CSV data and save to a file
                match_data(json_data_filtered, csv_data, output_file, False, info=True, playlist_length_minimum=10)

                json_data_filtered = load_json(output_file)

                slice += 1

                if slice == dataslices_max:
                    print("STOP loading, want more?: adjust the dataslices var")
                    break

        print("split datasets into two")
        # load test json data
        print("load intersected test set")
        json_final = load_json("data/intersected.json")
        json_filtered = "data/complete_adjusted"
        # split into two sets   
        separate_playlists_by_name(json_final, json_filtered)


if __name__ == "__main__":
    main()
