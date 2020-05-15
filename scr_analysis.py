#!/usr/bin/env python
#! /home/lauri/anaconda3/bin/python

#load libraries
import os, sys 
import pandas as pd
import numpy as np
from nilearn import plotting
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import seaborn as sns

#CDA.nSCR equal to number of peaks above threshold 
#CDA.AMpSum equal to amplitude sum of sig. peaks 
#CDA.PhasicMax equal to Maximum value of phaic activity

# Event-by-event data analysis for each subject
def by_event():
# Define file path
    subjectpath = '/media/lauri/My Passport/My_Computer/Documents/sync_me/EmoSal/subjects/'
    subjects = os.listdir(subjectpath)
# Define variables of importance
    variables = ['CDA.AmpSum','CDA.PhasicMax','CDA.SCR']
# Grab analysis file
    for s in subjects:
        scrpath = os.path.join('/media/lauri/My Passport/My_Computer/Documents/sync_me/EmoSal/subjects',s,'scr')
        files = os.listdir(scrpath)
        for f in files:
            if f.endswith('era.txt'):
# Read-in scr results table generated in Ledalab
                data = os.path.join(scrpath,f)
                analysis = pd.read_table(data, delim_whitespace = True)
# Read-in results and corresponding event type/number
                for v in variables:
                    csplusshockcda = (analysis.loc[analysis['Event.Name']==3, v]).tolist()
                    cspstime = (analysis.loc[analysis['Event.Name']==3, 'Event.Nr']).tolist()
                    cspluscda = (analysis.loc[analysis['Event.Name']==1, v]).tolist()
                    csptime = (analysis.loc[analysis['Event.Name']==1, 'Event.Nr']).tolist()
                    csminuscda = (analysis.loc[analysis['Event.Name']==2, v]).tolist()
                    csmtime = (analysis.loc[analysis['Event.Name']==2, 'Event.Nr']).tolist()
# Plot data by event number
                    plt.plot(cspstime,csplusshockcda, label='3')
                    plt.plot(csptime,cspluscda, label='1')
                    plt.plot(csmtime, csminuscda, label='2')
                    plt.xlabel('Event #',fontsize=15)
                    plt.ylabel('microsiemens',fontsize=15)
                    title = os.path.join(s,' ',v)
                    plt.title(title, fontsize =20)
# Make a manual legend (for 2+ items in legend)
                    blue_patch = mpatches.Patch(color='dodgerblue', label='CS Plus + Shock')
                    yellow_patch = mpatches.Patch(color='goldenrod', label='CS Plus')
                    green_patch = mpatches.Patch(color='forestgreen', label='CS Minus')
                    plt.legend(handles=[blue_patch, yellow_patch, green_patch])
                    plt.savefig(os.path.join('/home/lauri/Downloads/scrfigs/',s + v + '.jpg'), dpi=300)
                    plt.clf()

def by_run():
# Subject-by-subject data analysis for each stimulus by run
# Define file path
    subjectpath = '/media/lauri/My Passport/My_Computer/Documents/sync_me/EmoSal/subjects/'
    subjects = os.listdir(subjectpath)
# Define variables of importance
    variables = ['CDA.AmpSum','CDA.PhasicMax','CDA.SCR']
# Grab analysis file
    for s in subjects:
        scrpath = os.path.join('/media/lauri/My Passport/My_Computer/Documents/sync_me/EmoSal/subjects',s,'scr')
        files = os.listdir(scrpath)
        for f in files:
            if f.endswith('era.txt'):
# Read-in scr results table generated in Ledalab
                data = os.path.join(scrpath,f)
                analysis = pd.read_table(data, delim_whitespace = True)
                analysis['Event.Name'].replace(to_replace=3,value='csps', inplace=True)
                analysis['Event.Name'].replace(to_replace=2,value='csm', inplace=True)
                analysis['Event.Name'].replace(to_replace=1,value='csp', inplace=True)
                analysis['Event.Name'].replace(to_replace=0,value='iti', inplace=True)
