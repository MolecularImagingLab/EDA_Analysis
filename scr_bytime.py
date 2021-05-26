#!/usr/bin/env python

import pandas as pd
import numpy as np
sub1 = pd.read_csv('/home/rami/Documents/scr_all/AVL-001_era.txt', delim_whitespace = True)
sub2 = pd.read_csv('/home/rami/Documents/scr_all/AVL-003_era.txt', delim_whitespace = True)
sub3 = pd.read_csv('/home/rami/Documents/scr_all/AVL-004_era.txt', delim_whitespace = True)
sub4 = pd.read_csv('/home/rami/Documents/scr_all/AVL-006_era.txt', delim_whitespace = True)
sub5 = pd.read_csv('/home/rami/Documents/scr_all/AVL-007_era.txt', delim_whitespace = True)
sub6 = pd.read_csv('/home/rami/Documents/scr_all/AVL-011_era.txt', delim_whitespace = True)
sub7 = pd.read_csv('/home/rami/Documents/scr_all/AVL-101_era.txt', delim_whitespace = True)
sub8 = pd.read_csv('/home/rami/Documents/scr_all/AVL-102_era.txt', delim_whitespace = True)
sub9 = pd.read_csv('/home/rami/Documents/scr_all/AVL-105_era.txt', delim_whitespace = True)
subs = [sub1, sub2, sub3, sub4, sub5, sub6, sub7, sub8, sub9]

csm_all, ev_n_csm, csp_all, ev_n_csp, csps_all, ev_n_csps = ([] for i in range(0,6))
for sub in subs:
    csm = sub.loc[sub['Event.NID']==2, 'CDA.ISCR'].to_list()
    ev_n = sub.loc[sub['Event.NID']==2, 'Event.Nr'].to_list()
    csm_all.append(csm)
    ev_n_csm.append(ev_n)
    csp = sub.loc[sub['Event.NID']==1, 'CDA.ISCR'].to_list()
    ev_n = sub.loc[sub['Event.NID']==1, 'Event.Nr'].to_list()
    csp_all.append(csp)
    ev_n_csp.append(ev_n)
    csps = sub.loc[sub['Event.NID']==3, 'CDA.ISCR'].to_list()
    ev_n = sub.loc[sub['Event.NID']==3, 'Event.Nr'].to_list()
    csps_all.append(csps)
    ev_n_csps.append(ev_n)

