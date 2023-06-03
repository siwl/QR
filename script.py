import sys
from alpha.nDayRetStd import nDayRetStd
from alpha.nDayTurnoverStd import nDayTurnoverStd
from alpha.nDayTurnoverMean import nDayTurnoverMean
from alpha.nDayTurnoverStdvsMean import nDayTurnoverStdvsMean
from alpha.nDayTurnoverMeanvsStd import nDayTurnoverMeanvsStd
from alpha.nDayAcctTurnoverMean import nDayAcctTurnoverMean
from alpha.nDayVoloverNegshare import nDayVoloverNegshare

configs = {
    # 'accturnover_5day_mean':{'alpha':'nDayAcctTurnoverMean',
    #                       'params':{
    #                           'days':5,
    #                           'short':True}
    #                      },
    # 'accturnover_20day_mean':{'alpha':'nDayAcctTurnoverMean',
    #                       'params':{
    #                           'days':20,
    #                           'short':True}
    #                      },
    # 'accturnover_60day_mean':{'alpha':'nDayAcctTurnoverMean',
    #                       'params':{
    #                           'days':60,
    #                           'short':True}
    #                      },
    # 'turnover_5day_stdovermean':{'alpha':'nDayTurnoverStdvsMean',
    #                       'params':{
    #                           'days':5,
    #                           'short':True}
    #                      },
    # 'turnover_20day_stdovermean':{'alpha':'nDayTurnoverStdvsMean',
    #                       'params':{
    #                           'days':20,
    #                           'short':True}
    #                      },
    # 'turnover_60day_stdovermean':{'alpha':'nDayTurnoverStdvsMean',
    #                       'params':{
    #                           'days':60,
    #                           'short':True}
    #                      },
    # 'turnover_5day_meanoverstd':{'alpha':'nDayTurnoverMeanvsStd',
    #                       'params':{
    #                           'days':5,
    #                           'short':True}
    #                      },
    # 'turnover_20day_meanoverstd':{'alpha':'nDayTurnoverMeanvsStd',
    #                       'params':{
    #                           'days':20,
    #                           'short':True}
    #                      },
    # 'turnover_60day_meanoverstd':{'alpha':'nDayTurnoverMeanvsStd',
    #                       'params':{
    #                           'days':60,
    #                           'short':True}
    #                      },
    'volume_over_negshare':{'alpha':'nDayVoloverNegshare',
                          'params':{
                              'days':1,
                              'short':True}
                         },
    'volume_over_negshare_5day_mean':{'alpha':'nDayVoloverNegshare',
                          'params':{
                              'days':5,
                              'short':True}
                         },
    'volume_over_negshare_20day_mean':{'alpha':'nDayVoloverNegshare',
                          'params':{
                              'days':20,
                              'short':True}
                         },
}

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


for name,inputs in configs.items():
    alpha = inputs['alpha']
    params = inputs['params']
    params['name'] = name
    a = str_to_class(alpha)
    a = a(**params)
    a.output_csv()