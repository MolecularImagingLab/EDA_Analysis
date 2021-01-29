#!/usr/bin/env python
#! /home/lauri/anaconda3/bin/python

#load libraries
import os, sys 
import pandas as pd
import numpy as np
import math

def readin():
# First argument is scr .txt file input, second argument is .par file input, third argument is .par file output
    input_scr = sys.argv[1]
    input_par = sys.argv[2]
    output_par = sys.argv[3]
    return input_scr, input_par, output_par

def scr_mod(input_scr):
    #Reads in scr file and adds headers
    input_scr, input_par, output_par = readin()
    scr = pd.read_table(input_scr, header=0, names=['microsiemens', 'ch1', 'ch2', 'ch3'], delim_whitespace=True)
    # Add time as a column, at a sampling rate of 200 Hz
    scr = scr.assign(time=[0 + (0.005)*i for i in range(len(scr))])[['time'] + scr.columns.tolist()]
    # View data
    # scr.plot.line(x='time', y=['microsiemens','ch1','ch2','ch3'])
    # Start at iloc of 0 defines the time @ first electrical impulse - start1
    start1 = (scr.loc[scr['ch2']==5, 'time'].iloc[0])
    # Every 10-11th float aftwerwards denotes an electrical impulse - starts,  except where there are test shocks
    starts = list(scr.loc[scr['ch2']==5, 'time'])
    allstartsrounded = [round(num, 0) for num in starts]
    # Remove duplicates
    allstartsunique = []
    for r in allstartsrounded:
        if r not in allstartsunique:
            allstartsunique.append(r)
    print('the following numbers are possible start times for the experiment:', allstartsunique)
    # Startstop at iloc of 0 defines the time of the last electrical impulse of first run - end1
    # end1 = (scr.loc[scr['ch1']==5, 'time'].iloc[0])
    # Every 10-11th float afterwards denotes the starts and stops of the runs, except where there are test shocks
    startstops = list(scr.loc[scr['ch1']==5, 'time'])
    # Removes values that are smaller than start1
    allstartstops = []
    for l in startstops:
         if l > start1:
            allstartstops.append(l)
    allstartstoprounded = [round(num, 0) for num in allstartstops]
    # Remove duplicates
    startstopunique = []
    for r in allstartstoprounded:
        if r not in startstopunique:
            startstopunique.append(r)
    print('the following numbers are possible stop and start times for the experiment:', startstopunique)
    startstopunique_list = []
    # If 4 starts and 4 stops are accounted for, ensure they are within time limit for a single run
    print('enter rounded starts and stops - a total of 8 sequential whole numbers:')
    for i in range(0, 8): # set up loop to run 8 times
        number = int(input('Please enter a start or stop:')) # prompt user for number
        startstopunique_list.append(number)
    print(startstopunique_list)
    # Check if input values are valid
    count=0
    finalstartstops = []
    for number in [0, 2, 4, 6]:
        if startstopunique_list[number+1] - startstopunique_list[number] == 483:
            count = count +1 
            finalstartstops.append(startstopunique_list[number])
            finalstartstops.append(startstopunique_list[number+1])
    # Confirms all 4 runs are accounted for
    if count ==4:
        print('number of runs accounted for:', count)
    # If all four runs of a session are accounted for, starts and stops are set below by finding exact value
    finalnumbers, start1, end1, start2, end2, start3, end3, start4, end4 = ([] for i in range(0,9))
    starts_list = [start1, start2, start3, start4]
    for z,i in enumerate([0,2,4,6]): # count, item
        for l in starts:
            if math.isclose(finalstartstops[i], l, abs_tol = 1):
                finalnumbers.append(l)
                starts_list[z].append(finalnumbers[0])
                finalnumbers = []
    ends_list = [end1, end2, end3, end4]
    for z,i in enumerate([1,3,5,7]): # count, item
        for l in startstops:
            if math.isclose(finalstartstops[i], l, abs_tol = 1):
                finalnumbers.append(l)
                ends_list[z].append(finalnumbers[0])
                finalnumbers = []
    return start1, end1, start2, end2, start3, end3, start4, end4

def par_mod(input_par, output_par, start1, end1, start2, end2, start3, end3, start4, end4):
# Must execute par_concat.py to successfully run this function
# Reads in .par file
    par = pd.read_csv(input_par)
# Calculates time to fill between runs
    fill1 = (start2[0]) - (end1[0])
    fill2 = (start3[0]) - (end2[0])
    fill3 = (start4[0]) - (end3[0])
# Calculates duration of each run
    duration1 = (end1[0]) - (start1[0])
    duration2 = (end2[0]) - (start2[0])
    duration3 = (end3[0]) - (start3[0])
    duration4 = (end4[0]) - (start4[0])
# Run 1; index 0-70, Run 2; index 70-140, Run 3; index 140-210, Run 4; index 210-280
    newpar = ((par.iloc[0::2]).copy()).reset_index()
    newpar.drop(axis = 1, columns = ['index'], inplace = True)
    onset = (newpar['Trial Onset']).values
    synced_onset = np.add(onset, start1[0])
    run1 = list(synced_onset[0:35])
    run2 = list(synced_onset[35:70] + fill1 + duration1)
    run3 = list(synced_onset[70:105] + fill1 + fill2 + duration1 + duration2) 
    run4 = list(synced_onset[105:140] + fill1 + fill2 + fill3 + duration1 + duration2 + duration3) 
    allruns = run1 + run2 + run3 + run4
# Replace old Trial Onsets with new Trial Onsets and save new par file compatible with Ledalab
    newpar['Trial Onset'] = allruns
    newpar.columns = ['time','nid','stim_dur','ones']
    newpar.drop(axis = 1, columns = ['stim_dur','ones'], inplace = True)
    newpar.to_csv(output_par, index=False, header = True, sep='\t')

def main():
    input_scr, input_par, output_par = readin()
    start1, end1, start2, end2, start3, end3, start4, end4 = scr_mod(input_scr)
    par_mod(input_par, output_par, start1, end1, start2, end2, start3, end3, start4, end4)
    print('scr and par modifications complete')
if __name__ == "__main__":
    # execute only if run as a script
    main()
