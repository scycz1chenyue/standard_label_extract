# 候选人标签体系文档
***
### 项目背景
将半结构化的简历数据中的岗位和行业匹配标准的标签，并将标准的技术标签匹配到每段工作经历上。
### 主要功能
1. 匹配技术标签
* `skill_label_extract`接受一个输入参数：简历数据工作经历的dataframe；并返回一个在原dataframe上新增技术标签字段的dataframe。
* 标准技术标签的数据存在"人才库Mapping.xlsx"
2. 匹配行业标签
* `industry_label_exteact`接受一个输入参数：简历数据工作经历的dataframe；并返回一个原始行业名称、对应的标准二级行业标签、对应的标准一级行业标签组成的dataframe。
* 标准行业标签的数据来自爬取的智联招聘的行业分类，并存储在“zhilian-行业.xlsx”
3. 匹配岗位标签
* `position_name_label_extract`接受一个输入参数：简历数据工作经历的dataframe；并返回一个原始岗位名称、对应的大类、对应的岗位名称组成的dataframe。
* 标准岗位标签的数据存在”岗位mapping.xlsx“
### 代码示例输出
```
# 返回候选人标准技术标签
skill_label_extract(df_work)
# 返回候选人标准行业标签
industry_label_exteact(df_work)
# 返回候选人标准岗位标签
position_name_label_extract(df_work)
```
```
                                    responsibilities                                     标签
0  负责 Java 编程解决数据结构算法;\n 负责SSH2 框架的搭建及“音乐论坛”的设...                      [Java, 数据结构, SSH]
1  负责“日晖科技信息有限公司主页(http://www.rihuisoft.com)“设计...                                  [SSM]
2  负责“火灾逃生虚拟演练系统“的设计与开发,其中对导航网格寻路算法做了进一步的改进,提出\...                                     []
3  酒店入住记录方案开发(数据库操作);\n 天气服务缩减流量(Session 操作);\...                                     []
4  日志展示前后端开发及配置管理初步搭建(flask-appbuilder+mysql+bo...  [XML, Flask, Bootstrap, MySQL, 前后端开发]

    industry_name      二级行业          一级行业                        行业标签
0  IT服务(系统/数据/维护)      IT服务  互联网/IT/电子/通信  [IT, 服务, (, 系统, 数据, 维护, )]
1        广告/会展/公关        其他            其他                [广告, 会展, 公关]
2    通信/电信运营、增值服务  运营商/增值服务  互联网/IT/电子/通信     [通信, 电信, 运营, 、, 增值, 服务]
3           计算机软件     计算机软件  互联网/IT/电子/通信                   [计算机, 软件]
4        互联网/IT服务      IT服务  互联网/IT/电子/通信               [互联网, IT, 服务]

          原始岗位名称         岗位名称    大类
0       Java后台开发    Java开发工程师  后端开发
1    后台开发工程师 实习生    Java开发工程师  后端开发
2       虚拟仿真项目开发           其他  后端开发
3          服务器开发           其他  后端开发
4  Python后台开发工程师  Python开发工程师  后端开发
```