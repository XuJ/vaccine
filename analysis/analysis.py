import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def clean_create_company(x):
    x = x.upper()
    x = re.compile('\s').sub('', x)
    x = re.compile('\(').sub('（', x)
    x = re.compile('\)').sub('）', x)
    x = re.compile('研宄所').sub('研究所', x)
    x = re.compile('有限贵任公司').sub('有限责任公司', x)
    x = re.compile('研究有限责任公司').sub('研究所有限责任公司', x)
    p = re.compile('公司')
    m = p.search(x)
    if m:
        x = x[:m.end()]

    if '长春长生' in x or '长春生物' in x:
        return '长春长生生物科技有限责任公司'
    elif '康泰' in x or '康秦' in x:
        return '深圳康泰生物制品股份有限公司'
    elif '罗益' in x:
        return '罗益（无锡）生物制药有限公司'
    elif '玉溪' in x:
        return '玉溪沃森生物技术有限公司'
    elif '长春析健' in x or '长春祈健' in x:
        return '长春祈健生物制品有限公司'
    elif '科园倩海' in x or '科园信海' in x:
        return '科园信海（北京）医疗用品贸易有限公司'
    elif '博雅生物' in x:
        return '博雅生物制药集团股份有限公司'
    elif '中逸安科' in x:
        return '中逸安科生物技术股份有限公司'
    elif '国光生物' in x:
        return '台湾国光生物科技股份有限公司'
    elif '中国医学科学院医学生物研究所' in x or '中国医学科学院医学生物学研究所' in x:
        return '中国医学科学院医学生物学研究所'
    elif '赛诺菲巴斯德' in x or 'SANOFIPASTEURS' in x or 'SANOFI' in x:
        return 'SANOFI.PASTEUR.S.A'
    elif 'GLAXOSMITHKLINE' in x:
        return 'GLAXOSMITHKLINE.BIOLOGICALS.S.A.'
    elif 'CHIRON' in x:
        return 'CHIRON.BEHRING.VACCINES.PRIVATE.LTD.'
    elif 'PFIZER' in x:
        return 'PFIZER.IRELAND.PHARMACEUTICALS'
    elif 'DOHME' in x:
        return 'MERCK.SHARP.DOHME.CORP.'
    else:
        return x