# Plot data by run number
                sns.set_style("dark")
                allruns = (sns.violinplot(x='Event.Name', y='CDA.PhasicMax', data=analysis, inner="points", order=['iti','csm','csp','csps']).set_title('All Runs')).get_figure()
                allruns.savefig(os.path.join('/home/lauri/Downloads/scrfigs/',s + 'allruns.jpg'), dpi=300)
                plt.clf()
                run1 = sns.violinplot(x='Event.Name', y='CDA.PhasicMax', data=analysis[0:35], inner="points", order=['iti','csm','csp','csps']).set_title('Run 1').get_figure()
                run1.savefig(os.path.join('/home/lauri/Downloads/scrfigs/',s + 'run1.jpg'), dpi=300)
                plt.clf()
                run2 = sns.violinplot(x='Event.Name', y='CDA.PhasicMax', data=analysis[35:70], inner="points", order=['iti','csm','csp','csps']).set_title('Run 2').get_figure()
                run2.savefig(os.path.join('/home/lauri/Downloads/scrfigs/',s + 'run2.jpg'), dpi=300)
                plt.clf()
                run3 = sns.violinplot(x='Event.Name', y='CDA.PhasicMax', data=analysis[70:105], inner="points", order=['iti','csm','csp','csps']).set_title('Run 3').get_figure()
                run3.savefig(os.path.join('/home/lauri/Downloads/scrfigs/',s + 'run3.jpg'), dpi=300)
                plt.clf()
                run4 = sns.violinplot(x='Event.Name', y='CDA.PhasicMax', data=analysis[105:140], inner="points", order=['iti','csm','csp','csps']).set_title('Run 4').get_figure()
                run4.savefig(os.path.join('/home/lauri/Downloads/scrfigs/',s + 'run4.jpg'), dpi=300)
                plt.clf()

def all_subs_stimuli():
# All subjects data analysis for each stimulus
# Define file path
subjectpath = '/media/lauri/My Passport/My_Computer/Documents/sync_me/EmoSal/subjects/'
subjects = os.listdir(subjectpath)
# Define variables of importance
variables = ['CDA.AmpSum','CDA.PhasicMax','CDA.SCR']
# Grab analysis file and set storage variables
iti = []
csm = []
csp = [] 
csps = []
for s in subjects:
    scrpath = os.path.join('/media/lauri/My Passport/My_Computer/Documents/sync_me/EmoSal/subjects',s,'scr')
    files = os.listdir(scrpath)
    for f in files:
        if f.endswith('era.txt'):
# Read-in scr results table generated in Ledalab
            data = os.path.join(scrpath,f)
            analysis = pd.read_table(data, delim_whitespace = True)
# Average the data (by run) and append to grouped data
# Average the data (all 4 runs) and append to grouped data 
            avg = analysis.groupby('Event.Name').agg(np.mean)
            iti.extend(avg.loc[avg['Event.NID']==0, 'CDA.PhasicMax'].to_list())
            csm.extend(avg.loc[avg['Event.NID']==2, 'CDA.PhasicMax'].to_list())
            csp.extend(avg.loc[avg['Event.NID']==1, 'CDA.PhasicMax'].to_list())
            csps.extend(avg.loc[avg['Event.NID']==3, 'CDA.PhasicMax'].to_list())
# Plot results
iti = pd.DataFrame(iti, index = [0,1,2,3,4,5,6,7,8], columns = ['ITI'])
csm = pd.DataFrame(csm, index = [0,1,2,3,4,5,6,7,8], columns = ['CS minus'])
csp = pd.DataFrame(csp, index = [0,1,2,3,4,5,6,7,8], columns = ['CS plus'])
csps = pd.DataFrame(csps, index = [0,1,2,3,4,5,6,7,8], columns = ['CS plus Shock'])
concat = pd.DataFrame.join(iti, [csm, csp, csps])
sns.set_style('dark')
sns.set_palette('Dark2')
alldata = (sns.barplot(data=concat, linewidth=2.5, capsize=0.2, order=['ITI','CS minus','CS plus','CS plus Shock']).set_title('Skin Conductance Recordings (N = 9)'))
alldata = (sns.stripplot(data=concat, linewidth=2.5, jitter=True, order=['ITI','CS minus','CS plus','CS plus Shock']).set_title('Skin Conductance Recordings (N = 9)')).get_figure()
plt.xlabel('Conditions')
plt.ylabel('Phasic Max (Microsiemens)')
alldata.savefig(os.path.join('/home/lauri/Downloads/scrfigs/','alldata_scr_contrast.jpg'), dpi=300)
plt.clf()

