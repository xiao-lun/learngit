# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 16:09:45 2018

@author: jiazheng.he






程序逻辑：
   输入相关数据
   解析当前产品情况
   计算目标情况

相关变量：

    产品择时策略比例  Timing_ratio
    产品对冲策略比例  Hedge_ratio


    产品净资产  product_assets
    股票账户资产 stock_account ；股票资产占比  stock_account_ratio 
    多头市值    stock_value
    
    期货账户资产 future_account ；期货资产占比  future_account_ratio
    期货市值    future_value
    占用保证金   used_margin
    风险度      risk_degree
    期货持仓（IC) IC_n
    IC合约价格    IC_p
    IC占用保证金比例   IC_margin
    期货持仓（IF)  IF_n
    IF合约价格     IF_p
    IF占用保证金比例   IF_margin
    净敞口比例    net_exposure
    
    产品净资产变动 product_assets_change
    
    对冲策略目标股票资产比例 Timing :T
    择时策略目标股票资产比例 Hedge :H
    

当前  now  :n
目标  target :t


产品分仓
具体	股票端策略加仓方案(试算）	                      	            策略市值占比	占股票调仓市值比例 策略市值 策略停牌市值
alpha	CSI300_All_A_NoSize300_SizeNeutTrade1.0_FinancialContraint	13.11%	19.84%
      CSI500_All_A_Temp7_SizeNeutTrade0.8                       	5.60%	   8.48%
	   CSI500_All_A_NoSize500_SizeNeutTrade0.8	                  16.26%	24.61%
	   CSI500_SizeTop50_NoSize500	                               	11.77%	17.81%
	   CSI500_SizeTop50_Temp7	                      	            19.33%	29.26%
总计		                                                         66.07%
		

假设股票端 都处于接近 满仓状态




【注意】
1.假设产品中 对冲标的为IF的策略 市值 就是 产品对冲端 对冲标的为IF的 全部股票市值。
所以根据 产品中 对冲标的为IF的 策略市值 可以计算出 属于对冲端的 IF手数
2.择时策略端 主要是使用IC合约来调整敞口，由于IC开仓的限制，所以不够的部分会使用IF 来 进行补充。



本代码使用到的变量 含义对照

product_assets
stock_account
stock_value
future_account
future_value


Hedge_ratio
H_t_stock_account_ratio
H_t_future_account_ratio
H_t_stock_account_ratio

Timing_ratio
T_t_stock_account_ratio
T_t_future_account_ratio

IC_margin
IC_n
IC_p

IF_margin
IF_n
IF_p

product_assets_change
t_product_assets
H_t_product_assets
H_t_stock_account

H_IF_strategy_assets
H_t_stock_account_IF
H_t_stock_account_IC
H_t_IC_n
H_IF_n


"""
import numpy as np
import pandas as pd

'''
择时和 对冲 的资产 参数配置
'''
                            #产品资产

Hedge_ratio=0.8                                    #对冲策略 资产比例
H_stock_account_ratio=0.72                       #对冲策略——目标——股票资产占比
H_future_account_ratio=1-H_stock_account_ratio #对冲策略——目标——期货资产占比



Timing_ratio=1-Hedge_ratio                                  #择时策略 资产比例
T_stock_account_ratio=0.59                           #择时策略——目标——股票资产占比
T_future_account_ratio=1-T_stock_account_ratio     #择时策略——目标——期货资产占比


# 输入


'''
产品股票和期货情况
'''
product_assets=16636700   
stock_account=11229300                       #产品股票账户资产
stock_value=11207300                         #股票市值
future_account=5401700                      #产品期货账户资产
future_value=-9320300                       #期货市值
margin=2581900                              #保证金
IC_margin=0.30                          #IC 保证金比例
IC_n=-7                                #IC 合约手数
IC_p=1000000                           #IC 价格
IF_margin=0.15                         #IF 保证金比例
IF_n=-2                                #IF 合约手数
IF_p=1000000                          #IF  价 格


H_product_assets=product_assets*Hedge_ratio  # 理论下 当前对冲端 产品资产
H_stock_account=H_product_assets*H_stock_account_ratio
IF_strategy_ratio=0.1469                    #
H_IF_strategy_assets=product_assets*IF_strategy_ratio
H_IC_strategy_assets=H_product_assets-H_IF_strategy_assets
H_IF_ratio=H_IF_strategy_assets/H_stock_account


                                    #对冲端  IF策略 和 IC策略 
nowinfo=pd.DataFrame({
        '产品名称':'骄阳',
        '总资产':product_assets,
        '股票账户资产':stock_account,
        '股票市值':stock_value,
        '期货账户权益':future_account,
        '期货市值':future_value,
        '股票资产占比':stock_account/product_assets,
        '期货资产占比':future_account/product_assets,
        '占用保证金':margin,
        '期货持仓IC':IC_n,
        '期货持仓IF':IF_n,
        'IC合约价格':IC_p,
        'IF合约价格':IF_p,
        },index=['now'])



'''
假设产品中 对冲标的为IF的策略 市值 就是 产品对冲端 对冲标的为IF的 全部股票市值。
所以根据 产品中 对冲标的为IF的 策略市值 可以计算出 属于对冲端的 IF手数

'''






H_product_assets=product_assets*Hedge_ratio   # 对冲端 目标 资产

H_stock_account=H_product_assets*H_stock_account_ratio #对冲端 目标 股票资产
H_future_account=H_product_assets*H_future_account_ratio

'''
 由于只有 对冲策略端存在 直接对应 IF的策略，所以根据对冲标的为IF的 策略市值 可以得到 对冲端 对应IF数量
'''

H_IF_strategy_assets=H_IF_ratio*H_stock_account
H_IF_n=np.round(-1*H_IF_strategy_assets/IF_p)  # 对冲端 对冲标的为IF 的部分 IF手数，遵循四舍五入
H_stock_account_IF= H_IF_strategy_assets             #  产品 中 用IF作为对冲标的的策略市值 就是 产品对冲端 对应IF 的全部产品   
H_stock_account_IC=H_stock_account-H_stock_account_IF   #对冲端——对应IF——目标资产


H_IC_n=np.round(-1*H_stock_account_IC/IC_p)        #对冲端——目标_IC手数
H_future_value=H_IF_n*IF_p+H_IC_n*IC_p              #对冲端——期货市值
H_marginvalue=np.abs(H_IC_n*IC_p*IC_margin)+np.abs(H_IF_n*IF_p*IF_margin)
H_netexposure=(H_stock_account+H_future_value)/H_product_assets



T_producassets=product_assets*Timing_ratio          #择时端 ——产品资产
T_stock_account=T_producassets*T_stock_account_ratio #择时端 ——目标股票账户资产
T_future_account=T_producassets*T_future_account_ratio #择时端 ——目标期货账户资产


T_IC_n=IC_n-H_IC_n       #择时端  ——IC 合约手数
T_IF_n=IF_n-H_IF_n        #择时端   ——IF 合约手数

T_future_value=T_IC_n*IC_p+T_IF_n*IF_p   # 择时端 ——期货市值
T_marginvalue=np.abs(T_IC_n*IC_p*IC_margin)+np.abs(T_IF_n*IF_p*IF_margin) # 择时端 ——保证金

T_netexposure=(T_stock_account+T_future_value)/T_producassets # 择时端——风险净敞口

netexposure=(H_stock_account+T_stock_account+T_future_value+H_future_value)/product_assets  # 产品 整体敞口

stock_account=H_stock_account+T_stock_account
stock_value=stock_account
future_account=T_future_account+H_future_account
future_value=T_future_value+H_future_value

risk_degree=(T_marginvalue+H_marginvalue)/future_account

['目标产品',product_assets,stock_account/product_assets,future_account/product_assets,
 stock_account,stock_value,future_account,future_value,T_marginvalue+H_marginvalue,IC_n,IF_n,risk_degree]


'''
'产品名称','目标产品资产','目标股票账户资产比例','目标期货账户资产比例','目标股票账户资产','目标股票市值',
'目标期货账户资产','目标期货市值','保证金','IC合约手数','IF合约手数','风险度','风险敞口
'''
d0=['产品总计',product_assets,stock_account/product_assets,future_account/product_assets,
 stock_account, stock_value,future_account,future_value,T_marginvalue+H_marginvalue,IC_n,IF_n,risk_degree,netexposure]

d1=['对冲端——总',H_product_assets,H_stock_account/H_product_assets,H_future_account/H_product_assets,
 H_stock_account,H_stock_account,H_future_account,H_future_value,H_marginvalue,H_IC_n,H_IF_n,H_marginvalue/H_future_account,H_netexposure]


d2=['对冲端——IF',np.nan,np.nan,np.nan,
 H_stock_account_IF,H_stock_account_IF,np.nan,H_IF_n*IF_p,np.abs(H_IF_n*IF_p*IF_margin),0,H_IF_n,np.nan,np.nan]

d3=['对冲端——IC',np.nan,np.nan,np.nan,
 H_stock_account_IC,H_stock_account_IC,np.nan,H_IC_n*IC_p,np.abs(H_IC_n*IC_p*IC_margin),H_IC_n,0,np.nan,np.nan]



d4=['择时端——总',T_producassets,T_stock_account/T_producassets,T_future_account/T_producassets,
 T_stock_account,T_stock_account,T_future_account,T_future_value,T_marginvalue,T_IC_n,T_IF_n,T_marginvalue/T_future_account,T_netexposure]



 
info=pd.DataFrame([d0,d1,d2,d3,d4],columns=['产品名称','目标产品资产','目标股票账户资产比例','目标期货账户资产比例','目标股票账户资产',
                   '目标股票市值','目标期货账户资产','目标期货市值','保证金','IC合约手数','IF合约手数','风险度','风险敞口'])



'''
产品资产变动之后 

'''




'''
输入
'''
product_assets_change=-5000000       #产品资产变动

nowinfo=pd.DataFrame({
        '产品名称':'骄阳',
        '总资产':product_assets,
        '股票账户资产':stock_account,
        '股票市值':stock_value,
        '期货账户权益':future_account,
        '期货市值':future_value,
        '股票资产占比':stock_account/product_assets,
        '期货资产占比':future_account/product_assets,
        '占用保证金':margin,
        '期货持仓IC':IC_n,
        '期货持仓IF':IF_n,
        'IC合约价格':IC_p,
        'IF合约价格':IF_p,
        '产品资产变化额':product_assets_change
        },index=['now'])



t_product_assets=product_assets+product_assets_change  # 出入金之后的产品 资产


t_H_product_assets=t_product_assets*Hedge_ratio   # 对冲端 目标 资产

t_H_stock_account=t_H_product_assets*H_stock_account_ratio #对冲端 目标 股票资产
t_H_future_account=t_H_product_assets*H_future_account_ratio

'''
 由于只有 对冲策略端存在 直接对应 IF的策略，所以根据对冲标的为IF的 策略市值 可以得到 对冲端 对应IF数量
'''

t_H_IF_strategy_assets=H_IF_ratio*t_H_stock_account

t_H_IF_n=np.round(-1*t_H_IF_strategy_assets/IF_p)  # 对冲端 对冲标的为IF 的部分 IF手数，遵循四舍五入
t_H_stock_account_IF= t_H_IF_strategy_assets             #  产品 中 用IF作为对冲标的的策略市值 就是 产品对冲端 对应IF 的全部产品   
t_H_stock_account_IC=t_H_stock_account-t_H_stock_account_IF   #对冲端——对应IF——目标资产


t_H_IC_n=np.round(-1*t_H_stock_account_IC/IC_p)        #对冲端——目标_IC手数
t_H_future_value=t_H_IF_n*IF_p+t_H_IC_n*IC_p              #对冲端——期货市值
t_H_marginvalue=np.abs(t_H_IC_n*IC_p*IC_margin)+np.abs(t_H_IF_n*IF_p*IF_margin)

t_H_netexposure=(t_H_stock_account+t_H_future_value)/t_H_product_assets



t_T_product_assets=t_product_assets*Timing_ratio          #择时端 ——产品资产
t_T_stock_account=t_T_product_assets*T_stock_account_ratio #择时端 ——目标股票账户资产
t_T_future_account=t_T_product_assets*T_future_account_ratio #择时端 ——目标期货账户资产


'''
择时端 指定净敞口 得出对应的 期货合约手数  和股票仓位

'''

t_T_netexposure=T_netexposure   # 保持原敞口 不变 ，择时端 ——假设目标风险净敞口
t_T_future_value=t_T_netexposure*t_T_product_assets-t_T_stock_account
t_T_IC_n=t_T_future_value/IC_p


'''
IC IF 开仓限制 逻辑
'''
if np.abs(t_T_IC_n)+np.abs(t_H_IC_n)>20:
    t_T_IF_n=(np.abs(t_T_IC_n)+np.abs(t_H_IC_n)-20)*t_T_IC_n/np.abs(t_T_IC_n)
    t_T_IC_n=(20-np.abs(t_H_IC_n))*t_T_IC_n/np.abs(t_T_IC_n)
else:
    t_T_IF_n=0
    t_T_IC_n=t_T_IC_n
    
    


t_T_future_value=t_T_IC_n*IC_p+t_T_IF_n*IF_p   # 择时端 ——期货市值
t_T_marginvalue=np.abs(t_T_IC_n*IC_p*IC_margin)+np.abs(t_T_IF_n*IF_p*IF_margin) # 择时端 ——保证金

tt_T_netexposure=(t_T_stock_account+t_T_future_value)/t_T_product_assets # 择时端——实际目标风险净敞口

t_netexposure=(t_H_stock_account+t_T_stock_account+t_T_future_value+t_H_future_value)/t_product_assets  # 产品 整体敞口

t_stock_account=t_H_stock_account+t_T_stock_account
t_stock_value=t_stock_account
t_future_account=t_T_future_account+t_H_future_account
t_future_value=t_T_future_value+t_H_future_value

t_risk_degree=(t_T_marginvalue+t_H_marginvalue)/t_future_account
t_IC_n=t_T_IC_n+t_H_IC_n
t_IF_n=t_T_IF_n+t_H_IF_n

'''
'产品名称','目标产品资产','目标股票账户资产比例','目标期货账户资产比例','目标股票账户资产','目标股票市值',
'目标期货账户资产','目标期货市值','保证金','IC合约手数','IF合约手数','风险度','风险敞口
'''
d0=['产品总计',t_product_assets,t_stock_account/t_product_assets,t_future_account/t_product_assets,
 t_stock_account, t_stock_value,t_future_account,t_future_value,t_T_marginvalue+t_H_marginvalue,t_IC_n,t_IF_n,t_risk_degree,t_netexposure]

d1=['对冲端——总',t_H_product_assets,t_H_stock_account/t_H_product_assets,t_H_future_account/t_H_product_assets,
 t_H_stock_account,t_H_stock_account,t_H_future_account,t_H_future_value,t_H_marginvalue,t_H_IC_n,t_H_IF_n,t_H_marginvalue/t_H_future_account,t_H_netexposure]


d2=['对冲端——IF',np.nan,np.nan,np.nan,
 t_H_stock_account_IF,t_H_stock_account_IF,np.nan,t_H_IF_n*IF_p,np.abs(t_H_IF_n*IF_p*IF_margin),0,t_H_IF_n,np.nan,np.nan]

d3=['对冲端——IC',np.nan,np.nan,np.nan,
 t_H_stock_account_IC,t_H_stock_account_IC,np.nan,t_H_IC_n*IC_p,np.abs(t_H_IC_n*IC_p*IC_margin),t_H_IC_n,0,np.nan,np.nan]



d4=['择时端——总',t_T_product_assets,t_T_stock_account/t_T_product_assets,t_T_future_account/t_T_product_assets,
 t_T_stock_account,t_T_stock_account,t_T_future_account,t_T_future_value,t_T_marginvalue,t_T_IC_n,t_T_IF_n,t_T_marginvalue/t_T_future_account,t_T_netexposure]



 
tinfo=pd.DataFrame([d0,d1,d2,d3,d4],columns=['产品名称','目标产品资产','目标股票账户资产比例','目标期货账户资产比例','目标股票账户资产',
                   '目标股票市值','目标期货账户资产','目标期货市值','保证金','IC合约手数','IF合约手数','风险度','风险敞口'])






