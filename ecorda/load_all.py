import os
import json
from ecorda.api import base_api
from utils.logger import get_logger

logger = get_logger(__name__)

os.system(f'mkdir -p /eCorda_data')


def extraction_all(framework, liste_datas, url_ue):
    datas_load = []
    datas_empty = []
    datas_errors = []
    for b in liste_datas:
        try:
            result = base_api(base=b, framework=framework, url_ue=url_ue)
            b = b.replace("/", "_")

            if result:
                with open('/eCorda_data/'+b+'.json', 'w') as file:
                    file.write(json.dumps(result, indent=4))
                datas_load.append(b)
            else:
                datas_empty.append(b)
        except Exception as e:
            logger.error(f'Error in table {b}: {e}')
            datas_errors.append([b, e])

    try:
        logger.debug(f'Enpty tables: {datas_empty}')
        logger.debug(f'Loaded tables: {datas_load}')
        logger.debug(f'Error: {datas_errors}')
    except Exception as e:
        logger.error(f'Error in logging: {e}')
    return datas_load, datas_empty, datas_errors
