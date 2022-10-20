import os
import pandas as pd
from eCorda_code.api import base_api
from application.server.main.logger import get_logger

logger = get_logger(__name__)

os.system(f'mkdir -p /eCorda_data')

def extraction_all(framework, liste_datas, url_ue):
    counter=0
    for b in liste_datas:   
        result = base_api(base=b, framework=framework, url_ue=url_ue)

        if result:
            df = pd.json_normalize(result)

            list_in_df = df.applymap(lambda x: isinstance(x, list)).all()
            if list_in_df.index[list_in_df].tolist():
                for e in list_in_df.index[list_in_df].tolist():
                    for i, row in df.iterrows():
                        df.at[i , e] = ";".join(str(k) for k in row[e] if k is not None)

            df = df.drop_duplicates()
            b = b.replace("/", "_")
            filename = f'/eCorda_data/{b}.csv'
            df.to_csv(filename, sep=";", index=False, na_rep="", encoding="UTF-8")
            logger.debug(f'writing {filename}')
            if 'extractionDate' in filename:
                logger.debug(df.to_dict(orient='records'))
            counter+=1
    logger.debug(f"datas in csv:{counter}")