def clean_vaccine_name(x):
    if '肝' in x:
        if '重组乙型肝炎疫苗' in x:
            return '重组乙型肝炎疫苗'
        elif '重组乙型肝炎' in x:
            return '重组乙型肝炎疫苗'
        elif '乙型肝炎疫苗' in x:
            return '重组乙型肝炎疫苗'
        elif '甲型乙型肝炎联合疫苗' in x:
            return '甲型乙型肝炎联合疫苗'
        elif '乙肝联合疫苗' in x:
            return '甲型乙型肝炎联合疫苗'
        elif '甲型肝炎灭活疫苗' in x:
            return '甲型肝炎灭活疫苗'
        elif '重组戊型肝炎疫苗' in x:
            return '重组戊型肝炎疫苗'
        elif '冻干甲型肝炎减毒活疫苗' in x:
            return '冻干甲型肝炎减毒活疫苗'
        elif '甲肝灭活疫苗' in x:
            return '甲型肝炎灭活疫苗'
        elif '冻干甲肝减毒活疫苗' in x:
            return '冻干甲型肝炎减毒活疫苗'
        elif '乙型肝炎人免疫球蛋白' in x:
            return '重组乙型肝炎疫苗'
        else:
            return x
    elif '狂犬病' in x:
        if '人用狂犬病疫苗' in x:
            return '人用狂犬病疫苗'
        elif '狂犬病人免疫球蛋白' in x:
            return '人用狂犬病疫苗'
        else:
            return x
    elif '脑炎' in x:
        if '乙型脑炎灭活疫苗' in x:
            return '乙型脑炎灭活疫苗'
        elif '森林脑炎灭活疫苗' in x:
            return '森林脑炎灭活疫苗'
        elif '乙型脑炎减毒活疫苗' in x:
            return '乙型脑炎减毒活疫苗'
        else:
            return x
    elif '脑膜炎' in x:
        if 'W135' in x:
            return 'ACYW135群脑膜炎球菌多糖疫苗'
        elif 'ACYW136' in x:
            return 'ACYW136群脑膜炎球菌多糖疫苗'
        elif 'ACYW137' in x:
            return 'ACYW137群脑膜炎球菌多糖疫苗'
        elif 'b' in x:
            return 'AC群脑膜炎球菌（结合）b型流感嗜血杆菌（结合）联合疫苗'
        elif 'A' in x and 'C' in x:
            return 'A群C群脑膜炎球菌多糖结合疫苗'
        else:
            return x
    elif '裂解' in x:
        return '流行性感冒病毒裂解疫苗'
    elif '水痘' in x:
        return '水痘减毒活疫苗'
    elif '麻' in x:
        if '麻疹风疹' in x:
            return '麻疹风疹联合减毒活疫苗'
        elif '麻腮风' in x:
            return '麻腮风联合减毒活疫苗'
        elif '麻疹腮腺炎' in x:
            return '麻疹腮腺炎联合减毒活疫苗'
    elif '肺' in x:
        if '23' in x:
            return '23价肺炎球菌多糖疫苗'
        elif '13' in x:
            return '13价肺炎球菌多糖疫苗'
        else:
            return x
    elif '肠道' in x:
        if '72' in x:
            return '肠道病毒72型灭活疫苗'
        elif '71' in x:
            return '肠道病毒71型灭活疫苗'
        else:
            return x
    elif '霍乱' in x:
        if '重组B亚单位/菌体霍乱' in x:
            return '重组B亚单位/菌体霍乱疫苗'
        elif '霍乱疫苗' in x:
            return '霍乱疫苗'
        else:
            return x
    elif '腮腺炎' in x:
        return '腮腺炎减毒活疫苗'
    elif '百白破' in x:
        return '吸附无细胞百白破灭活脊髓灰质炎和b型流感嗜血杆菌（结合）联合疫苗'
    elif '流感' in x:
        if '嗜血杆菌' in x:
            return 'b型流感嗜血杆菌结合疫苗'
        elif '流感病毒亚单位疫苗' in x:
            return '流感病毒亚单位疫苗'
        else:
            return x
    elif '人乳头瘤' in x:
        if '双价' in x:
            return '双价人乳头瘤病毒吸附疫苗'
        elif '四价' in x:
            return '四价人乳头瘤病毒疫苗'
        elif '人乳头瘤病毒吸附疫苗' in x:
            return '人乳头瘤病毒吸附疫苗'
        else:
            return x
    elif '伤寒' in x:
        return '伤寒vi多糖疫苗'
    elif '黄热' in x:
        return '黄热病减毒活疫苗'
    elif '肾' in x:
        return '双价肾综合征出血热灭活疫苗'
    elif 'EV71' in x:
        return 'EV71型灭活疫苗'
    elif 'EV72' in x:
        return 'EV72型灭活疫苗'
    elif '破伤风' in x:
        return '吸附破伤风疫苗'
    elif '轮状病毒' in x:
        return '口服轮状病毒活疫苗'
    elif '卡介菌' in x:
        return '卡介菌纯蛋白衍生物'
    elif '炭疽' in x:
        return '皮上划痕人用炭疽活疫苗'
    else:
        return np.nan


BASE_DIR = 'csv'
csv_files = os.listdir(BASE_DIR)
dfs = []
for file in csv_files:
    f = open(os.path.join(BASE_DIR, file), encoding='utf8')
    df = pd.read_csv(f)
    dfs.append(df)

final_df = pd.concat(dfs)
final_df.name = final_df.name.apply(lambda x: x.strip())

data = final_df.copy(deep=True)
data['name'] = final_df['name'].apply(clean_vaccine_name)
data.dropna(inplace=True)
data.to_csv('analysis/data.csv', encoding='utf8', index=False)

# data = pd.read_csv('analysis/data.csv', encoding='utf8')
data['create_company'] = data['create_company'].apply(clean_create_company)

data.rename(columns={
    'create_company': '生产企业',
    'name': '疫苗名称',
    'price': '供应价',
    'report_company': '申报企业',
    'src': '原产',
    'prov': '省市',
    'year': '年份'
    }, inplace=True)

data.to_csv('analysis/data2.csv', encoding='utf8', index=False)

