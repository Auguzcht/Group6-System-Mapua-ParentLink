import os, requests

class AppConfig:
    def __init__(self):
        self.APPLICATION_KEY = os.getenv('APPLICATION_KEY')
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.APPLICATION_ID = os.getenv('APPLICATION_ID')
        self.OAUTH_TOKEN_URL = 'https://malayanmindanao-test.blackboard.com/learn/api/public/v1/oauth2/token'

    def init_app(self, app):
        app.config['APPLICATION_KEY'] = self.APPLICATION_KEY
        app.config['SECRET_KEY'] = self.SECRET_KEY
        app.config['APPLICATION_ID'] = self.APPLICATION_ID
        app.config['OAUTH_TOKEN_URL'] = self.OAUTH_TOKEN_URL

app_config = AppConfig()
def get_access_token():
    try:
        response = requests.post(
            app_config.OAUTH_TOKEN_URL,
            data={'grant_type': 'client_credentials'},
            auth=(app_config.APPLICATION_KEY, app_config.SECRET_KEY),
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            print(f"Failed to get access token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching access token: {e}")
        return None