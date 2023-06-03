import os
import pandas as pd
import matplotlib.pyplot as plt
from DataLoader import DataLoader
from PathConfig import PathConfig

class AlphaEval():
    def __init__(self,alphas):
        self.d = DataLoader()
        self.path = PathConfig()
        self.alphas = alphas
        self.pnl = {}
        self.alpha_dfs = {}

    def merge_df(self,name):
        merged_path = self.path.get_merged_alpha_path(name)
        path = self.path.get_alpha_path(name)
        if not os.path.exists(path):
            print('Alpha path not detected!')
        dfs = []
        for filename in os.listdir(path):
            date = filename.split(".")[0]
            if date.isdigit():
                df = self.d.loading('alpha',name=name,date=date)
                dfs.append(df)
        pd.concat(dfs).to_csv(merged_path)
        
    def compute_corr(self):
        df = pd.DataFrame()
        cols = []
        for a in self.alphas:
            col_a = 'alpha_'+a
            merged_path = self.path.get_merged_alpha_path(a)
            if not os.path.exists(merged_path):
                self.merge_df(a)
            if df.empty:
                df = pd.read_csv(merged_path)[['code','date','alpha']]
                df.rename(columns={'alpha': col_a}, inplace=True)
            else:
                df1 = pd.read_csv(merged_path)[['code','date','alpha']]
                df1.rename(columns={'alpha': col_a}, inplace=True)
                df = df.merge(df1,on=['code','date'])
            cols.append(col_a)
        self.corr_mat = df[cols].corr()

        
    def compute_pnl(self,groups=['hs300','zz500','zz800']):
        d = self.d
        for a in self.alphas:
            self.pnl[a] = {group:[] for group in groups}
            self.pnl[a]['all'] = []
            path = self.path.get_alpha_path(a)
            if not os.path.exists(path):
                print('Alpha path not detected!')
                continue
            for date in d.trade_dates:
                df1 = d.loading('alpha',name=a,date=date)
                df2 = d.loading('adj_return',date=date)
                if df1.empty or df2.empty:
                    continue
                for group in groups:
                    df3 = d.load_univ(group,date)
                    df1[group] = df1['code'].isin(df3['code'])
                df = df1.merge(df2,how='inner',on='code')[['code','weight','adj_return']+groups]
                df['weighted_return'] = df['adj_return']*df['weight']
                self.pnl[a]['all'].append([date,df['weighted_return'].sum()])
                for group in groups:
                    df['weighted_return_'+group] = df['adj_return']*df['weight']*df[group]
                    self.pnl[a][group].append([date,df['weighted_return_'+group].sum()])
            for k in self.pnl[a]:
                df = pd.DataFrame(self.pnl[a][k], columns=['date', 'return'])
                df['cum_return'] = df['return'].cumsum()
                self.pnl[a][k] = df
            
    def plot_pnl(self,alpha='all',univ='all'):
        l = []
        for a in self.pnl if alpha == 'all' else alpha:
            for u in self.pnl[a] if alpha == 'all' else univ:
                self.pnl[a][u]['cum_return'].plot(legend=True)
                l.append(a+'_'+u)
        plt.title("Cum PnL")
        plt.legend(l)