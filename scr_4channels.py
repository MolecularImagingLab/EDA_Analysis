#!/usr/bin/env python
#! /home/lauri/anaconda3/bin/python

# Import libraries
import os, sys
import pandas as pd
import numpy as np

def grab_scr(root, scrpath):
    ''' Grab scr files for specific subject. '''
    subject_id = sys.argv[1]
    filefolder = os.path.join(root, subject_id, scrpath)
    print('Grabbing par files from:' + filefolder)
    files = os.listdir(filefolder)
    for f in files:
        if f.endswith('.txt'):
            results = f
    return results, subject_id

def assign_time(root, subject_id, scrpath, results):
    ''' Adds time variable based on sampling rate of 200 Hz. '''
    scr = pd.read_table(os.path.join(root,subject_id,scrpath,results), header=0, names=['microsiemens', 'stst', 'csps', 'csp', 'csm'], delim_whitespace=True)
    scr = scr.assign(time=[0 + (0.005)*i for i in range(len(scr))])[['time'] + scr.columns.tolist()]
    return scr

def extract_markers(scr):
    ''' Extracts time for each marker type. '''
    # Get starts and stops into list
    stst = (scr.loc[scr['stst']==5, 'time']).to_numpy(dtype='int64')
    # Get unique values only
    stst_u = np.unique(stst)
    # Get CS+US pairings
    csps = (scr.loc[scr['csps']==5, 'time']).to_numpy(dtype='int64')
    # Get unique values only
    csps_u = np.unique(csps)
    # Get CS plus
    csp = (scr.loc[scr['csp']==5, 'time']).to_numpy(dtype='int64')
    # Get unique values only
    csp_u = np.unique(csp)
    # Get CS minus
    csm = (scr.loc[scr['csm']==5, 'time']).to_numpy(dtype='int64')
    # Get unique values only - delete first csm from every run
    csm_u = np.unique(csm)
    csm_u = np.delete(csm_u, [0,14,28,42])
    markers = []
    for num in stst_u:
        markers.append([num,0])
    for num in csps_u:
        markers.append([num,3])
    for num in csp_u:
        markers.append([num,1])
    for num in csm_u:
        markers.append([num,2])
    return markers

def ledalab_form(markers, root, parpath, subject_id):
    ''' Saves marker info in Ledalab friendly format. '''
    newpar = pd.DataFrame(markers, columns=['time','nid'])
    newpar.sort_values(by='time', inplace=True, ignore_index=True)
    newpar.to_csv(os.path.join(root,subject_id,parpath,subject_id+'.synced.par'), index=False, header = True, sep='\t')

def main():
    # Hardcoded file path
    root = '/group/tuominen/EmoSal/subjects'
    scrpath = 'scr'
    parpath = 'par'
    # Execute functions
    results, subject_id = grab_scr(root, scrpath)
    scr = assign_time(root, subject_id, scrpath, results)
    markers = extract_markers(scr)
    ledalab_form(markers, root, parpath, subject_id)
    print('Synced par file saved.')
if __name__ == "__main__":
    # execute only if run as a script
    main()
