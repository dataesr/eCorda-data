import os, json
import pandas as pd
from ecorda.api import base_api
from utils.logger import get_logger

logger = get_logger(__name__)

os.system(f'mkdir -p /eCorda_data')

def extraction_all(framework, liste_datas, url_ue):
    counter=0
    datas_load=[]
    datas_empty=[]
    for b in liste_datas:   
        result = base_api(base=b, framework=framework, url_ue=url_ue)
        b = b.replace("/", "_")

        if result:
            with open('/eCorda_data/'+b+'.json','w') as file:
                file.write(json.dumps(result, indent=4))
            datas_load.append(b)
            counter+=1
        else:
            datas_empty.append(b)
            
    logger.debug(f'datas empty no load: {datas_empty}') 
    No_load_datas = [i for i in liste_datas if (i.replace("/", "_") not in datas_empty) & (i.replace("/", "_") not in datas_load)]
    logger.debug(f'datas no load because prob: {No_load_datas}')                          