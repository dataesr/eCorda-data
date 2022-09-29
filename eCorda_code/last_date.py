import json

def lastDate():
    with open('/eCorda_data/' + 'last_date.json', 'r+') as pl:
        return json.load(pl)  

def lastDate_update(new_date):
    with open('/eCorda_data/'+"last_date.json", "w") as write_file:
        json.dump(new_date, write_file, indent=4)  