import json, requests, time
from eCorda_code.token_api import get_headers
from application.server.main.logger import get_logger
from retry import retry

logger = get_logger(__name__)

@retry(delay=50, tries=25)
def get_page(url):
    r = requests.get(url, headers=get_headers())
    return r.json()['data']

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
            try:
                result += get_page(url1)
                logger.debug(f'{page}', end=',')
            except:
                logger.debug(f"problem : {base}, end request {time.strftime('%H:%M:%S')}")   

        logger.debug(f"last page:{page+1}, last page expected:{page_max}, end request {time.strftime('%H:%M:%S')}") 
        return result
