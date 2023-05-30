from pathlib import Path 
from DataLoader import DataLoader
from PathConfig import PathConfig
from collections import deque
import pandas as pd

class nDayTurnoverMean():
    def __init__(self,**kwargs):
        self.days = kwargs.get('days',5)
        self.short =  kwargs.get('short',True)
        self.name = kwargs.get('name',self.__class__.__name__)
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
        n = self.days
        trade_dates = self.d.trade_dates
        dfs = deque([self.d.loading('stk_1min',date,fields=['turover','code']).groupby('code').last()
                     for date in trade_dates[1:n+1]])
        for date in trade_dates[n+1:]:
            df = pd.concat(dfs)
            a = -df.groupby(['code'])['turover'].mean()
            df = a.to_frame(name='alpha')
            df = self.compute_weight(df,short=self.short)
            dfs.popleft()
            dfs.append(self.d.loading('stk_1min',date,fields=['turover','code']).groupby('code').last())
            path = Path(pc.alphapath+self.name+'/'+str(date)+'.csv')
            path.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(path)