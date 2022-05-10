import numpy as np
import pandas as pd

## functions:

### unemployment: compute_beveridgean_unemployment
### elasticity: compute_matching_elasticity
### efficacy: compute_separation_efficacy, compute_matching_efficacy
### efficiency: compute_efficiency_endogenous, compute_efficiency_hosios


###############################################################
def compute_beveridgean_unemployment(f, lamb):
    '''
    This function computes the Beveridgean unemployment rate in a 
    Diamond–Mortensen–Pissarides (DMP) model from the job-finding 
    rate f and the job-separation rate lambda. The derivation of 
    the Beveridgean unemployment rate is in section 4.1 (eqn 9). 

    Parameters
    -----------
    f: pd.Series
        Job-finding rate.
    lamb: pd.Series
        Job-separation rate.
    
    Returns
    --------
    pd.Series
        Beveridgean unemployment rate.
    '''
    
    return lamb / (lamb + f)

###############################################################
def compute_matching_elasticity(u, epsilon):
    '''
    This function computes the matching elasticity eta in a DMP model from
    Beveridge elasticity epsilon and the unemployment rate u. The matching 
    elasticity is derived in online appendix C (eqn A12).
    
    Parameters
    -----------
    u: pd.Series
        unemployment rate.
    epsilon: pd.Series
        Beveridge elasticity.
        
    Returns
    --------
    pd.Series
        eta: Matching elasticity.
    '''

    return (1./(1.+ epsilon)) * (epsilon - u/(1. - u) ) 
    

###############################################################
def compute_separation_efficacy(u, eta, theta):
    '''
    This function computes the separation-efficacy ratio lambda/omega in a DMP model 
    from the matching elasticity eta, labor-market tightness theta, and unemployment 
    rate u. The separation-efficacy ratio is derived in online appendix C.
    
    Parameters
    -----------
    u: pd.Series
        Unemployment rate.
    eta: pd.Series
        Matching elasticity.
    theta: pd.Series
        Labor-market tightness.
    
    Returns
    --------
    pd.Series
        lambda/omega: Separation-efficacy ratio.
    '''

    return np.power(theta, (1. - eta)) * u/(1. - u)    
    
###############################################################
def compute_matching_efficacy(f, theta, eta):    
    '''
    This function computes the matching efficacy in a DMP model from the 
    job-finding rate f, the labor-market tightness theta, and the matching 
    elasticity eta. The matching efficacy is derived in online appendix D 
    (eqn A15).
    
    Parameters
    -----------
    f: pd.Series
        Job-finding rate.
    theta: pd.Series
        Labor-market tightness.
    eta: pd.Series
        Matching elasticity.
    
    Returns
    --------
    pd.Series
        omega: Matching efficacy.
    '''
    
    return f / np.power(theta,(1. - eta))

###############################################################
def compute_efficiency_endogenous(eta, z, c, lo):
    '''
    This function computes the efficient unemployment rate u_star and efficient labor-market 
    tightness theta_star in a DMP model using the sufficient-statistic formula in proposition 
    2 and accounting for the endogeneity of the Beveridge elasticity. This efficient unemployment 
    rate and efficient tightness are derived in online appendix C (eqn A10 & A11). 
    
    Parameters
    -----------
    eta: pd.Series
        Matching elasticity.
    z: pd.Series
        Relative productivity of unemployed workers.
    c: pd.Series
        Recruiting cost.
    lo: pd.Series
        Separation-efficiency ratio.
    
    Returns
    --------
    pd.Series
        u_star: Efficient unemployment rate.
    pd.Series
        theta_star: Efficient labor-market tightness.
    '''


    return u_star, theta_star
    
###############################################################
def compute_efficiency_hosios(eta, z, c, lamb, omega, r, u0):
    '''
    This function computes the efficient unemployment rate u_star and efficient labor-market 
    tightness theta_star in a DMP model using the Hosios condition. This efficient unemployment 
    rate and efficient tightness are derived in online appendix D (eqn A10 & A14). 
    
    Parameters
    -----------
    eta: pd.Series
        Matching elasticity.
    z: pd.Series
        Relative productivity of unemployed workers.
    c: pd.Series
        Recruiting cost.
    lamb: pd.Series
        Job-separation rate.
    omega: pd.Series
        Matching efficacy.
    r: pd.Series
        Discount rate.
    u0: scalar
        An initial value for the efficient unemployment rate.
    
    Returns
    --------
    pd.Series
        u_star: Efficient unemployment rate.
    pd.Series
        theta_star: Efficient labor-market tightness.
    '''


    return u_star, theta_star
    

