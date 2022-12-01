import os, json
import pandas as pd
from eCorda_code.api import base_api
from application.server.main.logger import get_logger

logger = get_logger(__name__)

os.system(f'mkdir -p /eCorda_data')

def extraction_all(framework, liste_datas, url_ue):
    counter=0
    datas_volume=[]
    for b in liste_datas:   
        result = base_api(base=b, framework=framework, url_ue=url_ue)
    
        if result:

            b = b.replace("/", "_")

            # create Json    
            unique = []
            [unique.append(r) for r in result if r not in unique]
            filename = f'/eCorda_data/{b}.json'    
            with open(filename, 'w') as file:
                file.write(json.dumps(unique, indent=4))
            datas_volume.append([b, 'json', len(unique)])
            counter+=1

            # créate CSV
            df = pd.json_normalize(result)
            list_in_df = df.applymap(lambda x: isinstance(x, list)).all()
            if list_in_df.index[list_in_df].tolist():
                for e in list_in_df.index[list_in_df].tolist():
                    for i, row in df.iterrows():
                        df.at[i , e] = ";".join(str(k) for k in row[e] if k is not None)

            df = df.drop_duplicates()
            filename = f'/eCorda_data/{b}.csv'
            df.to_csv(filename, sep=";", index=False, na_rep="", encoding="UTF-8")
            datas_volume.append([b, 'csv',len(df)])
            logger.debug(f'writing {filename}')
            if 'extractionDate' in filename:
                logger.debug(df.to_dict(orient='records'))
            counter+=1


    No_load_datas = [i for i in liste_datas if i not in set([x[0] for x in datas_volume])]
    pd.DataFrame(datas_volume, columns=['data', 'format', 'observations']).to_csv("/eCorda_data/datas_volume.csv", sep=";", index=False, na_rep="", encoding="UTF-8")
    logger.debug(f"***datas loaded:{counter}, datas no_load: {No_load_datas}****")