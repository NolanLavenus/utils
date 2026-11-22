import requests
import xmltodict
import os
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Functions
from utils import structure_data, db_connect, sql_export
# Variables
from utils import output

geopf_url = "https://data.geopf.fr/telechargement/capabilities?limit=10"

if not os.path.exists(output):
    os.mkdir(output)
getcapabilities = os.path.join(output, 'getcapabilities.json')

r_temp = requests.get(geopf_url)
r_temp = xmltodict.parse(r_temp.content)
pagecount = int(r_temp["feed"]["@gpf_dl:pagecount"])

capabilities = {}

for i in range(pagecount):
    page = i+1
    url = f"{geopf_url}&page={page}"
    r = requests.get(url)
    capabilities[str(page)] = xmltodict.parse(r.content)

if not os.path.exists(getcapabilities):
    with open(getcapabilities, "w", encoding='utf-8') as f:
        json.dump(capabilities, f, ensure_ascii=False, indent=4)
        f.close()

with open(getcapabilities, "r", encoding='utf-8') as f:
    data_api = json.load(f)
    f.close()

dfs = []

for i in data_api:
    data = data_api[i]["feed"]["entry"]
    dfs.append(pd.DataFrame(data = structure_data(data)))

sql_export(
    df=pd.concat(dfs, ignore_index=True),
    table_name=f"getcapabilities",
    conn=db_connect(),
    schema="telechargement"
    )