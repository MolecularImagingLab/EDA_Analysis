#!/group/tuominen/anaconda3/bin/python

# Import libraries
import glob, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns

def import_scr(root, exclude):
    path = root
    all_files = glob.glob(os.path.join(path, "*era.txt"))
    # Remove those not included in analysis
    exclude = exclude
    all_filesf = [f for f in all_files if exclude not in f]
    print('Number of subjects:', len(all_filesf))
    # Read in files
    dfs = []
    for file in all_filesf:
        dfs.append(pd.read_csv(file, delim_whitespace=True))
    return dfs

def extract_scr(dfs, var):
    #CDA.PhasicMax equal to maximum value of phasic activity [muS]
    #CDA.ISCR equal to area (time window * SCR) [muS * s]
    #CDA.SCR equal to average SCR [muS]
    csm_all, ev_n_csm, csp_all, ev_n_csp, csps_all, ev_n_csps = ([] for i in range(0,6))
    for sub in dfs:
        csm = sub.loc[sub['Event.NID']==2, var].to_list()
        ev_n = sub.loc[sub['Event.NID']==2, 'Event.Nr'].to_list()
        csm_all.append(csm)
        ev_n_csm.append(ev_n)
        csp = sub.loc[sub['Event.NID']==1, var].to_list()
        ev_n = sub.loc[sub['Event.NID']==1, 'Event.Nr'].to_list()
        csp_all.append(csp)
        ev_n_csp.append(ev_n)
        csps = sub.loc[sub['Event.NID']==3, var].to_list()
        ev_n = sub.loc[sub['Event.NID']==3, 'Event.Nr'].to_list()
        csps_all.append(csps)
        ev_n_csps.append(ev_n)
        return csm_all, ev_n_csm, csp_all, ev_n_csp, csps_all, ev_n_csps

def process_scr(sm_all, ev_n_csm, csp_all, ev_n_csp, csps_all, ev_n_csps):
    # By Event, run 1: 0:14, run 2: 14:28, run 3: 28:42, run 4: 42:56
    #6 CSPS, #14 CSP, #14 CSM
    # Create column names

    columns = [f[-15:-8] for f in all_files]
    columns.insert(0, 'Event')

    #CSP
    csp_df = pd.DataFrame(data=csp_all).T
    csp_df = csp_df.iloc[0:56,:]
    agg_csp = csp_df.assign(Event=[1 + (1)*i for i in range(len(csp_df))])[['Event'] + csp_df.columns.tolist()]
    agg_csp.columns = columns
    agg_csp['Marker'] = 'CSp'
    agg_csp['Run'] = 0
    for ev in agg_csp.index:
        if int(ev) in range(0,14):
            agg_csp.iloc[ev, -1] = 1
        elif int(ev) in range(14,28):
            agg_csp.iloc[ev, -1] = 2
        elif int(ev) in range(28,42):
            agg_csp.iloc[ev, -1] = 3
        elif int(ev) in range(42,56):
            agg_csp.iloc[ev, -1] = 4

    #CSM
    csm_df = pd.DataFrame(data=csm_all).T
    csm_df = csm_df.iloc[0:56,:]
    agg_csm = csm_df.assign(Event=[1 + (1)*i for i in range(len(csm_df))])[['Event'] + csm_df.columns.tolist()]
    agg_csm.columns = columns
    agg_csm['Marker'] = 'CSm'
    agg_csm['Run'] = 0
    for ev in agg_csm.index:
        if int(ev) in range(0,14):
            agg_csm.iloc[ev, -1] = 1
        elif int(ev) in range(14,28):
            agg_csm.iloc[ev, -1] = 2
        elif int(ev) in range(28,42):
            agg_csm.iloc[ev, -1] = 3
        elif int(ev) in range(42,56):
            agg_csm.iloc[ev, -1] = 4

    #CSPS
    csps_df = pd.DataFrame(data=csps_all).T
    csps_df = csps_df.iloc[0:24,:]
    agg_csps = csps_df.assign(Event=[1 + (1)*i for i in range(len(csps_df))])[['Event'] + csm_df.columns.tolist()]
    agg_csps.columns = columns
    agg_csps['Marker'] = 'CSps'
    agg_csps['Run'] = 0
    for ev in agg_csps.index:
        if int(ev) in range(0,6):
            agg_csps.iloc[ev, -1] = 1
        elif int(ev) in range(6,12):
            agg_csps.iloc[ev, -1] = 2
        elif int(ev) in range(12,18):
            agg_csps.iloc[ev, -1] = 3
        elif int(ev) in range(18,24):
            agg_csps.iloc[ev, -1] = 4

    #ALL
    all_stims = pd.concat([agg_csp, agg_csm], axis=0)
    allmelt = pd.melt(all_stims, id_vars=['Run','Event','Marker'], var_name='Subject', value_vars=[sub for sub in columns[1:]], value_name='SCR')
    return allmelt

def plot_scr(allmelt, dpath):
    # Figure size
    fig, ax = plt.subplots(1,4, figsize=(20,5))
    # Barplot colours
    # Tick params
    sns.set_style("ticks")
    # Plot
    for i, r in enumerate([[1,8], [2,22], [3,36], [4,50]]):
        sns.pointplot(data=allmelt.loc[(allmelt['Run'] == r[0])], x='Marker', y='SCR', edgecolor='black', linewidth=3,
        ax=ax[i], ci=95, capsize=0.2, palette='Set1', join=False)
        ax[i].set_ylabel('' ,fontsize=24)
        ax[i].set_xlabel('Run {}'.format(r[0]) ,fontsize=24)
        ax[i].set_xticklabels(['CS-', 'CS+'])
        # Spine settings
        ax[i].tick_params(width=3, length=10, labelsize=20, bottom=False, pad=15)
        ax[i].spines['left'].set_linewidth(3)
    ax[0].set_ylabel('Average phasic \npeak activity [muS]' ,fontsize=24)
    sns.despine(bottom=True)
    plt.tight_layout()
    plt.savefig(os.path.join(dpath, 'scr_byrun.jpg'), dpi=300)

def main():
    # Hardcoded file path to existing BIDS dataset
    root = '/Users/ramihamati/Documents/PhD_Work/AVL/SCR/syncedpars'
    dpath = '/Users/ramihamati/Downloads'
    exclude = 'AVL-001'
    # select variable of interest
    var = 'CDA.PhasicMax'
    # Execute functions
    dfs = import_scr(root, exclude)
    csm_all, ev_n_csm, csp_all, ev_n_csp, csps_all, ev_n_csps = extract_scr(dfs, var)
    allmelt = process_scr(sm_all, ev_n_csm, csp_all, ev_n_csp, csps_all, ev_n_csps)
    plot_scr(allmelt, dpath)
if __name__ == "__main__":
# execute only if run as a script
    main()
