# _*_coding: utf-8 _*_

from django.shortcuts import render
from django.http import JsonResponse
from sqlalchemy import create_engine
import pandas as pd
import pulp
import json
# Get product df ITEM_CATEGORY
engine = create_engine('sqlite:///db.sqlite3', echo=True)
ITEM_CATEGORY = pd.read_sql("SELECT * FROM APP1_LP_ITEM_CATEGORY",engine).fillna('')

def Index(request):
    return render(request,'APP1_LP/index.html')

def Staple(request):
    # Give all staple directly for choose
    Staple = ITEM_CATEGORY[ITEM_CATEGORY['ITEM_CATEGORY']=='Staple'] 
    list = []
    for index in Staple.index:
        list.append({'id':str(index),'name':str(Staple.loc[index,'ITEM_DESCRIPTION'])})   
    return JsonResponse({'data':list})

def Price(request):
    # Give all price.dropduplicates directly for choose
    Price = pd.DataFrame(ITEM_CATEGORY[ITEM_CATEGORY['ITEM_CATEGORY']=='Staple']['PRICE'].drop_duplicates().sort_values())
    list = []
    for index in Price.index:
        list.append({'id':str(index),'name':str(Price.loc[index,'PRICE'])})
    return JsonResponse({'data':list})

def StapleSelected(request,id):
    # When cilcking on a staple, get the price
    Price = ITEM_CATEGORY.loc[int(id),'PRICE']
    list = []
    list.append({'id':str(Price),'name':str(Price)})
    return JsonResponse({'data':list})

def PriceSelected(request,id):
    # When cilcking on a price, get the stape
    Price = ITEM_CATEGORY.loc[int(id),'PRICE']
    Staple = ITEM_CATEGORY[(ITEM_CATEGORY['ITEM_CATEGORY']=='Staple') & (ITEM_CATEGORY['PRICE']==Price)]
    list = []
    for index in Staple.index:
        list.append({'id':str(index),'name':str(Staple.loc[index,'ITEM_DESCRIPTION'])})  
    return JsonResponse({'data':list})

def StapleRecommand(index):
    # Select the staple must have
    STAPLE_RECOMMEND = pd.DataFrame(columns=['ITEM_CATEGORY','ITEM','ITEM_DESCRIPTION','Qty','PRICE'])
    STAPLE_RECOMMEND.loc[0] = [ITEM_CATEGORY.loc[index,'ITEM_CATEGORY'],ITEM_CATEGORY.loc[index,'ITEM'],ITEM_CATEGORY.loc[index,'ITEM_DESCRIPTION'],1,ITEM_CATEGORY.loc[index,'PRICE']]
    return STAPLE_RECOMMEND

def RandRecommand(TTPay):
    # Main recommand function
    RAND_RECOMMAND = pd.DataFrame(columns=['ITEM_CATEGORY','ITEM','ITEM_DESCRIPTION','Qty','PRICE'])
    RAND_RECOMMAND_INDEX = 0
    # Using rand 50% of the choices everytime
    ITEM_CATEGORY_T = ITEM_CATEGORY[ITEM_CATEGORY['ITEM_CATEGORY']!='Staple'].sample(frac=0.5)
    model = pulp.LpProblem("Rand Food", pulp.LpMinimize)
    var = {}
    aim = ''
    TTPRICE = ''
    TTNums = ''
    for index in ITEM_CATEGORY_T.index:
        var[index] = pulp.LpVariable(str(index), lowBound=0, cat='Integer')
        TTPRICE += ITEM_CATEGORY_T.loc[index,'PRICE'] * var[index]
        TTNums += var[index]
        model += var[index] <=2
    model += TTPay - TTPRICE    
    model += TTPRICE <= TTPay
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
    RAND_RECOMMAND=RAND_RECOMMAND.sort_values(by=['ITEM_CATEGORY','ITEM'])
    return RAND_RECOMMAND

def Recommend(request):  
    Staple = ''
    TTPay = ''
    pack = '' 

    # Get request
    if request.POST:
        Staple = request.POST.get('Staple')
        TTPay = request.POST.get('TTPay')
        pack = request.POST.get('pack')
    
    Recommend_CONF = pd.DataFrame(columns=['ITEM_CATEGORY','ITEM','ITEM_DESCRIPTION','Qty','PRICE'])
    Recommend_SUMMARY = {'TTPay':0}

    # if need packm, add at first
    if pack == '1':
        Recommend_CONF.loc[len(Recommend_CONF)]=['Others','pack','package cost',1,1.5]
        TTPay = float(TTPay)-1.5

    # Get selected staple
    if Staple!= '' and Staple!= None:
        STAPLE_RECOMMEND = StapleRecommand(int(Staple))
        Recommend_CONF = pd.concat([Recommend_CONF,STAPLE_RECOMMEND])
        TTPay = float(TTPay)-float(STAPLE_RECOMMEND.loc[0,'PRICE'])

    # Rand recommend with price limination
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
        html['Html_Status_Detail']='Cannot satisfy you'
    html['Html_Recommend_CONF']=Recommend_CONF.to_json(orient='records')   
    html['Html_Recommend_SUMMARY']=Recommend_SUMMARY
    return JsonResponse(json.dumps(html),safe=False)