# By Event, run 1: 0:14, run 2: 14:28, run 3: 28:42, run 4: 42:56
#CSP
csp_df = pd.DataFrame(data=csp_all).T
agg_csp = csp_df.assign(Event=[1 + (1)*i for i in range(len(csp_df))])[['Event'] + csp_df.columns.tolist()]
agg_csp.columns = ['Event', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9']
csp_melt = pd.melt(agg_csp[28:42], id_vars='Event', var_name='Subject', value_vars=['sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9'], value_name='SCR')

#CSM
csm_df = pd.DataFrame(data=csm_all).T
agg_csm = csm_df.assign(Event=[1 + (1)*i for i in range(len(csm_df))])[['Event'] + csm_df.columns.tolist()]
agg_csm.columns = ['Event', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9']
csm_melt = pd.melt(agg_csm[28:42], id_vars='Event', var_name='Subject', value_vars=['sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9'], value_name='SCR')

#CSPS
csps_df = pd.DataFrame(data=csps_all).T
agg_csps = csps_df.assign(Event=[1 + (1)*i for i in range(len(csps_df))])[['Event'] + csm_df.columns.tolist()]
agg_csps.columns = ['Event', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9']
csps_melt = pd.melt(agg_csps[6:11], id_vars='Event', var_name='Subject', value_vars=['sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9'], value_name='SCR')

#CONTRAST
cs_contrast = csp_df - csm_df
agg_contrast = cs_contrast.assign(Event=[1 + (1)*i for i in range(len(cs_contrast))])[['Event'] + cs_contrast.columns.tolist()]
agg_contrast.columns = ['Event', 'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9']
contrast_melt_half1 = pd.melt(agg_contrast[28:35], id_vars='Event', var_name='Subject', value_vars=['sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9'], value_name='SCR')
contrast_melt_half2 = pd.melt(agg_contrast[35:42], id_vars='Event', var_name='Subject', value_vars=['sub1', 'sub2', 'sub3', 'sub4', 'sub5', 'sub6', 'sub7', 'sub8', 'sub9'], value_name='SCR')
#6 CSPS, #14 CSP, #14 CSM

import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns
# agg_csp.iloc[0:13].plot(x='event', y='csp')
# agg_csm.iloc[0:13].plot(x='event', y='csm')
# agg_contrast.iloc[0:13].plot(x='Event', y='CS+ versus CS-\n Skin Conductance Recordings (uSiemens)')
fig, ax = plt.subplots(2,2, figsize=(20,14), gridspec_kw={
                           'width_ratios': [5, 1],
                         'height_ratios': [2, 2]})

ax[0,0].tick_params(width=4, length=10, labelsize=28, bottom=False, pad=15)
ax[1,0].tick_params(width=4, length=10, labelsize=28, bottom=False, pad=15)
ax[0,1].tick_params(width=4, length=10, labelsize=28, bottom=False, pad=15)
ax[1,1].tick_params(width=4, length=10, labelsize=28, bottom=False, pad=15)
sns.set_style("ticks")
# CSP
sns.barplot(data=csp_melt, x='Event', y='SCR', edgecolor='black', linewidth=3, ax=ax[0,0], ci=95, capsize=0.4, color='firebrick')
#sns.swarmplot(data=csp_melt, x='Event', y='SCR', edgecolor='black', linewidth=1.5, ax=ax[0], size=6)
ax[0,0].set_ylabel('CS+ (uSiemens)' ,fontsize=30)
ax[0,0].set_xlabel('Event #' ,fontsize=30)
# CSM
sns.barplot(data=csm_melt, x='Event', y='SCR', edgecolor='black', linewidth=3, ax=ax[1,0], ci=95, capsize=0.4, color='cornflowerblue')
ax[1,0].set_ylabel('CS- (uSiemens)',fontsize=30)
ax[1,0].set_xlabel('Event #' ,fontsize=30)
# CS CONTRAST FIRST HALF
sns.barplot(data=contrast_melt_half1, y='SCR', edgecolor='black', linewidth=3, ax=ax[0,1], ci=95, capsize=0.4, color='slateblue')
ax[0,1].set_ylabel('CS contrast (uSiemens)',fontsize=30)
ax[0,1].set_xlabel('Events 1-7' ,fontsize=30)
# CS CONTRAST SECOND HALF
sns.barplot(data=contrast_melt_half2, y='SCR', edgecolor='black', linewidth=3, ax=ax[1,1], ci=95, capsize=0.4, color='slateblue')
ax[1,1].set_ylabel('CS contrast (uSiemens)',fontsize=30)
ax[1,1].set_xlabel('Events 8-14' ,fontsize=30)
ax[0,0].spines['left'].set_linewidth(4)
ax[0,1].spines['left'].set_linewidth(4)
ax[1,0].spines['left'].set_linewidth(4)
ax[1,1].spines['left'].set_linewidth(4)
fig.suptitle('Skin Conductance Recordings (N=9)',fontsize=34, fontweight='bold')
sns.despine(bottom=True)
plt.tight_layout(pad=4)
plt.savefig('/home/rami/Downloads/run4_descriptive.jpg', dpi=300)
# CSPS
rc('font',**{'family':'sans-serif','sans-serif':['Computer Modern Sans serif']})
fig, ax = plt.subplots()
sns.set_style("ticks")
sns.set(font_scale=1.5)
sns.barplot(data=csps_melt, x='Event', y='SCR', edgecolor='black', linewidth=3, ax=ax, ci=95, capsize=0.4, color='firebrick')
#sns.swarmplot(data=csp_melt, x='Event', y='SCR', edgecolor='black', linewidth=1.5, ax=ax[0], size=6)
ax.set_ylabel('CS+Shock (uSiemens)' ,fontsize=18)
ax.title.set_text('CS+Shock by event #')
plt.savefig('/home/lauri/Downloads/run1_csps.jpg', dpi=300)
