# eCorda-data -> Horizon Europe
***

### Harvest eCorda databases from EU SI
- Collect all Horizon databases by API
- Convert to CSV format
- Save CSV and JSON files in a zip
- Send zips to Object Storage

### Run it locally:
```sh
docker build -t ecorda .
docker run --env-file=.env ecorda python3 main.py export
```
