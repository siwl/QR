from pathlib import Path
import pandas as pd
from collections import deque
from DataLoader import DataLoader
from PathConfig import PathConfig

class nDayRetStd():
    def __init__(self,**kwargs):
        self.ndays = kwargs.get('ndays',5)
        self.short = kwargs.get('short',True)
        self.pathconfig = PathConfig()
        self.d = DataLoader()
    
    def compute_weight(self,df,short=True):
        df['weight'] = df['alpha'].sub(df['alpha'].mean())
        pos_sum = df['weight'][df['weight']>0].sum()
        df['long_weight'] = df['weight'][df['weight']>0].div(pos_sum)
        df['long_weight'] = df['long_weight'].fillna(0)
        if short:
            neg_sum = df['weight'][df['weight']<0].sum()
            df['short_weight'] = df['weight'][df['weight']<0].div(-neg_sum)
            df['short_weight'] = df['short_weight'].fillna(0)
            df['weight'] = df['long_weight']+df['short_weight']
        else:
            df['weight'] = df['long_weight']
        df = df[['alpha','weight']]
        return df
        
    
    def output_csv(self):
        pc = self.pathconfig
        trade_dates = self.d.trade_dates
        n = self.ndays
        dfs = deque([self.d.loading('adj_return',date) for date in trade_dates[1:n+1]])
        df = pd.concat(dfs)
        for date in trade_dates[n+1:]:
            df = pd.concat(dfs)
            df = -df.groupby(['code'])['adj_return'].std()
            df = df.to_frame(name='alpha')
            df = self.compute_weight(df,short=self.short)
            dfs.popleft()
            dfs.append(self.d.loading('adj_return',date))
            path = Path(pc.alphapath+self.__class__.__name__+'/'+str(date)+'.csv')
            path.parent.mkdir(parents=True, exist_ok=True) 
            df.to_csv(path)