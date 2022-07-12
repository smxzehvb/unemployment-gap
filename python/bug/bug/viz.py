import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


###############################################
def format_plot(ax, rec_info=None,xgrid=True):

    if rec_info is not None:
        for idx, s in enumerate(rec_info[0]):
            plt.axvspan(rec_info[0][idx], rec_info[1][idx], facecolor='grey', alpha=0.5, zorder=-100)

    if xgrid:
        ax.grid(axis='x')

    ax.spines["bottom"].set_linewidth(1.5)
    ax.spines["bottom"].set_color('k')
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["left"].set_color('k')



##################################################
def plot_beveridge_elasticity_series(e, rec_info=None, fill=True, color='blueviolet', figsize=(9, 6)):


    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    e['E'].plot(ax=ax, color=color, linewidth=2, figsize=figsize)
    e[['LB', 'UB']].plot(ax=ax,color=color, linewidth=2,linestyle='dotted',)
    

    if fill:
        plt.fill_between(e.index, e['UB'], e['LB'], color=color, alpha=.3)

    format_plot(ax, rec_info=rec_info, xgrid=True)
	
    plt.ylabel('Beveridge Elasticity', fontsize=12)
    plt.title('Beveridge Elasticity', fontsize=14)
    plt.legend()
    
    return ax

##############################################################
def plot_beveridge_gap_series(gap, internal_bkps=None, rec_info=None, linecolor='blue', figsize=(9, 6)):


    ax = gap.plot(figsize=figsize, linewidth=2, color=linecolor, label='Beveridge Gap')

    plt.axhline(y=0, color='magenta', linewidth=1.5,)
    
    if internal_bkps is not None:     
    
        cmap = plt.get_cmap('CMRmap')        
    
        if len(internal_bkps) == len(gap):
            # assuming these are class labels
            colors = cmap( np.linspace( .1,.9,max(internal_bkps)+1 ) )
            for idx, c in enumerate(internal_bkps):
                plt.axvline(x=gap.index[idx], color=colors[c], linewidth=1.5, alpha=.5, zorder=-20)
        else:
            # assuming these are temporal breakpoints
            colors = cmap( np.linspace( .1,.9,len(internal_bkps)+1 ) )
            
            plt.axvspan(gap.index[0], gap.index[1], facecolor=colors[0], alpha=0.5, zorder=-20)
            for idx, b in enumerate(internal_bkps[:-1]):
                plt.axvspan(internal_bkps[idx], internal_bkps[idx+1], facecolor=colors[idx], alpha=0.5, zorder=-20)
                plt.axvline(x=b, color=linecolor, linewidth=1.5, alpha=.8, linestyle='-.', zorder=-10)
                
            plt.axvspan(internal_bkps[-1], gap.index[-1], facecolor=colors[-1], alpha=0.5, zorder=-20)
            plt.axvline(x=internal_bkps[-1], color=linecolor, linewidth=1.5, alpha=.8, linestyle='-.', zorder=-10)
                    
    
    format_plot(ax, rec_info=rec_info, xgrid=True)
    
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


    plt.figure(figsize = figsize)
    ax = plt.plot(log_u, log_v, linewidth=1, color='grey', zorder=-10)


   
    if len(bkps) == len(log_u):
        # assume class label for each (integers starting at zero)
        _plot_class_fits(log_u, log_v, bkps, fits, e)

    else: 
        # else we plot contiguous segments
        _plot_segment_fits(log_u, log_v, bkps, fits, e)
        
    
    plt.gca().spines["bottom"].set_linewidth(1.5)
    plt.gca().spines["bottom"].set_color('k')
    plt.gca().spines["left"].set_linewidth(1.5)
    plt.gca().spines["left"].set_color('k')
    
    plt.ylabel('Log Vacancy Rate', fontsize=12)
    plt.xlabel('Log Unemployment Rate', fontsize=12)
    
    plt.title('Beveridge Curve '+str(log_u.index[0])+'--'+str(log_u.index[-1]), fontsize=14)    

###############################################
def _plot_segment_fits(log_u, log_v, bkps, fits, e):
    
    handles = []
    
    cmap = plt.get_cmap('CMRmap')
    colors = cmap( np.linspace(.1,.9,len(bkps)) )
    
    for idx, b in enumerate(bkps[:-1]):
    
        plt.plot(log_u.iloc[bkps[idx]:bkps[idx+1]],
                 log_v.iloc[bkps[idx]:bkps[idx+1]], linewidth=2, color=colors[idx], alpha=.7)
                 
        plt.plot(log_u.iloc[bkps[idx]:bkps[idx+1]], 
                 fits[idx],linewidth=2.5, linestyle='dotted', color=colors[idx], alpha=1)

    
        q = log_u.index[bkps[idx]]

        handles.append(Line2D([0], [0],color=colors[idx], linewidth=2,label=str(q)+' : '+ 
                      str( round(e[idx],2) )  ))

    plt.legend(handles=handles, bbox_to_anchor=(1,1), title='Period Beginning : Slope  ')



###############################################
def _plot_class_fits(log_u, log_v, labels, fits, e):
    
    handles = []
    
    cmap = plt.get_cmap('CMRmap')
    
    colors = cmap( np.linspace(.1,.9,max(labels)) ) 
    for c in sorted(np.unique(labels)):
        
        plt.scatter(log_u[labels==c],
                    log_v.iloc[labels==c],
                     color=colors[c], alpha=.95)            

        plt.plot(log_u[labels==c], fits[c],
                 linewidth=2.5, linestyle='dotted', color=colors[c], alpha=1)

        handles.append(Line2D([0], [0],color=colors[c], linewidth=2,
                                  label=str(c)+" : "+str( round(e[c],2) )  ))

    plt.legend(handles=handles, bbox_to_anchor=(1,1), title='Cluster : Slope')