def by_run_contrast():
# All subjects data analysis for contrasts by run
# Define file path
subjectpath = '/media/lauri/My Passport/My_Computer/Documents/sync_me/EmoSal/subjects/'
subjects = os.listdir(subjectpath)
# Define variables of importance
variables = ['CDA.AmpSum','CDA.PhasicMax','CDA.SCR']
# Grab analysis file and set storage variables
iti = []
csm = []
csp = [] 
csps = []
for s in subjects:
    scrpath = os.path.join('/media/lauri/My Passport/My_Computer/Documents/sync_me/EmoSal/subjects',s,'scr')
    files = os.listdir(scrpath)
    for f in files:
        if f.endswith('era.txt'):
# Read-in scr results table generated in Ledalab
            data = os.path.join(scrpath,f)
            analysis = pd.read_table(data, delim_whitespace = True)
# Average the data (by run) and append to grouped data
            run1_avg = analysis[0:35].groupby('Event.Name').agg(np.mean)
            run2_avg = analysis[35:70].groupby('Event.Name').agg(np.mean)
            run3_avg = analysis[70:105].groupby('Event.Name').agg(np.mean)
            run4_avg = analysis[105:140].groupby('Event.Name').agg(np.mean)
            runs = [run1_avg, run2_avg, run3_avg, run4_avg]
            for r in runs:
                iti.extend(r.loc[r['Event.NID']==0, 'CDA.PhasicMax'].to_list())
                csm.extend(r.loc[r['Event.NID']==2, 'CDA.PhasicMax'].to_list())
                csp.extend(r.loc[r['Event.NID']==1, 'CDA.PhasicMax'].to_list())
                csps.extend(r.loc[r['Event.NID']==3, 'CDA.PhasicMax'].to_list())
# Create new dataframes 
iti = pd.DataFrame(iti, index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35], columns = ['ITI'])
csm = pd.DataFrame(csm, index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35], columns = ['CS minus'])
csp = pd.DataFrame(csp, index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35], columns = ['CS plus'])
csps = pd.DataFrame(csps, index = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35], columns = ['CS plus Shock'])
concat = pd.DataFrame.join(iti, [csm, csp, csps])
contrast = concat['CS plus'] - concat['CS minus']
run1 = pd.DataFrame(contrast[0:9], index = [0,1,2,3,4,5,6,7,8], columns = ['Run 1'])
run2 = (pd.DataFrame(contrast[9:18], index = [9,10,11,12,13,14,15,16,17], columns = ['Run 2'])).reset_index()
run3 = (pd.DataFrame(contrast[18:27], index = [18,19,20,21,22,23,24,25,26], columns = ['Run 3'])).reset_index()
run4 = (pd.DataFrame(contrast[27:36], index = [27,28,29,30,31,32,33,34,35], columns = ['Run 4'])).reset_index()
concat_contrast = pd.concat([run1, run2, run3, run4], axis=1)
concat_contrast.drop(columns='index', inplace=True)
# Plot Results
sns.set_style('dark')
sns.set_palette('Dark2')
alldata = (sns.barplot(data=concat_contrast, linewidth=2.5, capsize=0.2, edgecolor='black').set_title('CS+ versus CS-'))
alldata = (sns.stripplot(data=concat_contrast, linewidth=2.5, jitter=True).set_title('CS+ versus CS-')).get_figure()
plt.xlabel('Sessions')
plt.ylabel('Phasic Max (Microsiemens)')
alldata.savefig(os.path.join('/home/lauri/Downloads/scrfigs/','scr_contrast_byrun.jpg'), dpi=300)

