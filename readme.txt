make sure to have the following files in the data folder - the json and csv files are renamed after downloading them:


challange_set_10k_millionplaylist.json --> download : https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge

dataset_90k.csv --> download : https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset


Download the complete dataset ( https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge/dataset_files ) and put the slices in the data/completedataset folder

Now run load.py

useful data:

- intersected.json is the subset of the million set with [playlistname, [name,[references]]
- csv_filtered is the subset of the 90k dataset with only song information of the songs included in interesected.json

- data/complete_adjusted/
++ mpd.slice.xxx-xxx_adjusted : playlists with length > 10 of songs that are only in csv_filtered
++ /excluded /included : mpd.slice.xxx-xxx_adjusted_{included/excluded}.json included folder is of playlists that are the intersected.json subset, the excluded is where the playlists are not in intersected.json 

