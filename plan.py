# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.


产品当前最新的相关信息：




    产品择时策略比例
    产品对冲策略比例




    产品净资产  product_assets
    股票账户资产 stock_account
    可用（取）资金 stock_account-stock_value
    多头市值    stock_value
    
    期货账户资产 future_account
    期货市值    future_value
    占用保证金   used_margin
    可用资金    future_account-used_margin
    风险度      risk_degree
    期货持仓（IC) IC_n
    IC合约价格    IC_p 
    期货持仓（IF)  IF_n
    IF合约价格     IF_p
    期货持仓（IH)  IH_n
    IH合约价格    IH_p
    
    股票资产占比  stock_account_ratio
    期货资产占比  future_account_ratio
    净敞口比例    net_exposure
    
    产品净资产变动 product_assets_change

当前  now
目标  target


"""

import numpy as np

now_product_assets=19294000
now_stock_account=11292700
now_stock_value=11250100
    
now_future_account=8001300
now_future_value=-1037900
now_used_margin=322000


def riskdegree(future_value,future_account,margin_ratio=0.31):   # 计算风险度
    return (future_value*margin_ratio/future_account)

def netexposure():                                               #计算净敞口
    
now_risk_degree=riskdegree(now_future_value,now_future_account)
now_IC_n=-1
now_IC_p=1032500  # IC1807 0717

    
now_stock_account_ratio=now_stock_account/now_product_assets
now_future_account_ratio=now_future_account/now_product_assets
now_net_exposure=(now_stock_value+now_future_value)/now_product_assets
    
now_product_assets_change=5000000

当前  now
目标  target

margin_ratio=0.31

target_product_assets=now_product_assets-now_product_assets_change
target_stock_account=
target_stock_value=
    
target_future_account=
target_future_value=
target_used_margin=

    
target_risk_degree=0.75
target_IC_n=
target_IC_p=1032500
target_stock_account_ratio
target_future_account_ratio
target_net_exposure=



#  求解  目标敞口-0.5 情况下，期货风险度 在 0.73 到 0.78之间的 股票资产占比

def riskdegree_ratio(target_risk_degree,target_product_assets,stockratio=1,target_IC_p=1032500,margin_ratio=0.31):
    n=int(target_product_assets/target_IC_p)
    target_IC_list=range(int(-1.5*n),int(n))
    stockratio=1
    datadir={}
    datalist=[]
    for target_IC_n in target_IC_list:
        target_future_account=np.abs(target_IC_n)*target_IC_p*margin_ratio/target_risk_degree
        target_stock_account=target_product_assets-target_future_account
        target_stock_value=target_stock_account*stockratio
        target_net_exposure=(target_stock_value+target_IC_n*target_IC_p)/target_product_assets
        stock_account_ratio=target_stock_account/target_product_assets
        datadir[target_net_exposure+0.5]=[target_net_exposure,target_IC_n,stock_account_ratio]
        datalist.append(target_net_exposure+0.5)
#        print(target_net_exposure,target_IC_n,stock_account_ratio)

    b=list(np.square(datalist))
    index_min=datalist[b.index(np.min(b))]
    target_net_exposure,target_IC_n,best_stock_account_ratio=datadir[index_min]
    return best_stock_account_ratio,target_net_exposure,target_IC_n



    
    
    
输入  目标 资产比例
输入  当前股票市值
net_exposure_list=[-0.5,0,0.25,0.5,1,1.5]

def calculate(product_assets,stock_account_ratio,stockratio,IC_p=1032500,margin_ratio=0.31):
    stock_value=product_assets*stock_account_ratio*stockratio
    n=int(product_assets/IC_p)
    IC_list=range(int(-1.5*n),int(1.3*n))
    stock_account=product_assets*stock_account_ratio
    stock_value=stock_account*stockratio
    future_account=product_assets-stock_account
    datab=np.zeros((len(IC_list),5))
    key=0
    for IC_n in IC_list:
        future_value=IC_n*IC_p
        risk_degree=np.abs(future_value*margin_ratio)/future_account
        net_exposure=(stock_value+future_value)/product_assets

    #        print(target_net_exposure,target_IC_n,stock_account_ratio)
        datab[key]=[IC_n,net_exposure,risk_degree,stockratio,stock_account_ratio]
        key=key+1
    return datab

for a in range(5):
    target_risk_degree=0.73+0.01*a
    
    stock_account_ratio,target_net_exposure,target_IC_n=riskdegree_ratio(target_risk_degree,target_product_assets,
                                                stockratio=1,target_IC_p=1032500,margin_ratio=0.31)
    for i in range(6):
        stockratio=0.95+i*0.01
        datab=calculate(product_assets,stock_account_ratio,stockratio,IC_p=1032500,margin_ratio=0.31)
        datadf=pd.DataFrame(datab)
        print('*'*18)
        print(datadf)
        print('*'*18)
import pandas as pd
pd.DataFrame(datab)
#评价函数 
def evaluate(datab):
         # 评价是否 资产比例是否合理  就是  在 股票仓位 95%-100% 中 是否能比较准确地调整到 目标敞口
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


              




   
    