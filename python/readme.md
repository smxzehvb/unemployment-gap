# BUG: Beveridgean Unemployment Gap in Python

This python package re-implements the computations associated with the paper "Beveridgean unemployment gap"
by Pascal Michaillat & Emmanuel Saez (2021). [[link]](https://doi.org/10.1016/j.pubecp.2021.100009)

The paper's code was originally implemented in MATLAB, and can be found on the project's 
[GitHub page](https://github.com/pascalmichaillat/unemployment-gap)

## Requirements

  * pandas
  * numpy
  * scipy
  * statsmodels
  * ruptures
  * matplotlib
  * kneed

The package 'kneed' is only used in some of the example notebooks. It is not required for the execution of functions 
in the main bug package.   
  
## Development

This package is a work-in-progress, academic package, and is not guaranteed to be robust.

This version has been tested with python 3.9.12, from anaconda 4.12.0 for Linux 64-bit, and the following package versions:

  * IPython==8.2.0
  * jupyter_core==4.9.2
  * pandas==1.4.2
  * numpy==1.21.5
  * scipy==1.7.3
  * statsmodels==0.13.2
  * matplotlib==3.5.1
  
Additional packages installed from pypi:

  * ruptures==1.1.6
  * kneed==0.7.0
   
  
Development was done on a desktop running 64-bit Pop!_OS 22.04 LTS (a flavor of Ubuntu), with Intel Core i7-6700 CPU @3.40GHz ×8 and 32GB RAM. 
  
## Functions Conversion Crosswalk


| matlab file | python function | python file/notes | 
| :---------- | :-------------- | :---------: |	
|.....................................................|
| baiPerron.m					| `get_bp_breakpoints` 			 | breakpoints.py |
| baiPerron.m  					| `evaluate_num_breaks` 		 | ^ |
| getBreakDate.m				| `get_bp_breakpoints` 			 | ^ |
| getBeveridgeElasticity.m		| `compute_beveridge_elasticity` | ^ |
|.....................................................|
| computeUnemploymentGap.m			| `compute_unemployment_gap` 		| suffstats.py |
| computeEfficientTightness.m		| `compute_efficient_tightness` 	| ^ |
| computeEfficientUnemployment.m	| `compute_efficient_unemployment`  | ^ |
| computeBeveridgeInverse.m		| `compute_beveridge_inverse`  			| ^ |
| computeRecruitingInverse.m	| `compute_recruiting_inverse` 			| ^ |
| computeNonworkInverse.m		| `compute_nonwork_inverse`	   			| ^ |
|.....................................................|
| computeBeveridgeanUnemployment.m	| `compute_beveridgean_unemployment` | dmpmodel.py |
| computeMatchingElasticity.m		| `compute_matching_elasticity` 	 | ^ |
| computeMatchingEfficacy.m			| `compute_matching_efficacy`		 | ^ |
| computeSeparationEfficacy.m		| `compute_separation_efficacy`		 | ^ |
| computeEfficiencyEndogenous.m		| `compute_endogenous_efficiency`	 | ^ |
| computeEfficiencyHosios.m			| `compute_hosios_efficiency`		 | ^ |
|.....................................................|
| measureJobFinding.m			| `compute_job_finding_rate`  	| jobrates.py |
| measureJobSeparation.m		| `compute_job_separation_rate`	| ^ |
|.....................................................|
| 	*NA*					| `plot_beveridge_elasticity_series` |  viz.py  |
| 	*NA*					| `plot_beveridge_gap_series` |  ^  |
| 	*NA*					| `plot_beveridge_curve_fits` |  ^  |
| 	*NA*					| `plot_beveridge_curve_segments` |  ^  |
| formatPlot.m				| `format_plot`	| ^ |
| formatFigure.m			| *depreciated*	| ^ |
| figureX.m					| *depreciated*	| ^ |
|.....................................................|
| getUnemploymentRate.m		| *depreciated*	| handled wth pandas functionality <br>  demonstrated in jupyter notebooks |
| getVacancyRate.m			| *depreciated*	| ^ |
| getRecessionDate.m		| *depreciated*	| ^ |
| getLaborProductivity.m	| *depreciated*	| ^ |
| getNairu.m				| *depreciated*	| ^ |
| getNaturalUnemployment.m	| *depreciated*	| ^ |
| getTrendUnemployment.m	| *depreciated*	| ^ |
| getTimeline.m 			| *depreciated*	| ^ |
| monthlyToQuarterly.m		| *depreciated*	| ^ |



## Notebooks

Suggested order for exploring the example jupyter notebooks:

  1. BUG\_paper\_section\_2.ipynb
  1. BUG\_paper\_appendix\_B.ipynb
  1. BUG\_paper\_appendix\_C-D.ipynb
  1. BUG\_paper\_section\_5.ipynb
  1. BUG\_paper\_sec5-7\_appE.ipynb
  1. Computing\_Bev\_Gap\_w\_latest\_data.ipynb
  1. More\_on\_Breakpoints\_monthly\_series.ipynb
  1. Lots\_More\_on\_Breakpoints.ipynb

## References

More info on ruptures python package [[GitHub link]](https://github.com/deepcharles/ruptures):

  - C. Truong, L. Oudre, N. Vayatis. Selective review of offline change point detection methods. _Signal Processing_, 167:107299, 2020. [[journal]](https://doi.org/10.1016/j.sigpro.2019.107299) [[pdf]](http://www.laurentoudre.fr/publis/TOG-SP-19.pdf)




