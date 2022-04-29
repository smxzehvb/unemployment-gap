import numpy as np
import pandas as pd
from scipy.optimize import root

## functions:

### rates: compute_job_finding_rate, compute_job_separation_rate

###############################################################
def compute_job_finding_rate(u_level, ushort_level, quarterly=True, adjust_short=True):    
    '''
    The function measures the job-finding rate from the unemployment level and short-term 
    unemployment level. The measurement method was proposed by Shimer (2012) and is 
    described in online appendix B (eqn A7 & A8).
    
    Parameters
    -----------
    u_level: pd.Series
        Monthly unemployment level
    ushort_level: pd.Series
        Monthly short-term unemployment level
    quarterly: bool, optional
        Whether to convert monthly rates to quarterlty. Default is True.
    adjust_short: bool, optional
        Whether the short-term level needs to be adjusted as in Shimer (2012). Default True.
        
    Returns
    --------
    pd.Series
        Job-finding rate
    '''
    
    if adjust_short:
        # Adjust short-term unemployment level after January 1994 as in Shimer (2012, appendix A)
        ushort_level[ushort_level.index > '1994-1'] = 1.1*ushort_level[ushort_level.index > '1994-1']
        
    # Compute the monthly job-finding probability from equation (A7)
    f = 1.0 - (u_level.shift(-1) - ushort_level.shift(-1) )/u_level
    
    # Compute the monthly job-finding rate from equation (A8)
    rate = -np.log(1.0 - f)
    rate.name = 'job_find_rate'
    
    if quarterly:
        # monthly to quarterly
        rate = rate.resample('Q').sum()

    return rate
    


###############################################################
def job_sep_expr_(lambda_rate, *consts):

    find_rate, u_level, u_level_next, h_level = consts
    
    exp_factor = np.exp(-(find_rate+lambda_rate))
    
    expr = (1. - exp_factor) * lambda_rate/(find_rate + lambda_rate) * h_level + exp_factor * u_level - u_level_next  
    
    return expr 
    

###############################################################
def compute_job_separation_rate(u_level, ushort_level, h_level, quarterly=True, adjust_short=True):    
    '''
    The function measures the job-separation rate lambda, from the unemployment level 
    and labor-force size. The measurement method was proposed by Shimer (2012) and is 
    described in online appendix B.
    
    Parameters
    -----------
    u_level: pd.Series
        Monthly unemployment level
    ushort_level: pd.Series
        Monthly short-term unemployment level
    h_level: pd.Series
        Monthly labor force size
    quarterly: bool, optional
        Whether to convert monthly rates to quarterlty. Default is True.
    adjust_short: bool, optional
        Whether the short-term level needs to be adjusted as in Shimer (2012). Default True.
        
    Returns
    --------
    pd.Series
        Job-separation rate lambda
    '''
    
    find_rate = compute_job_finding_rate(u_level, ushort_level, quarterly=quarterly, adjust_short=adjust_short)
    
    # Compute equation (A9) solve for the monthly job-separation rate every month
    # use scipy.optimize.root to solve (setting root guess as 0.0)
    # calculate each month with a list comprehension
    rate = [root(job_sep_eqn, 0.0, (find_rate.loc[t], unempl_level.loc[t], unempl_level.shift(-1).loc[t], labor_level.loc[t])).x[0] for t in unempl_level.index]   
    
    rate = pd.series(data=rate, index=unempl_level.index, name='job_sep_lambda')
        
    if quarterly:
        # monthly to quarterly
        rate = rate.resample('Q').sum()
        
    return rate
    
    
