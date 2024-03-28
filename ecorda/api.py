import json
import requests
import time
from retry import retry
from ecorda.token_api import get_headers
from utils.logger import get_logger

logger = get_logger(__name__)

PAGE_SIZE = 500


@retry(delay=10, tries=4)
def get_page(url):
    try:
        r = requests.get(url, headers=get_headers())
        return r.json()['data']
    except Exception as e:
        logger.error(f'Error fetching {url}: {e}')
        raise e


def base_api(base=None, framework=None, url_ue=None):
    SIZE = str(PAGE_SIZE)
    url = url_ue + base + "?framework=" + framework + "&size=" + SIZE
    r = requests.get(url, headers=get_headers())

    tot_records = r.json().get("metadata").get("totalRecords")
    page_max = r.json().get("metadata").get("lastPage")
    # last_page_size = tot_records % PAGE_SIZE

    started_at = time.strftime("%H:%M:%S")

    result = []
    if tot_records != 0 and tot_records <= PAGE_SIZE:
        url1 = url_ue + base + "?framework=" + \
            framework + "&page=1&size=" + str(tot_records)
        time.sleep(0.2)
        result += get_page(url1)
        # logger.debug('1')
    if tot_records > PAGE_SIZE:
        for page in range(1, page_max+1):
            url1 = url_ue + base + "?framework=" + framework + \
                "&page=" + str(page) + "&size=" + SIZE
            time.sleep(0.2)
            result += get_page(url1)
            # logger.debug(f'{page}')
        # logger.debug(
        #     f'Total records: {tot_records} // Nombre de résultats: {len(result)}')

    logger.debug(
        f'***{base} -> totalRecords:{tot_records}, totalPage:{page_max}, Nombre de résultats: {len(result)}, start:{started_at}, end:{time.strftime("%H:%M:%S")}***')

    if tot_records != len(result):
        raise Exception('matching records faild')
    return result
