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

    def __init__(self, client_id, client_secret, grant_type = "client_credentials"):
        """
            Constructor
            Parameters:
                client_id - provider by Spotify when register app. (Required)
                cleint_secret - provider by Spotify when register app. (Required)
                grant_type - grant type, set it to “client_credentials”. (Required)
        """
        self.parameter = {
            grant_type : grant_type
        }

        self.authorization = base64.b64encode(client_id + ":" + client_secret)

        self.__authorize()

    def __authorize(self):
        print(self.authorization)

    def test(self):
        print(self.spotify_authorize_url)
        print(self.spotify_authorize_url + "?" + urlencode(self.parameter))
        self.__authorize()

    def test2(self):
        serial_param = urlencode(self.parameter)
        print(serial_param)

    def refresh_token(self):
        pass

    def get_token(self):
        return "token.."


a = Spotify("???", "???")
a.test()
