import numpy as np
import pandas as pd
import ruptures as rpt
import statsmodels.api as sm


###############################################################
def compute_beveridge_elasticity(u, v, quarterly=True, use_bp_defaults=True, bkps_in=None):
    '''
    This function computes beveridge elasticity using the unemployment rate u 
    and vacancy rate v. Elasticity is the estimated regression coefficient in 
    each of the detected structural segments.
    
    Parameters
    -----------
    u: scalar or pd.Series
        Current unemployment rate.
    v: scalar or pd.Series
        Vacancy rate.
    quarterly: bool, optional
    use_bp_defaults: bool, optional
        Whether to use Bai-Perron method for estimating structural break timepoints,
        using the same parameter settings as in Michaillat & Saez (2021).
        This will result in the exact same breakpoints as the MATLAB implementation.
        Default is True. (Currently no other approach is implemented, so True is forced.)
    bkps_in: list of int, optional
        The other option is to run a breakpoint estimation outside of this function and 
        feed this in. If bkps_in is specified, this will suppress the estimation with 
        the Bai-Perron method.
    
    
    Returns
    --------
    pd.DataFrame
        bev_e: beveridge elasticity and 95% CI estimates as time series.
    '''
    
    if quarterly:
        log_u = np.log(u.resample('Q').mean()/100.)
    
        log_v = np.log(v.resample('Q').mean()/100.)
        
        last_index = min(log_u.last_valid_index(), log_v.last_valid_index())
        log_u = log_u.loc[:last_index]
        log_v = log_v.loc[:last_index]
        
        
    else:
        log_u = np.log(u/100.)
        log_v = np.log(v/100.)
        
    if bkps_in is None:
    
        use_bp_defaults = True ## because we have not implemented any alternatives
        if use_bp_defaults:
            est_bkps = get_bp_breakpoints(log_u, log_v, use_bp_defaults=True)
            
    else:
    
        est_bkps = bkps_in
        
    # Now, ruptures package does not actually return the coeffs from the 
    # linear piecewise fit, so we have to get them again ourselves
    # note we just keep the coeff for the log_u, since that's what we 
    # need for the Bev elasticity
    
    ## set up the data
    y = np.array(log_v)
    X = np.vstack((np.array(log_u), np.ones(len(y)))).T
    
    # rule-of-thumb for setting the lag parameter in the Newey-West HAC estimator
    # statsmodels uses Newey-West HAC, which is slightly different than the 
    # Andrews HAC used by Bai & Perron.
    # see Cheung & Lai (1997) for nice discussion on N-W vs Andrews HAC
    haclags = int( (0.15*len(log_v))**(.25))
    
    coeffs = []  
      
    for idx, b in enumerate(est_bkps[:-1]):
 
        model = sm.OLS(y[est_bkps[idx]:est_bkps[idx+1]], X[est_bkps[idx]:est_bkps[idx+1],:]) 
        results = model.fit(cov_type='HAC', cov_kwds={'maxlags':haclags, 'use_correction': True}, use_t=True)
        coeffs.append((- results.params[0], results.bse[0]))

        
    bev_e = pd.DataFrame(columns=['E','SE', 'LB', 'UB'], index=log_v.index)
    
    for idx, a in enumerate(coeffs):
        bev_e.iloc[est_bkps[idx]:est_bkps[idx+1],0] = a[0]
        bev_e.iloc[est_bkps[idx]:est_bkps[idx+1],1] = a[1]
        bev_e.iloc[est_bkps[idx]:est_bkps[idx+1],2] = a[0] - 1.96*a[1]
        bev_e.iloc[est_bkps[idx]:est_bkps[idx+1],3] = a[0] + 1.96*a[1]
        
    bev_e = bev_e.astype('f')

    return bev_e
    
    
