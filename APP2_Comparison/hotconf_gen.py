# -*- coding: utf-8 -*-
"""
DB: collect hot conf from excel and import to DB
"""
import pandas as pd
from sqlalchemy import create_engine
engine = create_engine(r'sqlite:///db.sqlite3', echo=True)
df = pd.read_excel(r'D:\ProjectSites\APP2_Comparison\appfiles\套餐.xlsx').fillna('')
collect = pd.DataFrame(columns=['Name','Item','Qty'])
index_collect = 0
for i in range(1,11):
    Name = 'set'+str(i)
    for index in df.index:
        if index<2:
            pass
        elif df.loc[index,Name]!='':
            Item = df.loc[index,'ITEM']
            Qty = df.loc[index,'Qty']
            collect.loc[index_collect] = [Name,Item,Qty]
            index_collect +=1
        else:
            pass
collect['Repo'] = 'HotConf'
collect.to_sql('APP2_HotConf',engine,if_exists='replace',index=False)