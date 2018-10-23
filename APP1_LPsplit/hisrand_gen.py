# -*- coding: utf-8 -*-
"""
DB:
1.APP1_LPsplit_ITEM_CATEGORY include item_code, describe, category, price and etc.;
2.Rand generate a df of fake data to DB.
"""
# !!!if_exsit='replace' will drop the sheet and rebuild, so generally use 'append'
# import APP1_LPsplit_ITEM_CATEGORY from excel
import pandas as pd
from sqlalchemy import create_engine
# engine = create_engine("mysql://<name>:<password>@<ip>/db?charset=utf8", echo=True) # Using mysql
# engine = create_engine('mssql+pymssql://<ip>/db?') # Using sqlserver
# engine = create_engine(r'sqlite:///D:\ProjectSites\db.sqlite3', echo=True) # Using absolute dir
engine = create_engine(r'sqlite:///db.sqlite3', echo=True)
# df = pd.read_excel(r'D:\ProjectSites\APP1_LPsplit\appfiles\ITEM_CATEGORY.xlsx')
df = pd.read_excel(r'APP1_LPsplit/appfiles/ITEM_CATEGORY.xlsx')
df.to_sql('APP1_LPsplit_ITEM_CATEGORY',engine,if_exists='replace',index=False)

# Generate a df of fake data
hislen=1000
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
engine = create_engine(r'sqlite:///db.sqlite3', echo=True)
ITEM_CATEGORY = pd.read_sql('SELECT * FROM APP1_LPsplit_ITEM_CATEGORY',engine)
Items = ITEM_CATEGORY.ITEM.to_dict()
# NO. ITEM, QTY generate independently, maximum NO.=hislen/5
hisrand = pd.DataFrame()
hisrand['NO.'] = np.random.randint(1,high=hislen//5,size=hislen)
hisrand['ITEM'] = np.random.randint(0,high=len(Items),size=hislen)
hisrand['ITEM'] = hisrand['ITEM'].map(Items)
hisrand['QTY'] = np.random.randint(1,high=6,size=hislen)
hisrand = hisrand.sort_values(by=['NO.','ITEM'])
hisrand.to_sql('APP1_LPsplit_HISRAND',engine,if_exists='replace',index=False)
