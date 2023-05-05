from pathlib import Path 
from DataLoader import DataLoader
from PathConfig import PathConfig

class constVolIntraDay():
    def __init__(self,**kwargs):
        self.p = kwargs.get('const_threshold',1)
        self.short = kwargs.get('short',False)
        self.pathconfig = PathConfig()
        self.d = DataLoader()
        
    def compute(self,date):
        p = self.p
        short = self.short
        df = self.d.loading('stk_1min',date,fields=['open','close','high','low','code','volume'])
        df['const'] = ((df['close']-df['open']).abs()<=(p*(df['high']-df['low'])))
        df['const_vol'] = df['const']*df['volume']
        df = df[['code','volume','const_vol']].groupby(by=['code']).sum()
        df['alpha'] = df['const_vol']/df['volume']
        self.compute_weight(df,short=short)
        return df[['alpha','weight']]
    
    def compute_weight(self,df,short=False):
        df['weight'] = df['alpha'].sub(df['alpha'].mean())
        if not short:
            df['weight'] = df['weight'].mask(df['weight'].lt(0),0)
        df['weight'] = df['weight'].div(df['weight'].sum())
    
    def output_csv(self):
        pc = self.pathconfig
        for date in self.d.trade_dates:
            path = Path(pc.alphapath+self.__class__.__name__+'/'+str(date)+'.csv')
            path.parent.mkdir(parents=True, exist_ok=True) 
            df = self.compute(date)
            df.to_csv(path)