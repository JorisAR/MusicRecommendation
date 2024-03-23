import json
import pandas as pd

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def load_million_set():
    # https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset/data
    # https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files
    file_path = "data/challenge_set_10k_millionplaylist.json"  
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

def load_90k_set():
    # Load the CSV file into a DataFrame
    df = pd.read_csv("data/dataset_90k.csv")

    # Display the DataFrame
    # print(df)
    return df

def match_data(json_data, csv_data):
    print("Matching data")

    total_playlists = len(json_data['playlists'])
    total_matches = 0

    for index, row in csv_data.iterrows():
        track_id = row['track_id']
        track_uri = "spotify:track:" + track_id
        found_match = False
        
        # Check if track_uri exists in the JSON data
        for playlist in json_data["playlists"]:
            for track in playlist["tracks"]:
                if track_uri == track["track_uri"]:
                    total_matches += 1
                    found_match = True
                    break
            if found_match:
                break

        # Update progress bar
        progress = (index + 1) / len(csv_data) * 100
        print(f"Progress: {progress:.2f}%, Matches found: {total_matches}\r", end='')

    print("\nTotal matches found:", total_matches)



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
    print("loaded data")

    filter_playlists_with_tracks(json_data, "data/filtered_data.json")

    

    # match_data(json_data,csv_data)


if __name__ == "__main__":
    main()
