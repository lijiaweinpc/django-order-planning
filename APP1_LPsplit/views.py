# _*_coding: utf-8 _*_

from django.shortcuts import render
from django.http import JsonResponse
from sqlalchemy import create_engine
import pandas as pd
import pulp
import json
#取出产品数据基表ITEM_CATEGORY
engine = create_engine('sqlite:///db.sqlite3', echo=True)
ITEM_CATEGORY = pd.read_sql("SELECT * FROM APP1_LPsplit_ITEM_CATEGORY",engine).fillna('')

def Index(request):
    return render(request,'APP1_LPsplit/index.html')

def Staple(request):
    Staple = ITEM_CATEGORY[ITEM_CATEGORY['ITEM_CATEGORY']=='Staple']  
    list = []
    for index in Staple.index:
        list.append({'id':str(index),'name':str(Staple.loc[index,'ITEM_DESCRIPTION'])})
    return JsonResponse({'data':list})

def StapleSelected(request,id):
    ITEM = ITEM_CATEGORY.loc[int(id),'ITEM']
    PRICE = ITEM_CATEGORY.loc[int(id),'PRICE']
    list = []
    list.append({'ITEM_ID':str(ITEM),'ITEM_NAME':str(ITEM),'PRICE_ID':str(PRICE),'PRICE_NAME':str(PRICE)})
    return JsonResponse({'data':list})

def StapleRecommand(Staple,Qty):
    STAPLE_RECOMMEND = pd.DataFrame(columns=['ITEM_CATEGORY','ITEM','ITEM_DESCRIPTION','Qty','PRICE'])
    if Staple!='':
        STAPLE_RECOMMEND.loc[0] = [ITEM_CATEGORY.loc[Staple,'ITEM_CATEGORY'],ITEM_CATEGORY.loc[Staple,'ITEM'],ITEM_CATEGORY.loc[Staple,'ITEM_DESCRIPTION'],Qty,ITEM_CATEGORY.loc[Staple,'PRICE']]
    return STAPLE_RECOMMEND

def RandRecommand(TTPay):
    RAND_RECOMMAND = pd.DataFrame(columns=['ITEM_CATEGORY','ITEM','ITEM_DESCRIPTION','Qty','PRICE'])
    RAND_RECOMMAND_INDEX = 0
    import random
    Rand_TTNums = random.randint(int(TTPay/ITEM_CATEGORY.PRICE.mean()),int(TTPay/ITEM_CATEGORY.PRICE.min()))
    ITEM_CATEGORY_T = ITEM_CATEGORY[ITEM_CATEGORY['ITEM_CATEGORY']!='Staple']
    model = pulp.LpProblem("MinCost", pulp.LpMinimize)
    var = {}
    aim = ''
    TTPRICE = ''
    TTNums = ''
    for index in ITEM_CATEGORY_T.index:
        #每个备选项是一个变量
        var[index] = pulp.LpVariable(str(index), lowBound=0, cat='Integer')
        #目标函数是总的价格最小
        aim += ITEM_CATEGORY_T.loc[index,'PRICE'] * var[index]
        #约束条件要用到总数量和总价格
        TTPRICE += ITEM_CATEGORY_T.loc[index,'PRICE'] * var[index]
        TTNums += var[index]
        model += var[index] <= 3
    model += aim     
    model += TTPRICE >= TTPay
    model += TTNums >= Rand_TTNums
    model.solve()
    status = pulp.LpStatus[model.status]

    for key in var:
        if status != 'Optimal':
            break
        elif var[key].varValue>0:
            RAND_RECOMMAND.loc[RAND_RECOMMAND_INDEX]=[ITEM_CATEGORY.loc[key,'ITEM_CATEGORY'],ITEM_CATEGORY.loc[key,'ITEM'],ITEM_CATEGORY.loc[key,'ITEM_DESCRIPTION'],var[key].varValue,ITEM_CATEGORY.loc[key,'PRICE']]
            RAND_RECOMMAND_INDEX += 1
        else:
            pass
    return RAND_RECOMMAND

def Recommend(request):  
    Staple = ''
    TTPay = '' 

    #接收用户的输入
    if request.POST:
        Staple = request.POST.get('Staple')
        TTPay = request.POST.get('TTPay')
    
    Recommend_CONF = pd.DataFrame()
    Recommend_SUMMARY = {'TTPay':0}
    #锁定Staple的选择
    if Staple!= '' and Staple!= None:
        STAPLE_RECOMMEND = StapleRecommand(int(Staple),1)
        Recommend_CONF = pd.concat([Recommend_CONF,STAPLE_RECOMMEND])
    #价格限制下的随机推荐
    if TTPay!= '' and TTPay!=None:
        RAND_RECOMMAND = RandRecommand(int(TTPay))
        if len(RAND_RECOMMAND)>0:
            Recommend_CONF = pd.concat([Recommend_CONF,RAND_RECOMMAND])

    html={}
    if(len(Recommend_CONF)>0):
        Recommend_SUMMARY['TTPay']=sum(Recommend_CONF['Qty']*Recommend_CONF['PRICE'])
        html['Html_Status'] = 'OK'
        html['Html_Status_Detail']='OK'
    else:
        html['Html_Status']='FAIL'
        html['Html_Status_Detail']='实在满足不了你'
    html['Html_Recommend_CONF']=Recommend_CONF.to_json(orient='records')   
    html['Html_Recommend_SUMMARY']=Recommend_SUMMARY
    return JsonResponse(json.dumps(html),safe=False)