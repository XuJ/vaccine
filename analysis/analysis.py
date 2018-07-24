import copy
import json
import os

import numpy as np
import pandas as pd


def include_name(x):
    name_list = ['长春生物', '长春长生']
    # name_list = ['长春生物']
    null_list = [np.nan, None, 'NULL', 'null', '', ' ','None','NONE','none','Null','nan','NAN','NaN']
    if x not in null_list:
        for name in name_list:
            if name in x:
                return True
    return False


BASE_DIR = 'csv'
csv_files = os.listdir(BASE_DIR)
dfs = []
for file in csv_files:
    f = open(os.path.join(BASE_DIR, file), encoding='utf8')
    df = pd.read_csv(f)
    dfs.append(df)

final_df = pd.concat(dfs)
final_df.name = final_df.name.apply(lambda x: x.strip())

has_data_provs = final_df.prov.unique()
vaccinations_affected = final_df[final_df.create_company.apply(include_name)].name.unique()
print(len(vaccinations_affected)/len(final_df.name.unique()), len(final_df[final_df.create_company.apply(include_name)])/len(final_df))

with open(os.path.join('src', 'zh-mainland-provinces.geojson'), 'r', encoding='utf8') as f:
    geo_data = json.load(f)

for feature in geo_data['features']:
    if feature['properties']['name_local'] is None:
        feature['properties']['name_local'] = u"青海|青海"


def prov_affected(prov, included_prov):
    # return True if prov is in included_prov
    for a_prov in included_prov:
        if prov in a_prov:
            return True
    return False


def prov_included(prov, has_data_provs):
    # return True if prov is in has_data_provs
    for a_prov in has_data_provs:
        if prov in a_prov:
            return True
    return False


def prepare_geo_json(vac_name, final_df, geo_data, has_data_provs):
    part_df = final_df[np.logical_and(final_df.name == vac_name, map(include_name, final_df.create_company))]
    included_prov = part_df.prov.unique()
    geo_data_copy = copy.deepcopy(geo_data)
    for idx, feature in enumerate(geo_data_copy['features']):
        name = feature['properties']['name_local']
        if not name:
            continue
        # 黑龙江繁体在前 - hardcode
        if idx != 30:
            prov = name.split("|")[-1].encode('utf-8')
        else:
            prov = name.split("|")[0].encode('utf-8')
        if not prov_included(prov, has_data_provs):  # no data - grey
            feature['properties']['style'] = {
                'color': 'black',
                'weight': 1,
                'fillColor': 'grey',
                'fillOpacity': 0.3
                }
        elif prov_affected(prov, included_prov):  # has affected vaccine - red
            feature['properties']['style'] = {
                'color': 'black',
                'weight': 1,
                'fillColor': 'red',
                'fillOpacity': 0.3
                }
        else:  # has data but no affected vaccine - white
            feature['properties']['style'] = {
                'color': 'black',
                'weight': 1,
                'fillColor': 'white',
                'fillOpacity': 0.3
                }
    return geo_data_copy


m = Map(center=(39.9042, 116.4074), zoom=4)
for vaccination in vaccinations_affected:
    geo_json = GeoJSON(data=prepare_geo_json(vaccination, final_df, geo_data, has_data_provs),
                       name=unicode(vaccination, 'utf-8'))
    m.add_layer(geo_json)
m.add_control(LayersControl())
m
