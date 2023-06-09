class PathConfig():
    def __init__(self,**kwargs):
        self.alphapath=kwargs.get('alphapath','/Users/siwu/Downloads/QRData/Alpha/')
        self.datapath = kwargs.get('datapath','/Users/siwu/Downloads/QRData/Data/')

    def get_alpha_path(self,alpha_name):
        return self.alphapath+alpha_name+'/'

    def get_merged_alpha_path(self,alpha_name):
        return self.alphapath+alpha_name+'/'+'merged.csv'
    
    def get_univ_path(self,univ_name):
        return self.datapath+'univ/'+univ_name+'/'
    
    def get_data_path(self,data_name):
        return self.datapath+data_name+'/'