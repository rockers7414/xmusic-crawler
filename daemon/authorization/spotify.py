from io import BytesIO
from urllib.parse import urlencode
import pycurl
import base64
import json


class Spotify:

    """
        To make the API fast for everybody, rate limits apply.
        Unauthenticated requests are processed at the lowest rate limit.
        Authenticated requests with a valid access token benefit from higher rate limits
    """

    # Spotify Authorize API
    spotify_authorize_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, grant_type="client_credentials"):
        """
            Constructor
            Parameters:
                client_id - provider by Spotify when register app. (Required)
                cleint_secret - provider by Spotify when register app. (Required)
                grant_type - grant type, set it to “client_credentials”. (Required)
        """
        self.parameter = {
            "grant_type": grant_type
        }

        user_info_bytes = base64.b64encode(
            (client_id + ":" + client_secret).encode())
        self.user_info_base64 = user_info_bytes.decode()

        self.__authorize()

    def __authorize(self):
        headers = ["Authorization: Basic " + self.user_info_base64]
        post_field = urlencode(self.parameter)

        buf = BytesIO()

        client = pycurl.Curl()
        client.setopt(client.URL, self.spotify_authorize_url)
        client.setopt(client.HTTPHEADER, headers)
        client.setopt(client.POSTFIELDS, post_field)
        client.setopt(client.WRITEFUNCTION, buf.write)
        client.setopt(pycurl.SSL_VERIFYPEER, 0)
        client.perform()
        client.close()

        self.response = json.loads(buf.getvalue().decode())
        self.access_token = self.response.get("access_token")

    def get_token(self):
        self.__authorize()
        return self.access_token
