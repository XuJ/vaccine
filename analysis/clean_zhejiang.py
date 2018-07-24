import os

import numpy as np
import pandas as pd

BASE_DIR = 'csv1'
csv_files = os.listdir(BASE_DIR)
dfs = []
for file in csv_files:
    f = open(os.path.join(BASE_DIR, file), encoding='utf8')
    df = pd.read_csv(f)
    dfs.append(df)

a = dfs[11]
a.rename(columns={
    "供应商/生产企业": "create_company",
    "中标价（元）": "price",
    '品名': "name",
    }, inplace=True)
src_list = ['国产', '进口']
a['src'] = a['name'].apply(lambda x: np.nan if x[:2] not in src_list else x[:2])
a['name'] = a['name'].apply(lambda x: x if x[:2] not in src_list else x[2:])
a['prov'] = csv_files[11].strip(".csv")
a['year'] = 2018
a['report_company'] = a['create_company']
del a['计量单位']
del a['序号']

a.to_csv('csv/浙江省.csv', encoding='utf8', index=False)
