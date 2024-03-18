import json
import requests
import time
from retry import retry
from ecorda.token_api import get_headers
from utils.logger import get_logger

logger = get_logger(__name__)

PAGE_SIZE = 100


@retry(delay=50, tries=25)
def get_page(url):
    r = requests.get(url, headers=get_headers())
    return r.json()['data']


def base_api(base=None, framework=None, url_ue=None):
    SIZE = str(PAGE_SIZE)
    url = url_ue + base + "?framework=" + framework + "&size=" + SIZE
    r = requests.get(url, headers=get_headers())

    tot_records = r.json().get("metadata").get("totalRecords")
    page_max = r.json().get("metadata").get("lastPage")
    last_page_size = tot_records % PAGE_SIZE

    result = []
    if r.json().get("metadata").get("totalRecords") == 0:
        result = []
        logger.debug(f'***{base} Empty***')
    if tot_records <= PAGE_SIZE:
        result = []
        url1 = url_ue + base + "?framework=" + \
            framework + "&page=1&size=" + str(tot_records)
        time.sleep(0.2)
        result += get_page(url1)
        logger.debug('1')
    else:
        logger.debug(
            f'***{base} -> totalRecords:{r.json().get("metadata").get("totalRecords")}, totalPage:{page_max}, start request:{time.strftime("%H:%M:%S")}')
        for page in range(1, page_max+1):
            url1 = url_ue + base + "?framework=" + framework + \
                "&page=" + str(page) + "&size=" + SIZE
            time.sleep(0.2)
            result += get_page(url1)
            logger.debug(f'{page}')
        logger.debug(
            f'Total records: {tot_records} // Nombre de résultats: {len(result)}')

    if tot_records != len(result):
        raise Exception('matching records faild')
    return result
