# BUG: Beveridgean Unemployment Gap in Python

This python package re-implements the computations associated with the paper "Beveridgean unemployment gap"
by Pascal Michaillat & Emmanuel Saez (2021). https://doi.org/10.1016/j.pubecp.2021.100009

The paper's code was originally implemented in MATLAB, and can be found on the project's 
[GitHub page](https://github.com/pascalmichaillat/unemployment-gap)

## Requirements

  * pandas
  * numpy
  * scipy
  * statsmodels
  * ruptures
  * matplotlib
  
## Development status

This package is a work-in-progress, academic package, and is not guaranteed to be robust.

This version has been tested with (from anaconda 4.12.0):

  * python==3.9.12
  * IPython==8.2.0
  * jupyter_core==4.9.2
  * pandas==1.4.2
  * numpy==1.21.5
  * scipy==1.7.3
  * statsmodels==0.13.2
  * matplotlib==3.5.1
  
Additional packages installed from pypi:

  * ruptures==1.1.6 
  
## Conversion crosswalk


| matlab file | python function | python file/notes | 
| :---------- | :-------------- | :---------: |	
| baiPerron.m					| `get_bp_breakpoints` 			 | breakpoints.py |
| getBreakDate.m				| `get_bp_breakpoints` 			 | ^^ |
|.....................................................|
| getBeveridgeElasticity.m		| `compute_beveridge_elasticity` | ^^ |
| computeUnemploymentGap.m			| `compute_unemployment_gap` 		| suffstats.py |
| computeEfficientTightness.m		| `compute_efficient_tightness` 	| ^ |
| computeEfficientUnemployment.m	| `compute_efficient_unemployment`  | ^ |
| computeBeveridgeInverse.m		| `compute_beveridge_inverse`  			| ^ |
| computeRecruitingInverse.m	| `compute_recruiting_inverse` 			| ^ |
| computeNonworkInverse.m		| `compute_nonwork_inverse`	   			| ^ |
| computeBeveridgeanUnemployment.m	| `compute_beveridgean_unemployment` | dmpmodel.py |
| computeMatchingElasticity.m		| `compute_matching_elasticity` 	 | ^ |
| computeMatchingEfficacy.m			| `compute_matching_efficacy`		 | ^ |
| computeSeparationEfficacy.m		| `compute_separation_efficacy`		 | ^ |
| computeEfficiencyEndogenous.m		| `compute_endogenous_efficiency`	 | ^ |
| computeEfficiencyHosios.m			| `compute_hosios_efficiency`		 | ^ |
| measureJobFinding.m			| `compute_job_finding_rate`  	| jobrates.py |
| measureJobSeparation.m		| `compute_job_separation_rate`	| ^ |
| getUnemploymentRate.m		| *depreciated*	| handled wth pandas functionality <br>  demonstrated in jupyter notebooks |
| getVacancyRate.m			| *depreciated*	| ^ |
| getRecessionDate.m		| *depreciated*	| ^ |
| getLaborProductivity.m	| *depreciated*	| ^ |
| getNairu.m				| *depreciated*	| ^ |
| getNaturalUnemployment.m	| *depreciated*	| ^ |
| getTrendUnemployment.m	| *depreciated*	| ^ |
| getTimeline.m 			| *depreciated*	| ^ |
| monthlyToQuarterly.m		| *depreciated*	| ^ |
| formatFigure.m			| *depreciated*	| handled wth matplotlib functionality <br>  demonstrated in jupyter notebooks |
| formatPlot.m				| *depreciated*	| ^ |
| figureX.m					| *depreciated*	| ^ |