font_name = "STKaiti"
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(20, 18))
ax1 = sns.countplot(y=data['疫苗名称'], order=data['疫苗名称'].value_counts().index)
plt.title('全国各种第二类疫苗的中标情况')
plt.ylabel('疫苗名称')
plt.xlabel('中标数量')
totals = []
for p in ax1.patches:
    totals.append(p.get_width())
total = np.nansum(totals)
for p in ax1.patches:
    ax1.annotate('{:.1f}%'.format(p.get_width() / total * 100), (p.get_width() + 4, p.get_y() + p.get_height() / 2.),
                 ha='center', va='center')
plt.tight_layout()
plt.savefig('image/全国各种第二类疫苗的中标情况.jpg')
plt.close('all')

font_name = "STKaiti"
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False
plt.figure(figsize=(20, 18))
ax2 = sns.countplot(y=data['生产企业'], order=data['生产企业'].value_counts().index)
plt.title('各生产企业在全国各种第二类疫苗的中标占比')
plt.ylabel('生产企业')
plt.xlabel('中标数量')
totals = []
for p in ax2.patches:
    totals.append(p.get_width())
total = np.nansum(totals)
for p in ax2.patches:
    ax2.annotate('{:.1f}%'.format(p.get_width() / total * 100), (p.get_width() + 2, p.get_y() + p.get_height() / 2.),
                 ha='center', va='center')
plt.tight_layout()
plt.savefig('image/各生产企业在全国各种第二类疫苗的中标占比.jpg')
plt.close('all')

data2 = data.copy(deep=True)
data2['企业名称'] = data['生产企业'].apply(
    lambda x: '长春系公司' if x in ['长春长生生物科技有限责任公司', '深圳康泰生物制品股份有限公司', '罗益（无锡）生物制药有限公司', '北京祥瑞生物制品有限公司'] else '其他公司')
data3 = data2[data['疫苗名称'].isin(data2[data2['企业名称'] == '长春系公司']['疫苗名称'].unique())].copy(deep=True)

font_name = "STKaiti"
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False
ax3 = sns.countplot(y=data3['疫苗名称'], order=data3['疫苗名称'].value_counts().index, hue=data3['企业名称'])
plt.title('长春系公司在第二类疫苗的中标情况')
plt.ylabel('疫苗名称')
plt.xlabel('中标数量')
totals = []
for p in ax3.patches:
    if np.isnan(p.get_width()):
        totals.append(0)
    else:
        totals.append(p.get_width())
total = []
for i in range(len(totals)):
    if i < len(totals) / 2:
        total.append(totals[i] + totals[i + int(len(totals) / 2)])
    else:
        total.append(totals[i] + totals[i - int(len(totals) / 2)])
for i, p in enumerate(ax3.patches):
    ax3.annotate('{:.0f}%'.format(p.get_width() / total[i] * 100),
                 (p.get_width() + 5.5, p.get_y() + p.get_height() / 2.), ha='center', va='center', size=8)
plt.tight_layout()
plt.savefig('image/长春系公司在第二类疫苗的中标情况.jpg', dpi=200)
plt.close('all')

font_name = "STKaiti"
plt.rcParams['font.family'] = font_name
plt.rcParams['axes.unicode_minus'] = False
ax4 = sns.countplot(y=data3['省市'], order=data3['省市'].value_counts().index, hue=data3['企业名称'])
plt.title('长春系公司在全国范围的中标情况')
plt.ylabel('省市自治区')
plt.xlabel('中标数量')
totals = []
for p in ax4.patches:
    totals.append(p.get_width())
total = []
for i in range(len(totals)):
    if i < len(totals) / 2:
        total.append(totals[i] + totals[i + int(len(totals) / 2)])
    else:
        total.append(totals[i] + totals[i - int(len(totals) / 2)])
for i, p in enumerate(ax4.patches):
    ax4.annotate('{:.0f}%'.format(p.get_width() / total[i] * 100), (p.get_width() + 2, p.get_y() + p.get_height() / 2.),
                 ha='center', va='center', size=7)
plt.tight_layout()
plt.savefig('image/长春系公司在全国范围的中标情况.jpg', dpi=200)
plt.close('all')
