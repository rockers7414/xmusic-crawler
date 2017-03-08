# use token to get new release list
import urllib.request
import json

class Get_new_release:
    
    new_releases_json = []
    def __init__(self,access_token):
        """
            Get a list of new album releases featured in Spotify (shown, for example, on a Spotify player’s “Browse” tab).
        """
        self.headers = {
            "Authorization": "Bearer " + access_token
        } 
# }
    def get_new_list(self,count):
        """
            Parameters:
                count: Number of new song. You will get twenty times as number.
        """
        num = 0
        while num < count :
            self.new_release_url = "https://api.spotify.com/v1/browse/new-releases?limit=20&offset=" + str(num*20)
            req = urllib.request.Request(url = self.new_release_url,headers=self.headers)
            page = urllib.request.urlopen(req)
            contentBytes = page.read()
            contentBytes = contentBytes.decode("utf-8")
            d1 =  json.loads(contentBytes )
            num +=1
    
            i = 0
            while i < len(d1["albums"]["items"]):
                json_value = {"href :" :d1["albums"]["items"][i]["href"],
                "id" :d1["albums"]["items"][i]["id"],
                "name" :d1["albums"]["items"][i]["name"],
                "type" :d1["albums"]["items"][i]["type"],
                "uri" :d1["albums"]["items"][i]["uri"],
                "external_urls" :d1["albums"]["items"][i]["external_urls"]["spotify"],
                "images_small_url" :d1["albums"]["items"][i]["images"][0]["url"],
                "images_medium_url" :d1["albums"]["items"][i]["images"][1]["url"],
                "images_big_url" :d1["albums"]["items"][i]["images"][2]["url"]}
                self.new_releases_json.append(json_value)
                i += 1
#         print(new_releases_json)
        return self.new_releases_json