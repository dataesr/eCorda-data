import requests, json, os, urllib3

client_id = os.getenv('ECORDA_CLIENT_ID')
client_secret = os.getenv('ECORDA_CLIENT_SECRET')

def get_token():
    token_url = "https://api.tech.ec.europa.eu/token"
    data = {'grant_type': 'client_credentials'}
    access_token_response = requests.post(token_url, data=data, verify=False, allow_redirects=False, auth=(client_id, client_secret))
    tokens = json.loads(access_token_response.text)
    return tokens

def expire_token(token_lib):

    revoke_url = 'https://api.tech.ec.europa.eu/revoke'
    
    data = {"client_id": client_id,
            "client_secret": client_secret,
            "token": token_lib}
    token_revoke = requests.post(revoke_url, data=data, verify=False, allow_redirects=False)

def get_headers():
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    tokens = get_token()

    try:
        if tokens['expires_in'] > 0:
            api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
            return api_call_headers
    except:
        expire_token(tokens['access_token'])
        tokens = get_token()
        api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
        return api_call_headers
