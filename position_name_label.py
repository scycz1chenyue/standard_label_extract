import pandas as pd
import openpyxl
from tqdm import trange
import jieba


def position_name_label_extract(df_work):
    df_standard = pd.read_excel('岗位mapping.xlsx')

    df_position_tag = pd.DataFrame()

    jieba.load_userdict('custom.txt')

    for i in trange(df_standard.shape[0]):
        str_first = df_standard['大类'][i].replace('/', '')
        str_second = df_standard['岗位名称'][i].replace('/', '').replace('（', '').replace('）', '')

        seg_list_first = list(jieba.cut(str_first))
        seg_list_second = list(jieba.cut(str_second))
        res = {
            '大类': df_standard['大类'][i],
            '大类标签': seg_list_first,
            '岗位名称': df_standard['岗位名称'][i],
            '岗位名称标签': seg_list_second
        }
        df_position_tag = df_position_tag.append(res, ignore_index=True)

    df_position_raw = df_work['position_name'].drop_duplicates().reset_index(drop=True)
    position_list = df_position_tag['岗位名称'].tolist()

    df_mapping_result = pd.DataFrame()
    for i in trange(len(df_position_raw)):
        if df_position_raw[i] is not None:
            tag_list = list(jieba.cut(df_position_raw[i].replace('/', '')))
            if df_position_raw[i] in position_list:
                m = position_list.index(df_position_raw[i])
                second = df_position_tag['岗位名称'][m]
                first = df_position_tag['大类'][m]
            else:
                set_len_list = []
                for t in range(df_position_tag.shape[0]):
                    set_len_list.append(len(set(tag_list) & set(df_position_tag['岗位名称标签'][t])))
                max_set_index = set_len_list.index(max(set_len_list))
                if max(set_len_list) > 1:
                    second = df_position_tag['岗位名称'][max_set_index]
                    first = df_position_tag['大类'][max_set_index]
                elif max(set_len_list) == 1:
                    second = '其他'
                    first = df_position_tag['大类'][max_set_index]
                else:
                    second = '其他'
                    set_len_list_1 = []
                    for t in range(df_position_tag.shape[0]):
                        set_len_list_1.append(len(set(tag_list) & set(df_position_tag['大类标签'][t])))
                    max_set_index_1 = set_len_list_1.index(max(set_len_list_1))
                    if max(set_len_list) > 0:
                        first = df_position_tag['大类'][max_set_index_1]
                    else:
                        first = '其他'
            res = {
                '原始岗位名称': df_position_raw[i],
                '岗位名称': second,
                '大类': first,
            }
            df_mapping_result = df_mapping_result.append(res, ignore_index=True)

    print(df_mapping_result.head(5))
