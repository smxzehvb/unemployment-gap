import numpy as np
import pandas as pd

####################################################
def check_rates_formatting(r, to_quarterly=True):
    '''
    Check if rates are in [0., 1.] format, not [0., 100.].
    Also optionally convery montly series to quarterly.
    
    Parameters
    -----------
    r: pd.Series
        Monthly rate.
    to_quarterly: bool, optional
        Convert monthly data to quarterly; default is True.
        
    Returns
    --------
    pd.Series
        Rate.
    '''    
    
    # bit crude, we'll just check for any values >1, and then assume 
    # the format was [0,100] and not [0,1]
    if (r > 1.0).any():
        r = r/100.

    if to_quarterly:
        r = r.resample('Q')[columns].mean()
        
    return r
    
####################################################
