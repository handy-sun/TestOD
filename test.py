import timeit
import pandas as pd

# import numpy as np

list_df = []
dict_od = dict()
set_site = set()


# @timeit.timeit
def data_static(df):
    # 删除某列含有特定数值的行
    df = df[~df['交易金额'].isin([0])]
    df = df[~df['上次交易车站'].isin([0])]

    # df.index = [i for i in range(df.shape[0])]  # 重新建立索引
    df = df.reset_index(drop=True)  # 重新建立索引 法2
    df = df.drop('交易金额', axis=1)  # axis:{0:'index', 1:'columns'}
    # df.to_csv('Result.csv')
    return df
    # print(df)


def flow(df):
    for row in df.itertuples():
        if row[1] in set_site:
            index2 = get_index(row[1], list_df)
            if row[1] < row[2]:
                list_df[index2][1] += 1
            else:
                list_df[index2][2] += 1
            list_df[index2][3] += 1
        else:
            set_site.add(row[1])
            list_site = [0] * 4
            list_site[0] = row[1]
            if row[1] < row[2]:
                list_site[1] += 1
            else:
                list_site[2] += 1
            list_site[3] += 1
            list_df.append(list_site)

    print(list_df)


def get_index(val, _list):
    length = len(_list)
    for i in range(length):
        if _list[i][0] == val:
            return i


if __name__ == '__main__':
    data = pd.read_csv('filein.csv', usecols=[5, 6, 9])
    d_frame = data_static(data)
    flow(d_frame)
    time = timeit.repeat('flow', setup='from  __main__ import flow', repeat=5, number=1)
    print(min(time))

