import json, requests, time, pandas as pd
from ecorda.token_api import get_headers

def NewDate(framework, url_ue):
    url = url_ue+"extractionDate"
    r = requests.get(url, headers=get_headers())   
    for i in r.json()['data']:
        if i['framework'] == framework:
            return i['extraction_date']
