# -*- coding: utf-8 -*-
"""
生成随机流水数据并导入到数据库中:
1.维护产品数据基表ITEM_CATEGORY，内容包括产品编码，描述，分类，价格等信息；
2.随机生成历史流水假数据。
"""
#!!!if_exsit='replace'表若存在的话会drop重建，所以一般就使用append
#导入产品基表
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine(r'sqlite:///D:\ProjectSites\db.sqlite3', echo=True)
#engine = create_engine("mysql://<name>:<password>@<ip>/db?charset=utf8", echo=True) #连接mysql
#engine = create_engine('mssql+pymssql://<ip>/db?') #连接sql server
df = pd.read_excel(r'D:\ProjectSites\APP1_LPsplit\appfiles\ITEM_CATEGORY.xlsx')
df.to_sql('APP1_LPsplit_ITEM_CATEGORY',engine,if_exists='replace',index=False)

#生成一组历史假流水数据
hislen=1000
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
engine = create_engine(r'sqlite:///D:\ProjectSites\db.sqlite3', echo=True)
ITEM_CATEGORY = pd.read_sql('SELECT * FROM APP1_LPsplit_ITEM_CATEGORY',engine)
Items = ITEM_CATEGORY.ITEM.to_dict()
#流水单号，编码，数量单独随机生成，最大单号设为总量/5
hisrand = pd.DataFrame()
hisrand['NO.'] = np.random.randint(1,high=hislen//5,size=hislen)
hisrand['ITEM'] = np.random.randint(0,high=len(Items),size=hislen)
hisrand['ITEM'] = hisrand['ITEM'].map(Items)
hisrand['QTY'] = np.random.randint(1,high=6,size=hislen)
hisrand = hisrand.sort_values(by=['NO.','ITEM'])
hisrand.to_sql('APP1_LPsplit_HISRAND',engine,if_exists='replace',index=False)
