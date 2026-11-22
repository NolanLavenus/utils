import requests
import xmltodict
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

# Functions
from utils import api_diffusion_structure_data, db_connect, sql_export

apigpf_diffusion = "https://data.geopf.fr/wfs/ows?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities"

r = requests.get(apigpf_diffusion)
r = xmltodict.parse(r.content)

resources = r['wfs:WFS_Capabilities']['FeatureTypeList']['FeatureType']

dfs = [api_diffusion_structure_data(resource) for resource in resources]

df = pd.concat(dfs, ignore_index=True)

sql_export(
    df=df,
    table_name=f"getcapabilities",
    conn=db_connect(),
    schema="diffusion"
)