import os
import pandas as pd
import matplotlib.pyplot as plt
from DataLoader import DataLoader

class PathConfig():
    def __init__(self,**kwargs):
        self.alphapath=kwargs.get('alphapath','/Users/siwu/Downloads/QRData/Alpha/')
        self.datapath = kwargs.get('datapath','/Users/siwu/Downloads/QRData/Data/')

    def get_alpha_path(self,alpha_name):
        return self.alphapath+alpha_name+'/'

class AlphaEval():
    def __init__(self,alphas):
        self.d = DataLoader()
        self.path = PathConfig()
        self.alphas = alphas
        self.return_df = {}
        
    def compute_pnl(self):
        d = self.d
        for a in self.alphas:
            path = self.path.get_alpha_path(a)
            if not os.path.exists(path):
                print('Alpha path not detected!')
                continue
            res = []
            for date1,date2 in zip(d.trade_dates[:-1],d.trade_dates[1:]):
                df1 = d.loading('alpha',name=a,date=date1)
                df2 = d.loading('adj_return',date=date2)
                df = df1.merge(df2,how='inner',on='code',suffixes=('_yesterday', '_today'))
                df['weighted_return'] = df['adj_return']*df['weight']
                res.append([date2,df['weighted_return'].sum()])
            df = pd.DataFrame(res, columns=['date', 'return'])
            df['cum_return'] = df['return'].cumprod()
            self.return_df[a] = df
            
    def plot_pnl(self):
        for a,df in self.return_df.items():
            df['cum_return'].plot(legend=True)
        plt.title("Cum PnL")
        plt.legend(self.return_df.keys())