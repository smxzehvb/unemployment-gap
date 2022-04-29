import numpy as np
import pandas as pd

## functions:
### unemployment: compute_unemployment_gap,
### efficiency: compute_efficient_unemployment, compute_efficient_tightness,
### inverse: compute_beveridge_inverse, compute_recruiting_inverse, compute_nonwork_inverse

###############################################################
def compute_unemployment_gap(u, v, epsilon, zeta=0.26, kappa=0.92):
    '''
    This function computes the unemployment gap u_gap using the sufficient-statistic 
    formula in proposition 3 (eqn 5), the current unemployment rate u and vacancy rate v, 
    and three sufficient statistics: Beveridge elasticity epsilon, social value of nonwork 
    zeta, and recruiting cost kappa.
    
    Parameters
    -----------
    u: scalar or pd.Series
        Current unemployment rate.
    v: scalar or pd.Series
        Vacancy rate.
    epsilon: scalar or pd.Series
        Beveridge elasticity.
    zeta: scalar or pd.Series
        Social value of nonwork.
    kappa: scalar or pd.Series
        Recruiting cost.
    
    Returns
    --------
    pd.Series
        u_gap: Unemployment gap.
    '''
    
    u_gap = u - compute_efficient_unemployment(u, v, epsilon, zeta, kappa)
    
    return u_gap
    
###############################################################
def compute_efficient_unemployment(u, v, epsilon, zeta=0.26, kappa=0.92):
    '''
    This function computes the efficient unemployment rate using the sufficient-statistic 
    formula in proposition 3 (eqn 5), the current unemployment rate u and vacancy rate v, 
    and three sufficient statistics: Beveridge elasticity epsilon, social value of nonwork 
    zeta, and recruiting cost kappa.
    
    Parameters
    -----------
    u: scalar or pd.Series
        Current unemployment rate.
    v: scalar or pd.Series
        Vacancy rate.
    epsilon: scalar or pd.Series
        Beveridge elasticity.
    zeta: scalar or pd.Series
        Social value of nonwork.
    kappa: scalar or pd.Series
        Recruiting cost.
    
    Returns
    --------
    pd.Series   
        u_star: Efficient unemployment rate.
    '''
    
    C = (kappa * epsilon) / (1. - zeta)    
    u_star = np.power(  C * v / np.power(u, -epsilon) , 1./(1. + epsilon) )
    
    return u_star
    
###############################################################
def compute_efficient_tightness(epsilon, zeta=0.26, kappa=0.92):
    '''
    This function computes the efficient labor-market tightness using the sufficient-
    statistic formula in proposition 2 (eqn 4) and three sufficient statistics: 
    Beveridge elasticity epsilon, social value of nonwork zeta, and recruiting 
    cost kappa.
    
    Parameters
    -----------
    epsilon: scalar or pd.Series
        Beveridge elasticity.
    zeta: scalar or pd.Series
        Social value of nonwork.
    kappa: scalar or pd.Series
        Recruiting cost.
        
    Returns
    --------
    pd.Series
        theta: Efficient labor-market tightness.
    '''

    return (1. - zeta) / (kappa * epsilon)
    
###############################################################
def compute_beveridge_inverse(theta, zeta=0.26, kappa=0.92):
    '''
    This function computes the inverse-optimum Beveridge elasticity using the 
    sufficient-statistic formula in proposition 2 (eqn 17), the current labor-
    market tightness theta, and two sufficient statistics: social value of 
    nonwork zeta and recruiting cost kappa.

    Parameters
    -----------
    theta: scalar or pd.Series
        Current labor-market tightness.
    zeta: scalar or pd.Series
        Social value of nonwork.
    kappa: scalar or pd.Series
        Recruiting cost.
        
    Returns
    --------
    pd.Series
        Inverse-optimum Beveridge elasticity.
    '''

    return (1.0 - zeta) / (kappa * theta)
    
###############################################################
def compute_recruiting_inverse(theta, epsilon, zeta=0.26):
    '''
    This function computes the inverse-optimum recruiting cost using the 
    sufficient-statistic formula in proposition 2 (eqn 19), the current 
    labor-market tightness theta, and two sufficient statistics: Beveridge 
    elasticity epsilon and social value of nonwork zeta.
    
    Parameters
    -----------
    theta: scalar or pd.Series
        Current labor-market tightness.
    epsilon: scalar or pd.Series
        Beveridge elasticity.
    zeta: scalar or pd.Series
        Social value of nonwork.
        
    Returns
    --------
    pd.Series
        Inverse-optimum recruiting cost.
    '''
    
    return (1. - zeta) / (epsilon * theta)
    
###############################################################
def compute_nonwork_inverse(theta, epsilon, kappa=0.92):
    '''
    This function computes the inverse-optimum social value of nonwork using the 
    sufficient-statistic formula in proposition 2 (eqn 18), the current labor-
    market tightness theta, and two sufficient statistics: Beveridge elasticity 
    epsilon and recruiting cost kappa.
    
    Parameters
    -----------
    theta: scalar or pd.Series
        Current labor-market tightness.
    epsilon: scalar or pd.Series
        Beveridge elasticity.
    kappa: scalar or pd.Series
        Recruiting cost.
        
    Returns
    --------
    pd.Series
        Inverse-optimum social value of nonwork
    '''

    return 1. - (kappa * epsilon * theta)



