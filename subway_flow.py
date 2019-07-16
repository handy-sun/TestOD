# -*- coding:utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

qingdao3 = ['青岛站', '人民会堂', '汇泉广场', '中山公园', '太平角公园', '延安三路', '五四广场', '江西路', '宁夏路', '敦化路',
            '错埠岭', '清江路', '双山', '长沙路', '地铁大厦', '海尔路', '万年泉路', '李村', '君峰路', '振华路', '永平路', '青岛北站']

# @timeit.timeit 初步筛选
def data_static(df):
    # 删除 含有特定数值/上下车站相同 的行
    df = df[~df['交易金额'].isin([0])]
    df = df[~df['上次交易车站'].isin([0])]
    df = df.loc[df['上次交易车站'] != df['此次交易车站']]

    # df.index = [i for i in range(df.shape[0])]  # 重新建立索引
    df = df.reset_index(drop=True)  # 重新建立索引 法2
    df = df.drop('交易金额', axis=1)
    df.columns = ['start', 'end']
    # print(df)
    return df


def flow(df):  # 统计客流量
    df_n = df[df['start'] > df['end']]
    n_count = df_n['start'].value_counts()  # n_count<series类型>

    df_s = df[df['start'] < df['end']]
    s_count = df_s['start'].value_counts()
    # print(s_count.dtypes)
    df_mer = pd.DataFrame([s_count, n_count]).T
    df_mer.columns = ['N', 'S']
    # 按列填充空值 法1
    # df_mer.loc[df_mer['N'].isnull(), 'N'] = 0
    df_mer['N'] = df_mer['N'].fillna(0).astype(int)
    df_mer['S'] = df_mer['S'].fillna(0).astype(int)
    df_mer['SUM'] = df_mer.apply(lambda x: x.sum(), axis=1)
    # 修改索引名和列名
    df_mer.index = qingdao3
    # df_mer.columns = ['北向客流', '南向客流', '总客流']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    df_mer.plot(kind='bar', width=0.9)
    # 在柱子上显示总客流量数据
    for x, y in enumerate(df_mer['SUM']):
        plt.text(x, y + 0.5, '%s' % y, ha='center', va='bottom')
    plt.xlabel("车站")
    plt.ylabel("客流量")
    plt.title("客流量统计柱形图")
    # plt.savefig('flow.png', dpi=200)
    plt.show()

    return df_mer


def origin_destination(df, l):
    # df = df.groupby('start')['end'].value_counts().unstack()
    df = pd.DataFrame(df.groupby('start')['end'].value_counts().unstack(fill_value=0), dtype=np.int8)
    for i in l:
        df.loc[i, i] = '/'

    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 禁止自动换行(设置为False不自动换行)
    pd.set_option('expand_frame_repr', False)
    print(df.head(22))


if __name__ == '__main__':
    data = pd.read_csv('filein.csv', usecols=[5, 6, 9])
    d_frame = data_static(data)
    df_merge = flow(d_frame)
    # list_index = list(df_merge.index)
    list_index = (x for x in df_merge.index)
    origin_destination(d_frame, list_index)
