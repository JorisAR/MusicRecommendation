import json

def load_json_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def main():
    file_path = "challenge_set.json"  # Replace 'your_file_path.json' with the actual file path
    data = load_json_file(file_path)

    print("Date:", data["date"])
    print("Version:", data["version"])
    print("Playlists:")
    for playlist in data["playlists"]:
        # print("\tName:", playlist["name"])
        print("\tNumber of Holdouts:", playlist["num_holdouts"])
        print("\tPID:", playlist["pid"])
        print("\tNumber of Tracks:", playlist["num_tracks"])
        print("\tNumber of Samples:", playlist["num_samples"])
        print()

    print(data)

if __name__ == "__main__":
    main()
