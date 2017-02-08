from urllib.parse import urlencode
import requests
import base64


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
            grant_type: grant_type
        }

        user_info_bytes = base64.b64encode((client_id + ":" + client_secret).encode())
        self.user_info_base64 = user_info_bytes.decode()

        self.__authorize()

    def __authorize(self):
        headers = {"Authorization", "Basic " + self.user_info_base64}

        pass

    def display(self):
        print(self.spotify_authorize_url)
        print(self.spotify_authorize_url + "?" + urlencode(self.parameter))
        print(self.user_info_base64)

    def get_token(self):
        return "token.."


a = Spotify("??", "??")
a.display()
