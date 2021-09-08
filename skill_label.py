import pandas as pd
from tqdm import trange
import jieba.analyse
import openpyxl


def skill_label_extract(df_work):
    # 读取标准技术标签
    df_label = pd.read_excel('人才库Mapping.xlsx', sheet_name='技术标签')
    name_list = df_label.columns.tolist()
    df_label = df_label.melt(value_vars=name_list)
    df_label = df_label.dropna().reset_index(drop=True)

    # 将标准技术标签进行分词
    df_label['标签'] = ''
    for i in range(df_label.shape[0]):
        df_label['标签'][i] = list(jieba.cut(df_label['value'][i]))
        df_label['标签'][i] = [x.upper() for x in df_label['标签'][i]]

    # 将标准技术标签的分词结果添加至jieba自定义词典
    for i in range(df_label.shape[0]):
        jieba.add_word(df_label['value'][i])

    # 将df_work中的工作职责文本的分词结果存至tag_list
    df_work['tag_list'] = ''
    df_work['标签'] = ''
    for i in trange(df_work.shape[0]):
        df_work['标签'][i] = []
        if df_work['responsibilities'][i] is not None:
            df_work['tag_list'][i] = list(jieba.cut(df_work['responsibilities'][i]))
            df_work['tag_list'][i] = [x.upper() for x in df_work['tag_list'][i]]
            # 如果工作职责的分词结果的标签包含了标准技术标签的分词结果则将该技术标签分配至这段工作经历
            for t in range(df_label.shape[0]):
                label = df_label['value'][t].upper()
                if label in df_work['tag_list'][i] or set(df_label['标签'][t]).issubset(set(df_work['tag_list'][i])):
                    df_work['标签'][i].append(df_label['value'][t])

    print(df_work[['responsibilities', '标签']].head(5))
