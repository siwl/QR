import pandas as pd
import os
from PathConfig import PathConfig

class DataLoader(object):
    def __init__(self,root_path='/Users/siwu/Downloads/QRData/Data/'):
        # Root Path/
        #   adj_fct/
        #       20180102{date}/  ...
        #   idx/
        #       20180102{date}/  ...
        #   sw/
        #       20180102{date}/  ...
        #   lmt/
        #       20180102{date}/  ...
        #   univ/
        #       zz9999/  
        #           20180102{date}/  ...
        #   mkt_val/
        #       20180102{date}/  ...
        #   date/
        #       halt_date.csv
        #       lst_date.csv
        #       st_date.csv
        #       trd_date.csv
        #   qishi_1min_zip/
        #       20180102{date}/
        #           0000001{stock code}.csv ...
        self.path = PathConfig()
        self.stk_1min_path = root_path+'qishi_1min_zip/'
        self.adj_fct_path = root_path+'adj_fct/'
        self.adj_return_path = root_path+'adj_return/'
        self.halt_date_path = root_path+'date/halt_date.csv'
        self.lst_date_path = root_path+'date/lst_date.csv'
        self.st_date_path = root_path+'date/st_date.csv'
        self.trd_date_path = root_path+'date/trd_date.csv'
        self.idx_path = root_path+'idx/'
        self.lmt_path = root_path+'lmt/'
        self.mkt_val_path = root_path+'mkt_val/'
        self.sw_path = root_path+'sw/'
        self.univ_path = root_path+'univ/'
        trade_date_df= pd.read_csv(self.trd_date_path)
        trade_date_df = trade_date_df[(trade_date_df['is_open'] == 1)&
                                      (trade_date_df['date']>=20180000)&
                                      (trade_date_df['date']<20210000)]
        self.trade_dates = sorted(trade_date_df['date'].values.tolist())
        self.univ = ['hs300','zz500','zz800','zz1000','zz9999']
        
        
    @staticmethod
    def find_date_csv_path(path,date):
        res = path+date+'.csv'
        if not os.path.exists(res):
            return None
        return res
    
    @staticmethod
    def find_code_stk_path(path,code):
        res = path+code+'.csv'
        if not os.path.exists(res):
            raise Exception("CSV file does not exist for the corresponding stock code!")
        return res
    
    @staticmethod
    def find_date_folder_path(path,date):
        res = path+date+'/'
        if not os.path.exists(res):
            raise Exception("Folder does not exist for the corresponding date!")
        return res
    
    def load_multiple_date_csv(self,path,date,window,fields='All'):
        start = self.trade_dates.index(int(date))
        res = pd.DataFrame()
        for offset in range(min(window,len(self.trade_dates)-start)):
            i = start+offset
            d = self.trade_dates[i]
            date_offset_path = self.find_date_csv_path(path,str(d))
            if not date_offset_path:
                continue
            if fields != 'All':
                df = pd.read_csv(date_offset_path,usecols = fields)
            else:
                df = pd.read_csv(date_offset_path)
            if 'date' not in df.columns:
                df['date'] = d
            res = df if res.empty else pd.concat([res, df],ignore_index=True)
        return res


    def loading(self,tabname,date,fields='All',window=1,code=None,name=None):
        if tabname == 'stk_1min':
            df = self.load_multiple_date_csv(self.stk_1min_path,date,window,fields=fields)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'adj_fct':
            path = self.path.get_data_path(tabname)
            df = self.load_multiple_date_csv(tabname,date,window)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'adj_return':
            path = self.path.get_data_path(tabname)
            df = self.load_multiple_date_csv(path,date,window)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'idx':
            df = self.load_multiple_date_csv(self.idx_path,date,window)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'lmt':
            df = self.load_multiple_date_csv(self.lmt_path,date,window)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'mkt_val':
            df = self.load_multiple_date_csv(self.mkt_val_path,date,window)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'sw':
            df = self.load_multiple_date_csv(self.sw_path,date,window)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'univ':
            res = pd.DataFrame()
            for u in self.univ:
                df = self.load_multiple_date_csv(self.univ_path+u+'/',date,window)
                df['univ'] = u
                res = df if res.empty else pd.concat([res, df],ignore_index=True)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'lst_date':
            lst_date_path = self.lst_date_path
            df = pd.read_csv(lst_date_path)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'st_date':
            st_date_path = self.st_date_path
            df = pd.read_csv(st_date_path)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'halt_date':
            halt_date_path = self.halt_date_path
            df = pd.read_csv(halt_date_path)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        elif tabname == 'alpha':
            if not name:
                print("Please name the alpha.")
                return
            path = self.path.get_alpha_path(name)
            df = self.load_multiple_date_csv(path,date,window)
            if code is not None:
                return df[df['code']==int(code)]
            return df
        else:
            raise Exception("Tab name is not supported! Supported tabnames are:\n stk_1min,\n adj_fct,\n idx,lmt,\n mkt_val,\n sw,\n univ,\n lst_date,\n st_date,\n halt_date")
d = DataLoader(root_path='/Users/siwu/Downloads/QRData/Data/') 