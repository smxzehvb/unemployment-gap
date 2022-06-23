import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


###############################################
def format_plot(ax, rec_info=None,xgrid=True):

    if rec_info is not None:
        for idx, s in enumerate(rec_info[0]):
            plt.axvspan(rec_info[0][idx], rec_info[1][idx], facecolor='grey', alpha=0.6, zorder=-100)

    if xgrid:
        ax.grid(axis='x')

    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["bottom"].set_color('k')
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["left"].set_color('k')



##################################################
def plot_beveridge_elasticity_series(e, rec_info=None, color='blueviolet', figsize=(9, 6)):


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    e['E'].plot(ax=ax, color=color, linewidth=2, figsize=figsize)
    e[['LB', 'UB']].plot(ax=ax,color=color, linewidth=2,linestyle='dotted',)
    plt.legend()

    if rec_info is not None:
        for idx, s in enumerate(rec_info[0]):
            plt.axvspan(rec_info[0][idx], rec_info[1][idx], facecolor='grey', alpha=0.6, zorder=-100)

    plt.fill_between(e.index, e['UB'], e['LB'], color=color, alpha=.3)

    ax.grid(axis='x')

    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["bottom"].set_color('k')
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["left"].set_color('k')
	
    plt.ylabel('Beveridge Elasticity', fontsize=12)
    plt.title('Beveridge Elasticity', fontsize=14)
    
    return ax

##############################################################
def plot_beveridge_gap_series(gap, internal_bkps=None, rec_info=None, color='blue', figsize=(9, 6)):


    ax = gap.plot(figsize=figsize, linewidth=2, color=color, label='w/ '+str(len(internal_bkps))+' breakpoints')

    plt.axhline(y=0, color='magenta', linewidth=1.5,)

    if rec_info is not None:
        for idx, s in enumerate(rec_info[0]):
            plt.axvspan(rec_info[0][idx], rec_info[1][idx], facecolor='grey', alpha=0.6, zorder=-100)
    
    if internal_bkps is not None:     
        for b in internal_bkps:
            plt.axvline(x=b, color=color, linewidth=1.5, alpha=.8, linestyle='-.')
    
    ax.grid(axis='x')

    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["bottom"].set_color('k')
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["left"].set_color('k')
    
    plt.ylabel('Unemployment Gap', fontsize=12)
    plt.title('Beveridgean Unemployment Gap', fontsize=14)
    plt.legend()
    
    return ax


##############################################################
def plot_beveridge_curve_segments(log_u, log_v, bkps, color='teal', figsize=(6,6)):


    for idx, b in enumerate(bkps[:-1]):

        plt.figure(figsize = figsize)
        plt.plot(log_u, log_v, linewidth=1, color='grey')
        plt.plot(log_u.iloc[bkps[idx]:bkps[idx+1]],
                 log_v.iloc[bkps[idx]:bkps[idx+1]], 
                 linewidth=3, color=color)
    
        plt.annotate( str(log_u.index[bkps[idx]]), 
                     (log_u.iloc[bkps[idx]], log_v.iloc[bkps[idx]]) )
                 
        plt.annotate( str(log_u.index[bkps[idx+1]-1]), 
                     (log_u.iloc[bkps[idx+1]-1], log_v.iloc[bkps[idx+1]-1] ) )


        plt.gca().spines["bottom"].set_linewidth(1.5)
        plt.gca().spines["bottom"].set_color('k')
        plt.gca().spines["left"].set_linewidth(1.5)
        plt.gca().spines["left"].set_color('k')
    
        plt.ylabel('Log Vacancy Rate', fontsize=12)
        plt.xlabel('Log Unemployment Rate', fontsize=12)
    
        plt.title('Beveridge Curve '+str(log_u.index[bkps[idx]])+'--'+str(log_u.index[bkps[idx+1]-1]),
                  fontsize=14)

    
##############################################################
def plot_beveridge_curve_fits(log_u, log_v, bkps, fits, e, figsize=(8,8)):

    cmap = plt.get_cmap('CMRmap')
    colors = cmap( np.linspace(.1,.9,len(bkps)) )

    handles = []

    plt.figure(figsize = figsize)
    plt.plot(log_u, log_v, linewidth=1, color='grey')

    for idx, b in enumerate(bkps[:-1]):
    
        plt.plot(log_u.iloc[bkps[idx]:bkps[idx+1]],
                 log_v.iloc[bkps[idx]:bkps[idx+1]], 
                 linewidth=2, color=colors[idx], alpha=.7)
                 
    
        plt.plot(log_u.iloc[bkps[idx]:bkps[idx+1]], fits[idx],
                 linewidth=2.5, linestyle='dotted', color=colors[idx], alpha=.9)
    
        q = log_u.index[bkps[idx]]
        handles.append(Line2D([0], [0],color=colors[idx], linewidth=2,
                                  label=str(q)+' : '+ 
                                  str( round(e['E'].loc[q],2) )
                             ))


    plt.legend(handles=handles, bbox_to_anchor=(1,1), title='Period Beginning : Slope  ')
    
    plt.gca().spines["bottom"].set_linewidth(1.5)
    plt.gca().spines["bottom"].set_color('k')
    plt.gca().spines["left"].set_linewidth(1.5)
    plt.gca().spines["left"].set_color('k')
    
    plt.ylabel('Log Vacancy Rate', fontsize=12)
    plt.xlabel('Log Unemployment Rate', fontsize=12)
    
    plt.title('Beveridge Curve '+str(log_u.index[0])+'--'+str(log_u.index[-1]), fontsize=14)    


