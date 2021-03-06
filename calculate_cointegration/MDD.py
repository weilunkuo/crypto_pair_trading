# -*- coding: utf-8 -*-
"""
Created on Mon May 25 18:56:37 2020

@author: allen
"""
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator, FuncFormatter
import numpy as np
import time
import sys
import os
import pandas as pd
import math
import matplotlib.pyplot as plt
import datetime
import glob
import matplotlib.ticker as ticker

ext_of_profit = "_profit.csv"
path_to_profit = f"/home/allen/CryptoCurrency_TP/"

def color_change(n):
    if n : return "g"
    else : return "r" 
def plot_performance_with_dd( ans,total_with_capital, dates, open_number,normal_close_number, win_rate,capital_list,formation_time, jump,correlation_list,_day_return):
    profit_file = f"/home/allen/CryptoCurrency_TP/profit_return_picture_formation_{formation_time}_MLtask/"
    if not os.path.exists(profit_file):
                os.makedirs(profit_file)
    picture_title =f'Pairs trading with CryptoCurrency_BTC_ETH_formation_{formation_time}_jump_{jump}_adjust_capital_addML_'
    picture_correlation =f'Pairs trading with CryptoCurrency_BTC_ETH_formation_{formation_time}_correlation_Return_addML_'
    picture_return_distribution = f'Pairs trading with CryptoCurrency_BTC_ETH_formation_{formation_time}_Return_distribution_addML_'
    max_cap = max(capital_list)
    #total_with_capital = np.cumsum(total_with_capital)
    dates = sorted(dates)
    total = np.cumsum(ans)
    dd = list()
    tt =  total[0]
    r = pd.DataFrame(total_with_capital)
    capital_list = pd.DataFrame(capital_list)
    #per_r = pd.DataFrame(per_reward)
    #r = (total_with_capital - total_with_capital.shift(1)) / total_with_capital.shift(1)
    r_neg = [i for i in total_with_capital if i < 0]
    r_neg = pd.DataFrame(r_neg)
    sharp_ratio = r.mean() / r.std() * np.sqrt(len(dates))
    sortino_ratio = r.mean() / r_neg.std() * np.sqrt(len(dates))
    #per_sharpe_ratio = per_r.mean() / per_r.std() 
    for i in range(len(ans)):
        if i > 0 and total[i] > total[i-1]:
            tt = total[i]
        dd.append(total[i]-tt)
    print(dd) 
    xs = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in dates]
    highest_x = []
    highest_dt = []
    for i in range(len(total)):
        if total[i] == max(total[:i+1]) and total[i] > 0:
            highest_x.append(total[i])
            highest_dt.append(i)
    mpl.style.use('seaborn')
    color_list = list(map(color_change,[r> 0 for r in total_with_capital]))
    f, axarr = plt.subplots(3, sharex=True, figsize=(20, 12), gridspec_kw={'height_ratios': [3, 1, 1]})
    axarr[0].plot(np.arange(len(xs)), total, color='b', zorder=1)
    axarr[0].scatter(highest_dt, highest_x, color='lime', marker='o', s=40, zorder=2)
    axarr[0].set_title(picture_title, fontsize=20)
    axarr[1].bar(np.arange(len(xs)), dd, color='red')
    axarr[2].bar(np.arange(len(xs)), total_with_capital,color= color_list)
    date_tickers = dates
    def format_date(x,pos=None):
        if x < 0 or x > len(date_tickers)-1:
            return ''
        return date_tickers[int(x)]
    axarr[0].xaxis.set_major_locator(MultipleLocator(80))
    axarr[0].xaxis.set_major_formatter(FuncFormatter(format_date))
    axarr[0].grid(True)
    shift = (max(total)-min(total))/20
    text_loc = max(total)-shift
    axarr[0].text(np.arange(len(xs))[5], text_loc, 'Total open number : %d' % open_number, fontsize=15)
    axarr[0].text(np.arange(len(xs))[5], text_loc-shift, 'Total profit : %.2f' % total[-1], fontsize=15)
    axarr[0].text(np.arange(len(xs))[5], text_loc-shift*2, 'Win rate : %.2f ' % (win_rate), fontsize=15)
    axarr[0].text(np.arange(len(xs))[5], text_loc-shift*5, 'sharpe ratio : %.4f' % (sharp_ratio), fontsize=15)
    axarr[0].text(np.arange(len(xs))[5], text_loc-shift*6, 'sortino ratio : %.4f' % (sortino_ratio), fontsize=15)
    axarr[0].text(np.arange(len(xs))[5], text_loc-shift*3, 'Normal close rate : %.2f' % (normal_close_number/open_number), fontsize=15)
    axarr[0].text(np.arange(len(xs))[5], text_loc-shift*4, 'Max drawdown : %d' % min(dd), fontsize=15)
    axarr[0].text(np.arange(len(xs))[5], text_loc-shift*7, 'Max trade capital need in daily : %.3f' % max_cap, fontsize=15)
    axarr[0].text(np.arange(len(xs))[5], text_loc-shift*8, 'Average trade capital : %.3f' % capital_list.mean(), fontsize=15)
    plt.tight_layout()
    plt.savefig(profit_file+picture_title)
    plt.show()
    plt.close()

    plt.figure()
    plt.scatter(correlation_list,_day_return)
    plt.xlabel("Correlation")
    plt.ylabel("Return")
    plt.title("Plot between Correlation and Return")
    plt.savefig(profit_file+picture_correlation)
    return_distribution = [i for i in total_with_capital if i != 0]
    #print(total_with_capital)
    plt.show()
    plt.close()
    quartiles = [25, 50 ,75]
    plt.figure()
    plt.hist(return_distribution,bins = 64)
    
    q = np.percentile(return_distribution,quartiles[0])
    plt.axvline(q,color = 'orange',label = "Q1")
    q = np.percentile(return_distribution,quartiles[1])
    plt.axvline(q,color = 'red', label = "Median")
    q = np.percentile(return_distribution,quartiles[2])
    plt.axvline(q,color = 'green', label = "Q3")
    plt.legend(loc ="upper right")
    
    plt.title("strategy Return distribution")
    plt.savefig(profit_file+picture_return_distribution)
    plt.show()
    plt.close()



    return sharp_ratio,sortino_ratio,min(dd)
