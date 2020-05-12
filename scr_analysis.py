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
            data = os.path.join(scrpath,f)
            analysis = pd.read_table(data, delim_whitespace = True)
            for v in variables:
                csplusshockcda = (analysis.loc[analysis['Event.Name']==3, v]).tolist()
                cspstime = (analysis.loc[analysis['Event.Name']==3, 'Event.Nr']).tolist()
                cspluscda = (analysis.loc[analysis['Event.Name']==1, v]).tolist()
                csptime = (analysis.loc[analysis['Event.Name']==1, 'Event.Nr']).tolist()
                csminuscda = (analysis.loc[analysis['Event.Name']==2, v]).tolist()
                csmtime = (analysis.loc[analysis['Event.Name']==2, 'Event.Nr']).tolist()
                plt.plot(cspstime,csplusshockcda, label='3')
                plt.plot(csptime,cspluscda, label='1')
                plt.plot(csmtime, csminuscda, label='2')
                plt.xlabel('Event #',fontsize=15)
                plt.ylabel('microsiemens',fontsize=15)
                title = os.path.join(s,' ',v)
                plt.title(title, fontsize =20)
                blue_patch = mpatches.Patch(color='dodgerblue', label='CS Plus + Shock')
                yellow_patch = mpatches.Patch(color='goldenrod', label='CS Plus')
                green_patch = mpatches.Patch(color='forestgreen', label='CS Minus')
                plt.legend(handles=[blue_patch, yellow_patch, green_patch])
                plt.savefig(os.path.join('/home/lauri/Downloads/scrfigs/',s + v + '.jpg'), dpi=300)
                plt.clf()
