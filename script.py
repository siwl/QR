import sys
from alpha.nDayRetStd import nDayRetStd
from alpha.nDayTurnoverStd import nDayTurnoverStd
from alpha.nDayTurnoverMean import nDayTurnoverMean

configs = {
    'turnover_5day_std':{'alpha':'nDayTurnoverStd',
                          'params':{
                              'days':5,
                              'short':True}
                         },
    'turnover_20day_std':{'alpha':'nDayTurnoverStd',
                          'params':{
                              'days':20,
                              'short':True}
                         },
    'turnover_60day_std':{'alpha':'nDayTurnoverStd',
                          'params':{
                              'days':60,
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