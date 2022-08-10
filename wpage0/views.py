from django.shortcuts import render
from django.http import HttpResponse
from elasticsearch.client import Elasticsearch
import time
es = Elasticsearch([{'host':'127.0.0.1','port':9200}], timeout=3600)

def history(sth):
    t = time.localtime()
    tim=str(t.tm_mon)+'月'+str(t.tm_mday)+'日 '+str(t.tm_hour)+'时'
    i={'time0':tim,'txt':sth}
    query={"query" : {"match_all" : {}}}
    params = {"ignore_unavailable": "true"} 
    res2 = es.search(index="history", body=query,params=params)
    num=res2['hits']['total']['value']+1
    res2 = es.index(index="history", id=num,document=i)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.
def page0(request):
    s='1.html'
    if request.method == 'POST':
        s=request.POST.get('imsg')
        if s==None:#代表当前界面不是基础初始搜索界面
            na=request.POST.get('name')
            ttit=request.POST.get('title')
            ttot=request.POST.get('tot')
            more=request.POST.get('more')
            pho=request.POST.get('phone')
            
            sth="高级搜索—— 名称:"+na+", 部门:"+ttit+", 机构:"+ttot+", 其他:"+more+", 联系方式"+pho
            history(sth)
            query = {"query": {"match":{"name" : na}}}
        # 若对应查询栏为空，则忽略这一信息的约束，只对其他内容进行查询
            if (len(na)!=0 and len(ttit)==0 and len(ttot)==0):  # 仅指定了收件人
                query = {"query": {"match_phrase":{"name" : na}},"size":  20}
            if (len(na)==0 and len(ttit)!=0 and len(ttot)==0):  # 仅指定了收件人
                query = {"query": {"match_phrase":{"title" : ttit}},"size":  20} 
            if (len(na)==0 and len(ttit)==0 and len(ttot)!=0): # 仅指定了邮件主题
                query = {"query": {"match_phrase":{"tot" : ttot}},"size":  20} 
                
            if (len(na)!=0 and len(ttit)!=0 and len(ttot)==0):  # 仅指定了收发人
                query = {"query": {"bool":{"must":[ {"match_phrase":{"name" : na}},{"match_phrase":{"title" : ttit}} ] }},"size":  20}
            if (len(na)!=0 and len(ttit)==0 and len(ttot)!=0): # 仅指定了发件人和主题
                query = {"query": {"bool":{"must":[ {"match_phrase":{"name" : na}},{"match_phrase":{"tot" : ttot}} ] }},"size":  20}
            if (len(na)==0 and len(ttit)!=0 and len(ttot)!=0): 
                query = {"query": {"bool":{"must":[ {"match_phrase":{"title" : ttit}},{"match_phrase":{"tot" : ttot}} ] }},"size":  20}
            if (len(na)!=0 and len(ttit)!=0 and len(ttot)!=0):
                query = {"query":{"bool":{"must":[ {"match_phrase":{"name" : na}},{"match_phrase":{"title" : ttit}},{"match_phrase":{"tot" : ttot}} ] }},"size":  20}
            if(len(pho)!=0):
                query = {"query": {"match_phrase":{"phone" : pho}},"size":  20}
            if(len(more)!=0):
                query = {"query": {"match_phrase":{"more" : more}},"size":  20}
            params = {"ignore_unavailable": "true"} 
            res = es.search(index="web1", body=query,params=params)
            num=1
            if len(res['hits']['hits'])!=0:
                num=res['hits']['hits'][0]['_source']['num']
            m_data=[]
            for ri in res['hits']['hits']:
                x=ri['_source']
                strx='/static/web_img'
                spx=''.join(x['img'].split())
                if spx=='none':
                    strx+='/nk.jpg'
                else:
                    strx+=x['img'].replace('C:/Users/Lenovo/web_img','')
                x['img']=strx
                m_data.append(x)
            #print(res['hits']['hits'])
            #print("进入高级搜索界面，姓名为：%s，电话为"%na)
            #print(pho)
            #s=str(num)+'.html'
            return render(request,'0gd.html',{'order':m_data})
            
            
        else:#代表当前界面是初始界面
            s=request.POST.get('imsg')
            sth="普通搜索——搜索内容:"+s
            history(sth)
            query = {"query":{"bool":{"should":[ {"match":{"name" : s}},{"match":{"title" : s}},
                                            {"match":{"tot" : s}},{"match":{"more" : s}} ] }},"size":20}
                
            if '*' in s:
                query = {"query":{"bool":{"should":[ {"wildcard":{"name.keyword" : s}},
                        {"wildcard":{"title.keyword" : s}},{"wildcard":{"tot.keyword" : s}},
                        {"wildcard":{"more.keyword" : s}} ] }},"size":20}
                
            params = {"ignore_unavailable": "true"} 
            res = es.search(index="web1", body=query,params=params)
            m_data=[]
            for ri in res['hits']['hits']:
                x=ri['_source']
                strx='/static/web_img'
                spx=''.join(x['img'].split())
                if spx=='none':
                    strx+='/nk.jpg'
                else:
                    strx+=x['img'].replace('C:/Users/Lenovo/web_img','')
                x['img']=strx
                m_data.append(x)
            return render(request,'0gd.html',{'order':m_data})
            #s=str(num)+'.html'
            #print("输入的内容是：%s"%s)
    else:
        s='1.html'
    return render(request,s)