def reward_calculation(path_to_profit):
    datelist = [f.split('_')[0] for f in os.listdir(path_to_profit)]
    reward=[]
    cumulative_reward=[]
    capital_list=[]
    return_reward=[]
    per_reward = []
    max_cap = 0
    for i,date in enumerate(sorted(datelist)):
        #print(i,date)
        profit = pd.read_csv(path_to_profit+date+ext_of_profit)
        #print(profit)
        reward.append(profit["reward"].sum())
        capital_list.append(profit["trade_capital"].sum())
        for j in range(len(profit)):
            per_reward.append(profit["reward"][j]/profit["trade_capital"][j])
        
    max_cap = max(capital_list)
        #return_reward.append(reward[i]/capital_list[i])
    for i,date in enumerate(sorted(datelist)):
        return_reward.append(reward[i]/max_cap)
    return reward,return_reward,per_reward,max_cap ,datelist
if __name__ =="__main__":
    total_open = 0
    normal_close = 0
    win_rate = 0
    datelist = [f.split('_')[0] for f in os.listdir(path_to_profit)]
    #datelist.pop()
    print(sorted(datelist))
    reward=[]
    cumulative_reward=[]
    capital_list=[]
    return_reward=[]
    per_reward = []
    max_cap = 0
    print(datelist)
    for name in glob.glob(path_to_profit +'*.csv'):
        #profit = pd.read_csv(path_to_profit+date+ext_of_profit)
        profit = pd.read_csv(name)
        #print(profit)
        reward.append(profit["reward"].sum())
        capital_list.append(profit["trade_capital"].sum())
        total_open += profit["open_num"].sum()
        for j in range(len(profit)):
            per_reward.append(profit["reward"][j]/profit["trade_capital"][j])
            
    #print(capital_list)
    max_cap = max(capital_list)
    print("max_capital :",max_cap)
    total_cap = sum(capital_list)
        #return_reward.append(reward[i]/capital_list[i])
    print(len(reward))
    print(len(datelist))
    print(reward)
    for i,date in enumerate(sorted(datelist)):
        return_reward.append(reward[i]/max_cap)

    #plot_performance_with_dd(path_to_profit,reward,return_reward,per_reward,datelist,total_open,normal_close,win_rate,max_cap)
    
