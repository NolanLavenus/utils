import os
from pathlib import Path
from sqlalchemy import create_engine, engine
import pandas as pd
import requests
import xmltodict
import json
from datetime import datetime
import re

output = os.path.join(Path(__file__).parent, 'out')
getcapabilities = os.path.join(output, 'getcapabilities.json')

def structure_data(data):
    entries = data if isinstance(data, list) else [data]

    rows = []

    for entry in entries:
        title = entry["title"]
        links = entry["link"]
        if isinstance(links, dict):
            links = [links]

        rows.append({
            "id": title.lower().replace(" ", "_").replace("-", "_").replace("®", ""),
            "title": title,
            "api_link": [l["@href"] for l in links],
            "type": [l["@type"] for l in links],
            "updated": entry.get("updated"),
            "desc": entry["content"],
            "zones": entry.get("gpf_dl:zone"),
            "formats": entry.get("gpf_dl:format")
        })

    df = pd.DataFrame(rows)
    df["updated"] = pd.to_datetime(df["updated"])
    for col in ("api_link", "type", "zones", "formats"):
        df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False))
    return df

def db_connect(database = os.getenv("DB")):
    db_url=f"postgresql://{os.getenv("USER")}:{os.getenv("PSWD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{database}"
    return create_engine(db_url)

def get_formats(data: pd.DataFrame):
    formats = data["formats"].loc("index")[0]
    return [f["@term"] for f in formats]

def get_json_from_api(url):
    r = requests.get(url)
    return xmltodict.parse(r.text)

def sql_export(df: pd.DataFrame, table_name: str, conn: engine, schema: str):
    df.to_sql(
        name=table_name,
        con=conn,
        if_exists='replace',
        schema=schema
    )

def api_diffusion_structure_data(data):
    entries = data if isinstance(data, list) else [data]

    rows = []

    for entry in entries:
        title = entry['Title']
        abstract = entry['Abstract']
        match = None
        date_str = None
        date = None
        if abstract:
            match = re.search(r"(\d{4}-\d{2}-\d{2})", abstract)
        date_str = match.group(1) if match else None
        if date_str:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                date = None
        rows.append({
            "id": title.lower().replace(" ", "_").replace("-", "_").replace("®", ""),
            "title": title,
            "api_link": f"https://data.geopf.fr/wfs/ows?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES={entry['Name']}&SRSNAME=EPSG:4326&outputFormat=application/json",
            "type": "application/json",
            "updated": date,
            "desc": abstract
        })

    df = pd.DataFrame(rows)
    df["updated"] = pd.to_datetime(df["updated"], format="%Y-%m-%d", utc=True, errors="coerce").dt.date
    return df