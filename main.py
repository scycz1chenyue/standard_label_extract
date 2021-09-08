import pandas as pd
from sqlalchemy import create_engine
from skill_label import skill_label_extract
from industry_label import industry_label_exteact
from position_name_label import position_name_label_extract


# 连接数仓
def postgresql_engine():
    user = "postgres"
    password = "Passw0rd"
    host = "10.11.70.68"
    port = "5432"
    database = "edw"
    postgre_engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
    return postgre_engine


# 提取候选人work表
postgresql_engine = postgresql_engine()
df_work = pd.read_sql(
    """select * from dw_resume.mongo_resume_work""",
    con=postgresql_engine.connect())

# 返回候选人标准技术标签
skill_label_extract(df_work)

# 返回候选人标准行业标签
industry_label_exteact(df_work)

# 返回候选人标准岗位标签
position_name_label_extract(df_work)
