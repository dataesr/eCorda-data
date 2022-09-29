import json, requests, time, pandas as pd
from eCorda_code.token_api import get_headers

def NewDate(framework, url_ue):
    url = url_ue+"extractionDate"
    r = requests.get(url, headers=get_headers())   
    for i in r.json()['data']:
        if i['framework'] == framework:
            pd.json_normalize(i).to_csv('/eCorda_data/' + "extractionDate.csv", sep=";", index=False, na_rep="", encoding="UTF-8")
            return i['extraction_date']