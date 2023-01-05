import json, requests, time
from retry import retry
from ecorda.token_api import get_headers
from utils.logger import get_logger

logger = get_logger(__name__)

PAGE_SIZE=500

@retry(delay=50, tries=25)
def get_page(url):
    r = requests.get(url, headers=get_headers())
    return r.json()['data']

def base_api(base=None, framework=None, url_ue=None):
    SIZE=str(PAGE_SIZE)
    url = url_ue + base + "?framework=" + framework + "&size=" + SIZE
    r = requests.get(url, headers=get_headers())

    tot_records = r.json().get("metadata").get("totalRecords")
    page_max = r.json().get("metadata").get("lastPage")
    last_page_size = tot_records % PAGE_SIZE
    
    result = []
    if r.json().get("metadata").get("totalRecords") == 0:
        result = []
        logger.debug(f'***{base} Empty***')
    if tot_records <= 500:
        result = []
        url1 = url_ue + base + "?framework=" + framework + "&page=1&size=" + str(tot_records)
        time.sleep(0.2)
        result += get_page(url1)
        logger.debug('1') 
    else:
        logger.debug(f'***{base} -> totalRecords:{r.json().get("metadata").get("totalRecords")}, totalPage:{page_max}, start request:{time.strftime("%H:%M:%S")}')
        for page in range(1, page_max):
            url1 = url_ue + base + "?framework=" + framework + "&page=" + str(page) + "&size=" + SIZE
            time.sleep(0.2)
            result += get_page(url1)
            logger.debug(f'{page}') 
        ### Get last page with last_page_size
        last_page_url = url_ue + base + "?framework=" + framework + "&page=" + str(page_max + 1) + "&size=" + str(last_page_size)
        time.sleep(0.2)
        result += get_page(last_page_url)
        logger.debug(f'Dernière page: {page_max}') 
        logger.debug(f'Total records: {tot_records} // Nombre de résultats: {len(result)}') 

        logger.debug(f"***{page_max-page} pages de différence, end request {time.strftime('%H:%M:%S')}***") 
    return result
