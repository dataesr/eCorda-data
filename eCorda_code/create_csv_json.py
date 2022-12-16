import os, json
from pathlib import Path
import pandas as pd
from application.server.main.logger import get_logger

logger = get_logger(__name__)

def create_csv_json(framework, liste_datas):
    datas_volume=[]
    counter=0
    
    for b in liste_datas:   
        b = b.replace("/", "_")
        if Path('/eCorda_data/'+b+'.json').is_file():
            with open('/eCorda_data/'+b+'.json','r') as file:
                result = json.load(file)

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
        
        if 'extractionDate' in filename:
            logger.debug(df.to_dict(orient='records'))
        counter+=1

    else:
        pass


    datas_volume=pd.DataFrame(datas_volume, columns=['data', 'format', 'observations'])
    datas_volume.to_csv("/eCorda_data/datas_volume.csv", sep=";", index=False, na_rep="", encoding="UTF-8")      
    with open('/eCorda_data/datas_volume.json', 'w') as file:  
        file.write(json.dumps(datas_volume.to_json(orient='records'), indent=4))
    logger.debug(f"datas created:{counter}, *****")