###############################################################
def get_bp_breakpoints(log_u, log_v, use_bp_defaults=True, min_size=4, n_bkps=-1, max_bkps=20):
    '''
    This function calls the dynamic programming method with linear 
    cost functions from the python ruptures package to calculate 
    the breakpoints according to the Bai-Perron method.
    
    Parameters
    -----------
    log_u: scalar or pd.Series
        Log of unemployment rate.
    log_v: scalar or pd.Series
        Log of vacancy rate.
    use_bp_defaults: bool, optional
        Whether to use Bai-Perron method for estimating structural break timepoints,
        using the same parameter settings as in Michaillat & Saez (2021). Default is True.
    min_size: int, optional
        A valid min_size parameter to be used with ruptures rpt.Dynp algorithm.
        Needs to be specified if use_bp_defaults=False.
    n_bkps: int, optional
        Needs to be specified if use_bp_defaults=False.
        Use n_bkps = -1 to run a procedure to test for the number of breakpoints.
        
        
    Returns
    --------
    list:
        The estimated breakpoints (as int indices), list starts with 0 and ends with len(series).
        
    Notes
    -----
        If we feed in the same dates (1951Q1 to 2019Q4) for the unemployment and
        vacancy data, then using "use_bp_defaults=True," this routine will output 
        the exact same breakpoints as the MATLAB implementation. 
        Namely: [0, 41, 84, 153, 194, 235, 276].

    '''
    
    # check there are no NaNs at the end of the data:
    last_index = min(log_u.last_valid_index(), log_v.last_valid_index())
    log_u = log_u.loc[:last_index]
    log_v = log_v.loc[:last_index]
    
    ## set up the data
    y = np.array(log_v)
    X = np.vstack((np.array(log_u), np.ones(len(y)))).T    
    signal = np.column_stack((y.reshape(-1, 1), X))
    
    
    if use_bp_defaults:
        # these settings correspond to the algorithm in Bai & Perron (2003)
        # see: https://centre-borelli.github.io/ruptures-docs/user-guide/costs/costlinear/
        # with setting as used in Michaillat & Saez (2021)
        # this will give us the same output as the MATLAB
        min_size = int(0.15*len(log_v)) 
        n_bkps = 5

        # call the dynamic programming algo
        est_bkps = _call_dynp(signal, min_size,n_bkps)

        
    else:
        if n_bkps > 0 and min_size * (n_bkps+1) > len(log_u)-1:
            raise ValueError("Parameters invalid. Either min_size or n_bkps (or both) too big for length of series!")
        elif n_bkps < 1:
            # run procedure to estimate number of breakpoints
            n_bkps = estimate_num_breaks(max_bkps=max_bkps, min_size=min_size)

        # call the dynamic programming algo
        est_bkps = _call_dynp(signal, min_size, n_bkps)       

        
    return est_bkps
    

###############################################################
def _call_dynp(signal, min_size, n_bkps):

    # helper function to call the actual meat of the dynamic programming fit
    fit = rpt.Dynp(model='linear', min_size=min_size, jump=1).fit(signal)
    est_bkps = fit.predict(n_bkps=n_bkps)
    est_bkps.insert(0,0)  
    
    return est_bkps
    
    
###############################################################
def evaluate_num_breaks(signal, max_bkps, min_size=4):

    
    t = signal.shape[0]
    q = signal.shape[1]-1
    
    # null model: zero breaks
    haclags = int( (0.15*t)**(.25))
    
    model = sm.OLS(signal[:,0], signal[:,1:]) 
    results = model.fit(cov_type='HAC', cov_kwds={'maxlags':haclags, 'use_correction': True}, use_t=True)
    
    # start lists with first element the result for zero breaks model
    ssr = [results.ssr]
    bic = [ _bic(0, ssr[0], q, t, use_lwz=False) ]
    lwz = [ _bic(0, ssr[0], q, t, use_lwz=True) ]
    
    # set up the breakpoint detection
    fit = rpt.Dynp(model='linear', min_size=min_size, jump=1).fit(signal)
    _ = fit.predict(max_bkps)
    
    bps_list=[[0,signal.shape[0]] ]
    # iterate over possible number of breakpoints
    for m in range(1,max_bkps+1):
    
        bkps = fit.predict(n_bkps=m)
        bkps.insert(0,0)
        bps_list.append(bkps)
        
        ssr_tmp = 0        
        for idx, b in enumerate(bkps[:-1]):
            # iterate over the segments of the model with m breaks, add up the ssr piece-wise
            model = sm.OLS(signal[bkps[idx]:bkps[idx+1],0], signal[bkps[idx]:bkps[idx+1],1:]) 
            results = model.fit(cov_type='HAC', cov_kwds={'maxlags':haclags, 'use_correction': True}, use_t=True)
            
            # add the ssr for the segment
            ssr_tmp += results.ssr
            
        # append results to lists    
        ssr.append(ssr_tmp)
        bic.append( _bic(m, ssr_tmp, q, t) ) 
        lwz.append( _bic(m, ssr_tmp, q, t, use_lwz=True) )
             
        n_bkps = np.argmin(bic)
    
    return bic, lwz, ssr, bps_list
    

#################
def _bic(m, ssr, q, t, use_lwz=False):
    # helper function to return the BIC 
    # or Liu, Wu and Zidek (1994) modified criterion

    if use_lwz:
    
        return( np.log(ssr/(t-(q*(m+1)+m))) + 0.299*((q*(m+1)+m)/t)*np.log(t)**2.1  )
    else:
        return( np.log(ssr/t) + (q*(m+1)+m)*np.log(t)/t)
    
    

    
