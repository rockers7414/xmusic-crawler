import configparser
from spotify import Spotify
from get_new_release import Get_new_release
from get_album_song import Get_album_song

# Read config.cfg to get Client_ID and Client_Secret
config = configparser.ConfigParser()
config.read('../config.cfg')
Client_ID = config.get('Spotify_Parameters' ,'Client_ID')
Client_Secret = config.get('Spotify_Parameters','Client_Secret' )

# Get access token value
s = Spotify(Client_ID,Client_Secret)
access_token = s.get_token()


new_release = Get_new_release(access_token)
album_song = Get_album_song(access_token)

# Get new release name. 
# You will get twenty times as number
new_count = 1
album_information_list = []
new_list = new_release.get_new_list(new_count)

# use new release name to get artists's name
new_list_count = 0

# artists_name_list: check artists if already exist
new_release_imformation = []
# album_information_list is new release album and album's songs
while new_list_count < len(new_list):
    album_information_list.append(album_song.get_album_song(new_list[new_list_count]["id"]))
    new_list_count += 1
    
