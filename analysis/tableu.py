import copy
import json
import os

import pandas as pd
from ipyleaflet import GeoJSON, LayersControl, Map

data = pd.read_csv('../analysis/data2.csv', encoding='utf8')
data_sub = data[data['生产企业'].isin(['长春长生生物科技有限责任公司', '深圳康泰生物制品股份有限公司', '罗益（无锡）生物制药有限公司', '北京祥瑞生物制品有限公司'])].copy(
    deep=True)

has_data_provs = data['省市'].unique()
vaccinations_affected = data_sub['疫苗名称'].unique()

with open(os.path.join('../src', 'zh-mainland-provinces.geojson'), 'r', encoding='utf8') as f:
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


def affected_ratio(prov, included_prov, part_df):
    # return the affected ratio in specific prov for specific vaccinee
    for prov_name in included_prov:
        if prov in prov_name:
            break
    affected_num = len(part_df[(part_df['省市'] == prov_name) & (
        part_df['生产企业'].isin(['长春长生生物科技有限责任公司', '深圳康泰生物制品股份有限公司', '罗益（无锡）生物制药有限公司', '北京祥瑞生物制品有限公司']))])
    total_num = len(part_df[(part_df['省市'] == prov_name)])
    affected_ratio = affected_num / total_num
    return affected_ratio


def prepare_geo_json(vac_name, data, geo_data, has_data_provs):
    part_df = data[(data['疫苗名称'] == vac_name)]
    included_prov = part_df.loc[
        part_df['生产企业'].isin(['长春长生生物科技有限责任公司', '深圳康泰生物制品股份有限公司', '罗益（无锡）生物制药有限公司', '北京祥瑞生物制品有限公司']), '省市'].unique()
    geo_data_copy = copy.deepcopy(geo_data)
    for idx, feature in enumerate(geo_data_copy['features']):
        name = feature['properties']['name_local']
        if not name:
            continue
        # 黑龙江繁体在前 - hardcode
        if idx != 30:
            prov = name.split("|")[-1]
        else:
            prov = name.split("|")[0]
        if not prov_included(prov, has_data_provs):  # no data - grey
            feature['properties']['style'] = {
                'color': 'black',
                'weight': 1,
                'fillColor': 'grey',
                'fillOpacity': 0.5
                }
        elif prov_affected(prov, included_prov):  # has affected vaccine - red
            feature['properties']['style'] = {
                'color': 'black',
                'weight': 1,
                'fillColor': 'red',
                'fillOpacity': affected_ratio(prov, included_prov, part_df)
                }
        else:  # has data but no affected vaccine - white
            feature['properties']['style'] = {
                'color': 'black',
                'weight': 1,
                'fillColor': 'green',
                'fillOpacity': 0.5
                }
    return geo_data_copy


m = Map(center=(40, 110), zoom=4, layout=Layout(width='100%', height='700px'))
for vac_name in vaccinations_affected:
    geo_json = GeoJSON(data=prepare_geo_json(vac_name, data, geo_data, has_data_provs), name=vac_name)
    m.add_layer(geo_json)
m.add_control(LayersControl())
m
