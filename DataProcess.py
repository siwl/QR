#!/usr/bin/env python3

import os
import pandas as pd
import shutil
path = '/Users/siwu/Downloads/QRData/Data/qishi_1min_zip/'

def process_daily_stk_data(path):
    for date in sorted(os.listdir(path))[:40]:
        sub_path = path+date
        if os.path.isdir(sub_path):
            res = []
            for filename in sorted(os.listdir(sub_path)):
                code = filename.split('.')[0]
                f = os.path.join(sub_path, filename)
                if os.path.isfile(f):
                    df = pd.read_csv(f)
                    df['code'] = code
                    res.append(df)
            frame = pd.concat(res, axis=0, ignore_index=True)
            output_path = sub_path+'.csv'
            frame.to_csv(output_path,index=False)
            shutil.rmtree(sub_path)

stk_path = '/Users/siwu/Downloads/QRData/Data/qishi_1min_zip/'       
adj_fct_path = "/Users/siwu/Downloads/QRData/Data/adj_fct/"
output_path = "/Users/siwu/Downloads/QRData/Data/adj_return/"
def process_adj_price(stk_path,adj_fct_path,output_path):
    df_yesterday = pd.DataFrame()
    for filename in sorted(os.listdir(stk_path)):
        f1 = os.path.join(stk_path, filename)
        output_f = os.path.join(output_path, filename)
        date = filename.split('.')[0]
        df1 = pd.read_csv(f1,usecols = ['code','close']).groupby('code').last()
        f2 = os.path.join(adj_fct_path, filename)
        df2 = pd.read_csv(f2,usecols = ['code','cum_adjf'])
        df_today = df1.merge(df2, how='inner', on='code')
        df_today['adj_close'] = df_today['cum_adjf']*df_today['close']
        if not df_yesterday.empty:
            df = df_today.merge(df_yesterday, how='inner', on='code',suffixes=('_today', '_yesterday'))
            df['adj_return'] = df['adj_close_today']/df['adj_close_yesterday']-1.0
            df = df[['code','adj_return']]
            df.to_csv(output_f,index=False)
            print("============= Processed adj return on date: {}.  =============".format(date))
        df_yesterday = df_today
