from django.shortcuts import render
from . import EXCELconvert
import pandas as pd
import openpyxl  
import time
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpRequest, FileResponse
import json
from django.http import JsonResponse
from sqlalchemy import create_engine
engine = create_engine('sqlite:///db.sqlite3', echo=True)

# Create your views here.
def index(request):
    return render(request,'APP2_Comparison/index.html')

def uploads(request):
    df = pd.DataFrame()
    dfx = pd.DataFrame()
    df_t = pd.DataFrame()
    BOQNUMS=0
    nosupport=[]#没有支持的产品
    errorcode1=[]#没有定位行
    hotfind=[]#找到相似爆款
    hotcontain={}#完全包含相似爆款
    Description_dict={}#描述字典
    productlist=['流水单','套餐']
    info_SHOW_BIGTYPES=['Staple','Snack','Dessert_Drink']
    repolist = ['HOT','BIG']

    if request.POST:
        files = request.FILES.getlist('UploadForm[excelFiles][]')
        noSelect = request.POST.get('noSelect').split(',')
        repolist = request.POST.get('Repo').split(',')
 
        for f in files:
            dfx=pd.read_excel(f)
            if ('名称' in dfx.columns) and ('编码' in dfx.columns) and ('数量' in dfx.columns):
                dfx['filename']=f.name
                break
            dfx = pd.DataFrame()

            BOQNUMS+=1
            statuscode,df_t = EXCELconvert.EXCELconvert(f,productlist)
            if (statuscode==0) and len(df_t)>0:
                df=pd.concat([df,df_t])
            elif (statuscode==0) and len(df_t)==0:
                nosupport.append(f.name)
            elif statuscode==1:
                errorcode1.append(f.name)
            else:
                pass
        if len(dfx)>0:
            df=dfx
    
    HTML={}
    for filename in nosupport:
        HTML[filename]={'status_detail':'这个文件中没有找到流水单'}
    for filename in errorcode1:
        HTML[filename]={'status_detail':'缺少定位行'}
    info_category = pd.read_sql("SELECT * FROM APP1_LPsplit_ITEM_CATEGORY",engine)
    df.rename(columns={'名称':'Name','编码':'Item','数量':'Qty'},inplace=True)
    if len(df)>0:
        df1=pd.merge(df,info_category,how='left').fillna('unknow')
    else:
        HTML['All_files']={'status_detail':'您所上传的文件中没有找到流水单。'}
        return JsonResponse(json.dumps(HTML),safe=False)     

    #准备比对的对象，sql hotconf并准备宽表
    sql_hot="SELECT * FROM APP2_HotConf where"
    for repo in repolist:
        sql_hot+=" Repo=='"+repo+"' or"
    sql_hot=sql_hot[:-3]
    df_hot = pd.read_sql(sql_hot,engine).sort_values(by=['Name','Item'])
    df_hot=pd.merge(df_hot,info_category,how='left').fillna('unknow')
    hot_cases=df_hot[(df_hot['机箱']!='N') & (df_hot['机箱']!='unknow')].set_index('Name')
    df2=pd.DataFrame(index=hot_cases.index,columns=info_SHOW_BIGTYPES).fillna('')
    df2['conf']=''
    for indexs in df_hot.index:
        ITEMNUMS=int(df_hot.loc[indexs,'Qty'])
        APPENDITEM=str(df_hot.loc[indexs,'Item'])+'*'+str(ITEMNUMS)
        if APPENDITEM not in Description_dict:
            Description_dict[APPENDITEM]=df_hot.loc[indexs,'Item_Description']
        #写入df2
        Big_Category=df_hot.loc[indexs,hot_cases.loc[df_hot.loc[indexs,'Name'],'机箱']]
        if(Big_Category in info_SHOW_BIGTYPES):         
            df2.loc[df_hot.loc[indexs,'Name'],Big_Category]+=APPENDITEM+';'
        else:
            df2.loc[df_hot.loc[indexs,'Name'],'其他']+=APPENDITEM+';'
        if df_hot.loc[indexs,'机箱']!='N' and df_hot.loc[indexs,'机箱']!='unknow':
            df2.loc[df_hot.loc[indexs,'Name'],'机箱']+=APPENDITEM+';'
        elif df_hot.loc[indexs,'电源']=='Y':
            df2.loc[df_hot.loc[indexs,'Name'],'电源']+=APPENDITEM+';'
        elif df_hot.loc[indexs,'CPU']=='Y':
            df2.loc[df_hot.loc[indexs,'Name'],'CPU']+=APPENDITEM+';'
        elif df_hot.loc[indexs,'硬盘']=='Y':
            df2.loc[df_hot.loc[indexs,'Name'],'硬盘']+=APPENDITEM+';'
        elif df_hot.loc[indexs,'PCIe卡']=='Y':
            df2.loc[df_hot.loc[indexs,'Name'],'PCIe卡']+=APPENDITEM+';'
        else:
            pass           
        df2.loc[df_hot.loc[indexs,'Name'],'conf']+=APPENDITEM+';' 
    df2['Repo']=hot_cases['Repo']
    df2['Product']=hot_cases['机箱']

    #准备用户数据宽表
    info_CONF=df1[(df1['机箱']!='N') & (df1['机箱']!='unknow')].set_index('Name')
    df1_all=df1[df1['Name'].isin(info_CONF.index)]
    df1_=df1_all.copy().sort_values(by=['Name','Item'])#注意按Item排序
    print(info_CONF)
    #info_CONF里面重塑Configuration_ID,然后整合到df1_里
    df3=pd.DataFrame(index=info_CONF.index,columns=info_SHOW_BIGTYPES).fillna('')
    df3['conf']=''
    for indexs in df1_.index:
        kitnum=int(info_CONF.loc[df1_.loc[indexs,'Name'],'Qty'])
        ITEMNUMS=int(df1_.loc[indexs,'Qty'])/kitnum
        if df1_.loc[indexs,'Qty']%kitnum==0:ITEMNUMS=int(ITEMNUMS) 
        df1_.loc[indexs,'Qty']=ITEMNUMS
        APPENDITEM=str(df1_.loc[indexs,'Item'])+'*'+str(ITEMNUMS)
        if APPENDITEM not in Description_dict:
            Description_dict[APPENDITEM]=df1_.loc[indexs,'Item_Description']
        #写入df3
        Big_Category=df1_.loc[indexs,info_CONF.loc[df1_.loc[indexs,'Name'],'机箱']]
        if(Big_Category in info_SHOW_BIGTYPES):         
            df3.loc[df1_.loc[indexs,'Name'],Big_Category]+=APPENDITEM+';'
        else:
            df3.loc[df1_.loc[indexs,'Name'],'其他']+=APPENDITEM+';' 
        if df1_.loc[indexs,'机箱']!='N' and df1_.loc[indexs,'机箱']!='unknow':
            df3.loc[df1_.loc[indexs,'Name'],'机箱']+=APPENDITEM+';'
        elif df1_.loc[indexs,'电源']=='Y':
            df3.loc[df1_.loc[indexs,'Name'],'电源']+=APPENDITEM+';'
        elif df1_.loc[indexs,'CPU']=='Y':
            df3.loc[df1_.loc[indexs,'Name'],'CPU']+=APPENDITEM+';'
        elif df1_.loc[indexs,'硬盘']=='Y':
            df3.loc[df1_.loc[indexs,'Name'],'硬盘']+=APPENDITEM+';'
        elif df1_.loc[indexs,'PCIe卡']=='Y':
            df3.loc[df1_.loc[indexs,'Name'],'PCIe卡']+=APPENDITEM+';'
        else:
            pass 
        df3.loc[df1_.loc[indexs,'Name'],'conf']+=APPENDITEM+';'
    df3['Product']=info_CONF['机箱']
    df3['filename']=info_CONF['filename']
    df3['Qty']=info_CONF['Qty']
    df3.index+='有'+df3['Qty'].astype(str)+'台'
    df3.index.name='Name'

    #筛掉用户不关心的部件
    df2=df2.drop(columns=noSelect,errors='ignore') 
    df3=df3.drop(columns=noSelect,errors='ignore') 
    info_SHOW_BIGTYPES= [i for i in info_SHOW_BIGTYPES if i not in noSelect] 

    #所有配置比对Repo，计算距离
    df_dis = pd.DataFrame(index=df3.index,columns=df2.index)
    WEIGHT={'CPU': 0.5,'内存':0.24,'硬盘':0.12,'基本配置':0.06,'PCIe卡':0.03,'RAID卡':0.014,'网卡':0.007}
    for i in df_dis.index:
        for j in df_dis.columns:
            if df3.loc[i,'机箱'] != df2.loc[j,'机箱']:
                df_dis.loc[i,j]=999999
                continue
            elif (('CPU' not in noSelect) and ('内存' not in noSelect) and ('硬盘' not in noSelect) and (df3.loc[i,'CPU'] != df2.loc[j,'CPU']) and (df3.loc[i,'内存'] != df2.loc[j,'内存']) and (df3.loc[i,'硬盘'] != df2.loc[j,'硬盘'])):
                df_dis.loc[i,j]=999999
                continue
            DIFF=0
            for p in info_SHOW_BIGTYPES:                  
                    try:
                        W=WEIGHT[p]
                    except KeyError:
                        W=0.0001
                    if df3.loc[i,p] != df2.loc[j,p]:
                        DIFF+=1+W
            df_dis.loc[i,j]=DIFF
    df_dis['Product']=df3['Product']
    df_dis['filename']=df3['filename']
    #逐个repo筛选最近的hot
    output=df3.reset_index().copy()
    output['neariest']=''
    output['neariest_dis']=999999
    output['Father_ID']=0
    neariest_hot=pd.DataFrame(index=range(len(output)*len(repolist)),columns=output.columns)
    neariest_hot['neariest_dis']=999999
    neariest_hot_index=0
    for repo in repolist:
        hotname=hot_cases[hot_cases['Repo']==repo].index.tolist()
        df_dis_t=df_dis[[i for i in df_dis.columns if i in hotname]]
        for index in output.index:
            name=output.loc[index,'Name']
            for hot in hotname:
                if df_dis_t.loc[name,hot]<neariest_hot.loc[index,'neariest_dis']:
                    neariest_hot.loc[neariest_hot_index,'Name']=hot
                    neariest_hot.loc[neariest_hot_index,'neariest_dis']=df_dis_t.loc[name,hot]
                    neariest_hot.loc[neariest_hot_index,'Father_ID']=name
                    hotfind.append(name)
                    neariest_hot.loc[neariest_hot_index,'filename']=output.loc[index,'filename']
                    neariest_hot.loc[neariest_hot_index,'Product']=output.loc[index,'Product']
            neariest_hot_index+=1   
    #确定每个配置最近的hot
    for index in output.index:
        output.loc[index,'neariest_dis']=neariest_hot[neariest_hot['Father_ID']==output.loc[index,'Name']]['neariest_dis'].min()
    output=output.fillna(value={'neariest_dis':'inf'})
    #填补neariest_hot的部件,判断爆款是否被完全包含
    neariest_hot=neariest_hot[neariest_hot['neariest_dis']!=999999]
    for index in neariest_hot.index:
        hotcontain_flag=1
        hot=neariest_hot.loc[index,'Name']
        neariest_hot.loc[index,'Name']+='_'+hot_cases.loc[hot,'Repo']
        for p in info_SHOW_BIGTYPES:
            neariest_hot.loc[index,p]=df2.loc[hot,p]
            if neariest_hot.loc[index,p]!=output[output['Name']==neariest_hot.loc[index,'Father_ID']].iloc[0][p]:
                hotcontain_flag=0
        if hotcontain_flag==1:
            hotcontain[neariest_hot.loc[index,'Father_ID']]=neariest_hot.loc[index,'Name']


    #整合输出json
    HTML['Description_dict']=Description_dict
    #每个文件的分析
    for filename in df3['filename'].drop_duplicates():
        html={}
        #有支持产品的正常BOQ
        output_f=output[(output['filename']==filename)]
        Confnum=len(output_f)
        Diffconfnum=len(output_f['conf'].drop_duplicates())
        status_detail='在文件'+filename+'中共解析了'+str(Confnum)+'个配置'
        if Diffconfnum != Confnum:
            status_detail+='其中不一样的配置有'+str(Diffconfnum)+'种。'
        html['status_detail']=status_detail
        #逐个产品去分析配置
        for product in productlist:
            product=product.replace(' ','_')
            output_t=output_f[output_f['Product']==product]
            #output_t['Name']=output_t['Name']+'有'+output_t['Qty'].astype(str)+'台;'
            neariest_hot_t=neariest_hot[(neariest_hot['filename']==filename)&(neariest_hot['Product']==product)]
            if len(output_t)>0:
                #重做配型ID，合并相同配置
                output_tt=output_t.drop_duplicates(subset=['conf'])
                output_tt=output_tt.reset_index(drop=True)
                if len(output_tt)!=len(output_t):
                    #BOQ里存在完全相同的配置,把他们整合                       
                    for index in output_tt.index:
                        neariest_hot_tt=neariest_hot_t[neariest_hot_t['Father_ID']==output_tt.loc[index,'Name']]
                        output_tt.loc[index,'Name']=output_t[output_t['conf']==output_tt.loc[index,'conf']]['Name'].str.cat(sep=';')
                        output_tt.loc[index,'Qty']=output_t[output_t['conf']==output_tt.loc[index,'conf']]['Qty'].sum()
                        if len(neariest_hot_tt)>0:
                            for index1 in neariest_hot_tt.index:
                                neariest_hot_t.loc[index1,'Father_ID']=output_tt.loc[index,'Name']
                output_t=output_tt
                output_t=output_t.reset_index()
                output_t['index']=output_t['index']+1
                if len(neariest_hot_t)>0:
                    neariest_hot_t=neariest_hot_t.reset_index()
                    for index in neariest_hot_t.index:
                        neariest_hot_t.loc[index,'index']=neariest_hot_t.loc[index,'Name']
                        output_tt=output_t[output_t['Name']==neariest_hot_t.loc[index,'Father_ID']]
                        if len(output_tt)>0:
                            neariest_hot_t.loc[index,'Father_ID']=output_tt.iloc[0]['index']
                        else:
                            neariest_hot_t=neariest_hot_t.drop([index])
                    output_t=pd.concat([output_t,neariest_hot_t]).rename(columns={'index':'配型ID','Name':'BOQnames'})
                else:
                    output_t=output_t.rename(columns={'index':'配型ID','Name':'BOQnames'})
                
                Qty = output_t['Qty']
                neariest_dis=output_t['neariest_dis']
                output_t.drop(labels=['Qty','neariest_dis'], axis=1,inplace = True)
                output_t.insert(1, '台套数', Qty)
                #output_t.insert(2, '最小差异', neariest_dis)
                output_t=output_t.fillna('')

                #删掉空的列
                for p in info_SHOW_BIGTYPES:
                    if sum(output_t[p]!='')==0:                           
                        output_t=output_t.drop(p,axis=1)
                drop_list=['机箱','电源','CPU','硬盘','PCIe卡','neariest','filename','conf','Product']
                for category in drop_list:
                    if category in output_t.columns:
                        output_t=output_t.drop(category,axis=1)                  
                html[product]=output_t.to_json(orient='records')
                #展示表头顺序
                order=output_t.columns.tolist()
                order=[i for i in order if i not in ['BOQnames','Father_ID']]
                html[product+'_order']=order
        HTML[filename]=html        
    #整体分析报告
    html={}
    Confnum=len(output)
    Diffconfnum=len(output['conf'].drop_duplicates())
    status_detail='您共上传了'+str(BOQNUMS)+'份文件BOQ，解析出了'+str(Confnum)+'个配置；其中不一样的配置有'+str(Diffconfnum)+'种。<br>'
    '''
    if len(hotfind)>0:
        status_detail+='搜索到相似爆款的配置有：<br>'
        for f in hotfind:
            status_detail+= f
            status_detail+=';<br>'
    if len(hotcontain)>0:
        status_detail+='搜索到完全包含了某爆款的配置有：<br>'
        for key in hotcontain.keys:
            status_detail+= key+'完全包含了：'+hotcontain[key]
            status_detail+=';<br>'
    '''
    if len(nosupport)>0:
        status_detail+='没有可支持的产品的文件有：<br>'
        for f in nosupport:
            status_detail+= f
            status_detail+=';<br>'
    if len(errorcode1)>0:
        status_detail+='非标准BOQ,没有找到定位行的文件有：<br>'
        for f in errorcode1:
            status_detail+= f
            status_detail+=';<br>'
    html['status_detail']=status_detail
    for product in productlist:
        product=product.replace(' ','_')
        output_t=output[output['Product']==product]
        neariest_hot_t=neariest_hot[(neariest_hot['Product']==product)]
        if len(output_t)>0:
            #重做配型ID，合并相同配置
            output_tt=output_t.drop_duplicates(subset=['conf'])
            output_tt=output_tt.reset_index(drop=True)
            if len(output_tt)!=len(output_t):
                #BOQ里存在完全相同的配置,把他们整合
                for index in output_tt.index:
                    neariest_hot_tt=neariest_hot_t[neariest_hot_t['Father_ID']==output_tt.loc[index,'Name']]
                    output_tt.loc[index,'Name']=output_t[output_t['conf']==output_tt.loc[index,'conf']]['Name'].str.cat(sep=';')
                    output_tt.loc[index,'Qty']=output_t[output_t['conf']==output_tt.loc[index,'conf']]['Qty'].sum()
                    if len(neariest_hot_tt)>0:
                        for index1 in neariest_hot_tt.index:
                            neariest_hot_t.loc[index1,'Father_ID']=output_tt.loc[index,'Name']
            output_t=output_tt
            output_t=output_t.reset_index()
            output_t['index']=output_t['index']+1
            if len(neariest_hot_t)>0:
                neariest_hot_t=neariest_hot_t.reset_index()
                for index in neariest_hot_t.index:
                    neariest_hot_t.loc[index,'index']=neariest_hot_t.loc[index,'Name']
                    output_tt=output_t[output_t['Name']==neariest_hot_t.loc[index,'Father_ID']]
                    if len(output_tt)>0:
                        neariest_hot_t.loc[index,'Father_ID']=output_tt.iloc[0]['index']
                    else:
                        neariest_hot_t=neariest_hot_t.drop([index])
                output_t=pd.concat([output_t,neariest_hot_t]).rename(columns={'index':'配型ID','Name':'BOQnames'})
            else:
                output_t=output_t.rename(columns={'index':'配型ID','Name':'BOQnames'})
            
            Qty = output_t['Qty']
            neariest_dis=output_t['neariest_dis']
            output_t.drop(labels=['Qty','neariest_dis'], axis=1,inplace = True)
            output_t.insert(1, '台套数', Qty)
            #output_t.insert(2, '最小差异', neariest_dis)
            output_t=output_t.fillna('')

            #删掉空的列
            for p in info_SHOW_BIGTYPES:
                if sum(output_t[p]!='')==0:                           
                    output_t=output_t.drop(p,axis=1)
            drop_list=['机箱','电源','CPU','硬盘','PCIe卡','neariest','filename','conf','Product']
            for category in drop_list:
                if category in output_t.columns:
                    output_t=output_t.drop(category,axis=1)                  
            html[product]=output_t.to_json(orient='records')
            #展示表头顺序
            order=output_t.columns.tolist()
            order=[i for i in order if i not in ['BOQnames','Father_ID']]
            html[product+'_order']=order
    HTML['All_files']=html
    
    return JsonResponse(json.dumps(HTML),safe=False)

def downloadexample(request):
    
    file=open('APP2_Comparison/appfiles/examples.zip','rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="examples.zip"'
    return response