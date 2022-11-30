import json, requests, time
from eCorda_code.token_api import get_headers
from application.server.main.logger import get_logger

logger = get_logger(__name__)

def base_api(base=None, framework=None, url_ue=None):
    SIZE=500
    url = url_ue + base + "?framework=" + framework + "&size=" + SIZE
    r = requests.get(url, headers=get_headers())

    if r:
        globals()['tot_records'] = r.json().get("metadata").get("totalRecords")
        page_max = r.json().get("metadata").get("lastPage")

        logger.debug(f'****{base} -> totalRecords:{r.json().get("metadata").get("totalRecords")}, totalPage:{page_max}, start request:{time.strftime("%H:%M:%S")}')

        result = []    
        for page in range(0, page_max + 1): 
            url1 = url_ue + base + "?framework=" + framework + "&page=" + str(page) + "&size=" + SIZE
            time.sleep(0.2)
            r1 = requests.get(url1, headers=get_headers())
            try:
                result += r1.json()['data']
                logger.debug(f'{page}', end=',')
            except:
                logger.debug(f"problem : {base}, end request {time.strftime('%H:%M:%S')}")   

        logger.debug(f"last page:{page+1}, last page expected:{page_max}, end request {time.strftime('%H:%M:%S')}") 
        return result