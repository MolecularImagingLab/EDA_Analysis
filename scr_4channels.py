#!/opt/anaconda3/bin/python
# Import libraries
import os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def grab_scr(root, scrpath):
    ''' Grab scr files for specific subject. '''
    subject_id = sys.argv[1]
    filefolder = os.path.join(root, scrpath, subject_id)
    print('Grabbing par files from:' + filefolder)
    files = os.listdir(filefolder)
    files = [f for f in files if 'era' not in f]
    for f in files:
        # FC.txt for AVLRAC to filter out baseline recordings
        if f.endswith('.txt'):
            results = f
    print(results)
    return results, subject_id

def assign_time(root, subject_id, scrpath, results):
    ''' Adds time variable based on sampling rate of 200 Hz. '''
    scr = pd.read_table(os.path.join(root,scrpath,subject_id,results), header=0,
    names=['microsiemens', 'stst', 'csps', 'csp', 'csm'], delim_whitespace=True)
    scr = scr.assign(time=[0 + (0.005)*i for i in range(len(scr))])[['time'] + scr.columns.tolist()]
    return scr

def filter_closeby(cs):
    # Should be 8 start/stops, 24 csps, 56 csp and 56 csm
    print('unique numbers before filter:', len(cs))
    threshold = 4
    diff = np.empty(cs.shape)
    diff[0] = np.inf
    diff[1:] = np.diff(cs)
    mask = diff > threshold
    cs = cs[mask]
    print('unique numbers after closeby filter:', len(cs))
    return cs

def filter_stst(stst_uf, cs):
    cs = np.asarray([c for c in cs if c not in stst_uf], dtype='int64')
    print('unique numbers after start/stop deletion ***: \n{}'.format(cs), len(cs))
    return cs

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
    # Get unique values only
    csm_u = np.unique(csm)
    # Filter close numbers
    print('--Starts & Stops--')
    stst_uf = filter_closeby(stst_u)
    # Filter close numbers and starts/stops
    print('--CSPS--')
    csps_uf = filter_closeby(csps_u)
    csps_uf = filter_stst(stst_uf, csps_uf)
    print('--CSP--')
    csp_uf = filter_closeby(csp_u)
    csp_uf = filter_stst(stst_uf, csp_uf)
    print('--CSM--')
    csm_uf = filter_closeby(csm_u)
    csm_uf = filter_stst(stst_uf, csm_uf)
    # Delete faulty csm - first csm of every run
    csm_uf = np.delete(csm_uf, [0,15,30,45])
    print('unique numbers after faulty CSM deletion *****:', len(csm_uf))
    # Order all events in a list
    markers = []
    for num in stst_uf:
        markers.append([num,0])
    for num in csps_uf:
        markers.append([num,3])
    for num in csp_uf:
        markers.append([num,1])
    for num in csm_uf:
        markers.append([num,2])
    return markers, csps_uf, csp_uf, csm_uf

def ledalab_form(markers, root, parpath, subject_id):
    ''' Saves marker info in Ledalab friendly format. '''
    newpar = pd.DataFrame(markers, columns=['time','nid'])
    newpar.sort_values(by='time', inplace=True, ignore_index=True)
    newpar.to_csv(os.path.join(root,parpath,subject_id+'.synced.par'), index=False, header = True, sep='\t')

def concat_scr(scr, iti, ti, cs):
    concat = []
    for c in cs[0:13]:
        concat.append((scr.loc[(scr['time'] >= c) & (scr['time'] <= c+ti), 'microsiemens'] - ( scr.loc[(scr['time'] >= c - iti) & (scr['time'] <= c), 'microsiemens'].agg('mean') ) ).tolist())
    con = pd.DataFrame(concat).mean()
    return con

def plot_eventavg(scr, name, cs):
    iti=2
    t=[4,5,6,7,8,9,10]
    fig, axes=plt.subplots(1,7,figsize=(20,4))
    for i, ti in enumerate(t):
        con = concat_scr(scr, iti, ti, cs)
        length = len(con)
        arr = np.arange(start = 0, stop = ti, step = ti/(length))
        try:
            axes[i].plot(arr, con)
        except:
            axes[i].plot(arr[:-1], con)
        axes[i].title.set_text(f'{ti} seconds from {name}')
    return fig

def main():
    # Hardcoded file path
    root = '/Users/ramihamati/Documents/PhD_Work/AVL'
    scrpath = 'SCR/SCR_JUNE2021'
    parpath = 'SCR/syncedpars'
    # Execute functions
    results, subject_id = grab_scr(root, scrpath)
    scr = assign_time(root, subject_id, scrpath, results)
    markers, csps, csp, csm = extract_markers(scr)
    ledalab_form(markers, root, parpath, subject_id)
    print('Synced par file saved.')
    dict = {'csps':csps, 'csp':csp, 'csm':csm}
    for cs in dict.keys():
        fig = plot_eventavg(scr, cs, dict[cs])
        fig.savefig(os.path.join(root,parpath,subject_id+f'.eventavg.{cs}.jpg'), dpi=300)
    print('Event avgs saved.')
if __name__ == "__main__":
    # execute only if run as a script
    main()
