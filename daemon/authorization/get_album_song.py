import urllib.request
import json

class Get_album_song:
    
    

    def __init__(self,access_token):
        """
            Get Spotify catalog information for a single album.
        """
        self.headers = {
            "Authorization": "Bearer " + access_token
        } 
# }
    def get_album_song(self,album_id):
        """
            Parameters:
        """
        self.album_song_url = "https://api.spotify.com/v1/albums/" + album_id
        req = urllib.request.Request(url = self.album_song_url,headers=self.headers)
        page = urllib.request.urlopen(req)
        contentBytes = page.read()
        contentBytes = contentBytes.decode("utf-8")
        self.album_song_json = []
        d1 =  json.loads(contentBytes )

        for i,t in enumerate(d1["tracks"]["items"]):
            json_value = {"name :" : t["name"],
            "track_number :" : t["track_number"],
            "id :" : t["id"],
            "type :" : t["type"],
            }
            self.album_song_json.append(json_value)
        self.album_information_json = {"artise_copyrights" : d1["copyrights"],
        "artise_external_urls" : d1["external_urls"],
        "artise_images" : d1["images"],
        "artise_name" : d1["name"],
        "artise_release_date" : d1["release_date"],
        "artise_external_urls" : d1["external_urls"],
        "artise_album_song" : self.album_song_json}
        
        return self.album_information_json