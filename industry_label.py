import jieba
import pandas as pd
from tqdm import trange


def industry_label_exteact(df_work):
    df_industry_standered = pd.read_excel("zhilian-行业.xlsx", sheet_name='Sheet1')
    df_industry_tag = pd.DataFrame()

    jieba.load_userdict('custom.txt')
    jieba.suggest_freq(('计算机', '软件'), True)
    jieba.suggest_freq(('计算机', '硬件'), True)
    jieba.suggest_freq(('金属', '制品'), True)
    jieba.suggest_freq(('非金属', '矿'), True)
    jieba.suggest_freq(('制品', '业'), True)
    jieba.suggest_freq(('新闻', '出版'), True)
    jieba.suggest_freq(('会议', '展览'), True)
    jieba.suggest_freq(('广播', '电视'), True)
    jieba.suggest_freq(('咨询', '服务'), True)

    for i in trange(df_industry_standered.shape[0]):
        str_first = df_industry_standered['一级行业'][i].replace('/', '')
        str_second = df_industry_standered['二级行业'][i].replace('/', '').replace('（', '').replace('）', '')

        seg_list_first = list(jieba.cut(str_first))
        seg_list_second = list(jieba.cut(str_second))
        res = {
            '一级行业': df_industry_standered['一级行业'][i],
            '一级标签': seg_list_first,
            '二级行业': df_industry_standered['二级行业'][i],
            '二级标签': seg_list_second
        }
        df_industry_tag = df_industry_tag.append(res, ignore_index=True)

    df_industry_raw = df_work['industry_name'].drop_duplicates().reset_index(drop=True)
    industry_list = df_industry_standered['二级行业'].tolist()

    df_mapping_result = pd.DataFrame()
    for i in trange(len(df_industry_raw)):
        if df_industry_raw[i] is not None:
            tag_list = list(jieba.cut(df_industry_raw[i].replace('/', '')))
            if df_industry_raw[i] in industry_list:
                m = industry_list.index(df_industry_raw[i])
                second = df_industry_tag['二级行业'][m]
                first = df_industry_tag['一级行业'][m]
            else:
                set_len_list = []
                for t in range(df_industry_tag.shape[0]):
                    set_len_list.append(len(set(tag_list) & set(df_industry_tag['二级标签'][t])))
                max_set_index = set_len_list.index(max(set_len_list))
                if max(set_len_list) > 1:
                    second = df_industry_tag['二级行业'][max_set_index]
                    first = df_industry_tag['一级行业'][max_set_index]
                elif max(set_len_list) == 1:
                    second = '其他'
                    first = df_industry_tag['一级行业'][max_set_index]
                else:
                    second = '其他'
                    set_len_list_1 = []
                    for t in range(df_industry_tag.shape[0]):
                        set_len_list_1.append(len(set(tag_list) & set(df_industry_tag['一级标签'][t])))
                    max_set_index_1 = set_len_list_1.index(max(set_len_list_1))
                    if max(set_len_list) > 0:
                        first = df_industry_tag['一级行业'][max_set_index_1]
                    else:
                        first = '其他'
            res = {
                'industry_name': df_industry_raw[i],
                '二级行业': second,
                '一级行业': first,
                '行业标签': tag_list
            }
            df_mapping_result = df_mapping_result.append(res, ignore_index=True)

    print(df_mapping_result.head(5))
