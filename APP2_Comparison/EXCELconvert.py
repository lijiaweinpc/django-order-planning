
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 14:21:51 2018

@author: l00429237
从excel里解析配置
"""

import pandas as pd
import openpyxl  
def EXCELconvert(filepath,productlist):
        wb = openpyxl.load_workbook(filepath)    
        # 获取workbook中所有的表格  
        sheets = wb.get_sheet_names()
        collect = pd.DataFrame(columns=['Name','Item','Qty','filename'])
        index_collect=0
        statuscode=0
        for st in sheets:
                if st in productlist:
                        ws = wb.get_sheet_by_name(st)
                        df = pd.DataFrame(ws.values)
                        # 定位'No.'的位置
                        for indexcol in range(df.columns.size):
                                if 'No.' in df[indexcol].tolist():
                                        headraw=df[df[indexcol]=='No.'].index
                                        break
                                elif '序号' in df[indexcol].tolist():
                                        headraw=df[df[indexcol]=='序号'].index
                                        break
                        # 删除表外的行和列
                        df=df.drop(list(range(headraw[0])))
                        df=df.drop(list(range(indexcol)),axis=1)
                        df=df.reset_index(drop=True).fillna('')
                        # 定位数量列
                        itemnumcol=[]
                        itemnumcolname=[]
                        for col in df.columns:
                                if (df.loc[0,col]=='No.') & (df.loc[1,col] != ''):
                                        print('缺少定位行')
                                        break
                                elif df.loc[1,col] != '':
                                        itemnumcol.append(col)
                                        if df.loc[1,col] in itemnumcolname:
                                                t=df.loc[1,col]+'_a'
                                                while (t in itemnumcolname):
                                                        t=t+'a'
                                                df.loc[1,col]=t
                                        itemnumcolname.append(df.loc[1,col])
                                        df.loc[1,col]=filepath.name+'_'+df.loc[1,col].replace(' ','')
                                else:
                                        pass
                        for index in df.index:
                                if index<3:
                                        pass
                                elif df.loc[index,indexcol]=='':
                                        for numcol in itemnumcol:
                                                Itemnum=df.loc[index,numcol]
                                                if Itemnum != '':
                                                        Name=df.loc[1,numcol]
                                                        Item=df.loc[index,indexcol+1]
                                                        collect.loc[index_collect]=[Name,Item,Itemnum,filepath.name]
                                                        index_collect+=1
                                                else:
                                                        pass
                                else:
                                        pass
                                                        
                else:
                        pass
                print(collect)
        return statuscode,collect
