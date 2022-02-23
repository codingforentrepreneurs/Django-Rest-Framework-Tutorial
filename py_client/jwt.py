# Blog post reference: https://www.codingforentrepreneurs.com/blog/python-jwt-client-django-rest-framework-simplejwt

from dataclasses import dataclass 
import requests
from getpass import getpass
import pathlib 
import json


@dataclass
class JWTClient:
    """
    Use a dataclass decorator
    to simply the class construction
    """
    access:str = None
    refresh:str = None
    # ensure this matches your simplejwt config
    header_type: str = "Bearer"
    # this assumesy ou have DRF running on localhost:8000
    base_endpoint = "http://localhost:8000/api"
    # this file path is insecure
    cred_path: pathlib.Path = pathlib.Path("creds.json")

    def __post_init__(self):
        if self.cred_path.exists(): 
            """
            You have stored creds,
            let's verify them
            and refresh them.
            If that fails,
            restart login process.
            """
            try:
                data = json.loads(self.cred_path.read_text())
            except Exception:
                print("Assuming creds has been tampered with")
                data = None
            if data is None:
                """ 
                Clear stored creds and
                Run login process
                """
                self.clear_tokens()
                self.perform_auth()
            else:
                """
                `creds.json` was not tampered with
                Verify token -> 
                if necessary, Refresh token ->
                if necessary, Run login process
                """
                self.access = data.get('access')
                self.refresh = data.get('refresh')
                token_verified = self.verify_token()
                if not token_verified:
                    """
                    This can mean the token has expired
                    or is invalid. Either way, attempt
                    a refresh.
                    """
                    refreshed = self.perform_refresh()
                    if not refreshed:
                        """
                        This means the token refresh
                        also failed. Run login process
                        """
                        print("invalid data, login again.")
                        self.clear_tokens()
                        self.perform_auth()
        else:
            """
            Run login process
            """
            self.perform_auth()
        
    def get_headers(self, header_type=None):
        """
        Default headers for HTTP requests
        including the JWT token
        """
        _type = header_type or self.header_type
        token = self.access
        if not token:
            return {}
        return {
                "Authorization": f"{_type} {token}"
        }

    def perform_auth(self):
        """
        Simple way to perform authentication
        Without exposing password(s) during the
        collection process.
        """
        endpoint = f"{self.base_endpoint}/token/" 
        username = input("What is your username?\n")
        password = getpass("What is your password?\n")
        r = requests.post(endpoint, json={'username': username, 'password': password}) 
        if r.status_code != 200:
            raise Exception(f"Access not granted: {r.text}")
        print('access granted')
        self.write_creds(r.json())

    def write_creds(self, data:dict):
        """
        Store credentials as a local file
        and update instance with correct
        data.
        """
        if self.cred_path is not None:
            self.access = data.get('access')
            self.refresh = data.get('refresh')
            if self.access and self.refresh:
                self.cred_path.write_text(json.dumps(data))
    
    def verify_token(self):
        """
        Simple method for verifying your
        token data. This method only verifies
        your `access` token. A 200 HTTP status
        means success, anything else means failure.
        """
        data = {
            "token": f"{self.access}"
        }
        endpoint = f"{self.base_endpoint}/token/verify/" 
        r = requests.post(endpoint, json=data)
        return r.status_code == 200
    
    def clear_tokens(self):
        """
        Remove any/all JWT token data
        from instance as well as stored
        creds file.
        """
        self.access = None
        self.refresh = None
        if self.cred_path.exists():
            self.cred_path.unlink()
    
    def perform_refresh(self):
        """
        Refresh the access token by using the correct
        auth headers and the refresh token.
        """
        print("Refreshing token.")
        headers = self.get_headers()
        data = {
            "refresh": f"{self.refresh}"
        }
        endpoint = f"{self.base_endpoint}/token/refresh/" 
        r = requests.post(endpoint, json=data, headers=headers)
        if r.status_code != 200:
            self.clear_tokens()
            return False
        refresh_data = r.json()
        if not 'access' in refresh_data:
            self.clear_tokens()
            return False
        stored_data = {
            'access': refresh_data.get('access'),
            'refresh': self.refresh
        }
        self.write_creds(stored_data)
        return True

    def list(self, endpoint=None, limit=3):
        """
        Here is an actual api call to a DRF
        View that requires our simplejwt Authentication
        Working correctly.
        """
        headers = self.get_headers()
        if endpoint is None or self.base_endpoint not in str(endpoint):
            endpoint = f"{self.base_endpoint}/products/?limit={limit}" 
        r = requests.get(endpoint, headers=headers) 
        if r.status_code != 200:
            raise Exception(f"Request not complete {r.text}")
        data = r.json()
        return data


if __name__ == "__main__":
    """
    Here's Simple example of how to use our client above.
    """
    
    # this will either prompt a login process
    # or just run with current stored data
    client = JWTClient() 

    # simple instance method to perform an HTTP
    # request to our /api/products/ endpoint
    lookup_1_data = client.list(limit=5)
    # We used pagination at our endpoint so we have:
    results = lookup_1_data.get('results')
    next_url = lookup_1_data.get('next')
    print("First lookup result length", len(results))
    if next_url:
        lookup_2_data = client.list(endpoint=next_url)
        results += lookup_2_data.get('results')
        print("Second lookup result length", len(results))