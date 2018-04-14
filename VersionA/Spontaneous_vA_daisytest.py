#opened 12/12/16
#edited 5/23/17 to add in stop cue timing and ratings
#editing 6/26/17 to pseudorandomize pictures
#still need to pseduorandomize ISI 
#SERP fMRI
#Spontaneous Script Version A
#---------------------------------------------------------
#Experiment description: 3 blocks of 10 pictures each. No cue for what 
#participant should use on the block of pictures.
#Version 1(A) of 3.
#---------------------------------------------------------
import os
import serial
import sys
import numpy as np
import pandas as pd
import psychopy.gui
import psychopy.visual
import psychopy.event
import psychopy.core
from psychopy import data, logging, sound, visual
from psychopy.constants import *  # things like STARTED, FINISHED
from random import randint
from random import shuffle
import time

def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))
#----------------------------------------------------
#Set up----------------------------------------------
#----------------------------------------------------
#
#----Get subject ID----
gui = psychopy.gui.Dlg()
gui.addField("Subject ID:")
gui.show()
subj_id = gui.data[0]
print subj_id
#----read in pre-specified pseudorandom order of conditions-----
co=pd.read_csv("/Users/whalenlab/Desktop/Experiments/SERP/VersionA/spontAimageorder.csv", header=None); #column1 is block 1 image order; column 2 is block 2 image order; column 3 is block 3 image order 
imagelist=pd.read_csv("/Users/whalenlab/Desktop/Experiments/SERP/VersionA/spontAimages.csv", header=None); #trial ID of neutral and negative; first 9 neutral, last 21 negative
neu_list = imagelist.iloc[:9]
neg_list = imagelist.iloc[9:]

assert len(neu_list) == 9
assert len(neg_list) == 21

imageDur = 1
print neu_list
print neg_list
#
#----Create file path for experiment timing data----
data_path = "Sponteneous_vA_"+str(subj_id)+".csv";
while os.path.exists(data_path): #if path exists, rename it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subj_id = subj_id+"000"
    data_path = "Spontenous_vA_"+str(subj_id)+".csv"
data_path2 = "Sponteneous_vA_"+str(subj_id)+"_cue.csv";

#
#----Configuration for USB serial input for scanner trigger
#serial_settings = {
    #'mount': '/dev/tty.USA19H141P1.1',   # May need to change per computer
    #'baud': 115200,
    #'timeout': .0001
#}
#fmri_settings = {
    #'sync': '5',         # character to use as the sync timing event
#}
#
#
#----Declare experiment variables
#
num_blocks = 3
num_stim = 30
num_cues = 2
num_reps = 10
num_vars = 5; #variables: subj_ID, trial#, photoID, Photo Onset, Response
neu_list.sample(frac=1)#randomize which neutral image is displayed
neg_list.sample(frac=1) #randomize which neg image displayed
#break randomized photo stim into 3 groups of 10
#moved counter=0 down to the beginning of each loop

#IF YOU WANT FIXED RANDOM NUMBERS (I.E., ACROSS SUBJECTS)
#SET THE RANDOM NUMBER GENERATOR SEED (1, 2, 3) FOR THE THREE BLOCKS
#create 3 groups of 10 random ISIs between 2 and 6 within a uniform 
#distribution that all add up to 40 seconds (total time of ISIs in 1 block)
Block1Seed = np.random.seed(1)
jitter1 = np.random.uniform(low=2, high=6, size=10);
jitter1 = jitter1 / np.sum(jitter1) * 40

Block2Seed = np.random.seed(2)
jitter2 = np.random.uniform(low=2, high=6, size=10);
jitter2 = jitter2 / np.sum(jitter2) * 40

Block3Seed = np.random.seed(3)
jitter3 = np.random.uniform(low=2, high=6, size=10);
jitter3 = jitter3 / np.sum(jitter3) * 40

#-------Variables Cont.
X=np.zeros((num_stim,num_vars));   #Create blank vector to store timing data
Xcue=np.zeros((num_blocks,num_cues))
Exp_cl = psychopy.core.Clock();#clock for keeping track of image/question presentation throughout experiment
Cue = "Block_Cue.jpg"
#
#-----------------------------
#----Open experiment window----
#-----------------------------
win = psychopy.visual.Window(
    size=[1280, 800],
    units="pix",
    fullscr=True,
    color=[-1, -1, -1]
)

#-----------------------------
#----Open experiment window----
#-----------------------------
win = psychopy.visual.Window(
    size=[1280, 800],
    units="pix",
    fullscr=True,
    color=[-1, -1, -1]
)
win.mouseVisible = False

myRatingScale = visual.RatingScale(
    win=win, 
    choices=map(str, range(-4, 5)), 
    low=-4, high=4, 
    precision=1, 
    labels=('Negative', 'Positive'), 
    markerStart=4, 
    size=1.5, 
    showAccept=False, 
    leftKeys='1', rightKeys='2', 
    maxTime=4, 
    noMouse=True
)
#----Declare image and text variables
welcome_text = psychopy.visual.TextStim(
    win=win,
    text="Waiting for scanner...",
    color=[1, 1, 1],
    height=35
)

#
fixation_text = psychopy.visual.TextStim(
    win=win,
    text="+",
    color=[1,1,1],
    height=35
)

myItem = psychopy.visual.TextStim(
    win=win,
    text="How negative or positive do you feel?",
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000,
    alignHoriz='center'
)
finish_text = psychopy.visual.TextStim(
    win=win,
    text="Please wait...",
    color=[1, 1, 1],
    height=35,
    wrapWidth=1000
)
#Start and Stop White Block Cue
Cue_filename ="/Users/whalenlab/Desktop/Experiments/SERP/"+ Cue
Cue_img = psychopy.visual.ImageStim(
    win=win,
    image= Cue_filename,
    units="pix"
)
  #scale image?
#----Set up opening of exp. with fMRI trigger-------
#---------------------------------------------------------
#welcome_text.draw()
#win.flip()
#psychopy.event.waitKeys()
#
#ser = serial.Serial(
    #serial_settings['mount'],
    #serial_settings['baud'],
    #timeout = serial_settings['timeout']
#)
#ser.flushInput()
#trigger = ''
#while trigger != fmri_settings['sync']:
    #welcome_text.draw()
    #win.flip()
    #trigger = ser.read()
#ser.close()
#
#---------------------------------------------------------
#----Begin experiment blocks------------------------------
#---------------------------------------------------------
#Set Exp clock to 0 at beginning of experiment
Exp_cl.reset(0)


#fixation
fixation_text.draw()
win.flip()
psychopy.core.wait(2)#CHANGE THIS BACK TO 20!!!
#
Cue_img.draw()
Cue_onset = Exp_cl.getTime()
win.flip()
psychopy.core.wait(2)
#----------------------------
#----------BLOCK 1-----------
#----------------------------
blocknum=0;

block1order = co.iloc[:,0];
print block1order

# Set counters equal to 0 (note that neg_list has weird Pandas indexing)
neu_counter=0
neg_counter=9

for i in range(0, num_reps):
    this_trial = block1order[i];
    if this_trial == 'Neutral':
        filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ str(neu_list[0][neu_counter]) +".jpg"
        print neu_list[0][neu_counter]
        neu_counter = neu_counter+1
        print neu_counter
    else:
        filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ str(neg_list[0][neg_counter]) +".jpg"
        neg_counter = neg_counter+1
        print neg_counter
        
    img = psychopy.visual.ImageStim(
        win=win,
        image=filename,
        units="pix"
    )
    size_x = img.size[0]
    size_y = img.size[1]
    img.size = [size_x, size_y]   #scale image
    img.draw()
    win.flip()
    PhotoOnset = Exp_cl.getTime()
    psychopy.core.wait(imageDur)
    
    #ISI
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(jitter1[i])
    
    #need to collect response--
    myRatingScale.reset()
    while myRatingScale.noResponse:  # while rating scale has been up < 4 secs
        myItem.draw()
        #key = ser.read()
        #psychopy.event._onPygletKey(symbol=key, modifiers=None, emulated=True)
        myRatingScale.draw()
        win.flip()
    
    Response_History = len(myRatingScale.getHistory())
    Response = myRatingScale.getRating()
    print 'rating =', myRatingScale.getRating()
    print 'history', myRatingScale.getHistory()
    
   
    #---collect response----
    
    X[i,0] = subj_id;
    X[i,1] = i+1; #trial number
    if this_trial is 'Neutral':
        X[i,2] = get_num(neu_list[0][neu_counter]);
    elif this_trial is 'Negative':
        X[i,2] = get_num(neg_list[0][neg_counter]);
    X[i,3] = PhotoOnset; #Time photo was presented in overall exp timeline
    X[i,4] = myRatingScale.getRating()
    
    # Okay end of loop, incrementing counter
    neu_counter = neu_counter+1
    neg_counter = neg_counter+1
    
Cue_img.draw()
win.flip()
psychopy.core.wait(2)   
Cue_offset = Exp_cl.getTime()

# collect cue timing out of block
Xcue[blocknum,0]=Cue_onset;
Xcue[blocknum,1]=Cue_offset;
   
#Interblock rest
fixation_text.draw()
win.flip()
psychopy.core.wait(20)

#
Cue_img.draw()
Cue_onset = Exp_cl.getTime()
win.flip()
psychopy.core.wait(2)
#----------------------------
#----------BLOCK 2-----------
#----------------------------
blocknum = blocknum + 1;

block2order = co.iloc[:,1];
print block2order

# Set counters equal to 0 (note that neg_list has weird Pandas indexing)

for i in range(0, num_reps):
    this_trial = block2order[i];
    if this_trial is 'Neutral':
        filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ str(neu_list[0][neu_counter]) +".jpg"
        neu_counter = neu_counter+1
        print neu_counter
    else:
        filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ str(neg_list[0][neg_counter]) +".jpg"
        neg_counter = neg_counter+1
        print neg_counter
    img = psychopy.visual.ImageStim(
        win=win,
        image=filename,
        units="pix"
    )
    size_x = img.size[0]
    size_y = img.size[1]
    img.size = [size_x, size_y]   #scale image
    img.draw()
    win.flip()
    PhotoOnset = Exp_cl.getTime()
    psychopy.core.wait(imageDur)
    
    #ISI
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(jitter2[i])
    
    #---collect response----
    X[i+10,0] = subj_id;
    X[i+10,1] = i+11; #trial number
    if this_trial is 'Neutral':
        X[i+10,2] = get_num(neu_list[0][neu_counter]);
    elif this_trial is 'Negative':
        X[i+10,2] = get_num(neg_list[0][neg_counter]);
    X[i+10,3] = PhotoOnset; #Time photo was presented in overall exp timeline
    X[i+10,4] = myRatingScale.getRating()
    
    # Okay end of loop, incrementing counter
    neu_counter = neu_counter+1
    neg_counter = neg_counter+1
        
   

Cue_img.draw()
win.flip()
psychopy.core.wait(2)   
Cue_offset = Exp_cl.getTime()


# collect cue timing out of block
Xcue[blocknum,0]=Cue_onset;
Xcue[blocknum,1]=Cue_offset;

#Interblock rest
fixation_text.draw()
win.flip()
psychopy.core.wait(20)
#
#
Cue_img.draw()
Cue_onset = Exp_cl.getTime()
win.flip()
psychopy.core.wait(2)
#----------------------------
#----------BLOCK 3-----------
#----------------------------

blocknum = blocknum + 1;
block3order = co.iloc[:,2];
print block3order

# Set counters equal to 0 (note that neg_list has weird Pandas indexing)

# For each block, remove early counter and move to end of loop (after response),
# and add if/elif statement to collect response, should match filename variable (neu_list[0][neu_counter])

for i in range(0, num_reps):
    this_trial = block3order[i];
    if this_trial is 'Neutral':
        filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ str(neu_list[0][neu_counter]) +".jpg"
        neu_counter = neu_counter+1
        print neu_counter
    else:
        filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ str(neg_list[0][neg_counter]) +".jpg"
        neg_counter = neg_counter+1
        print neg_counter
    img = psychopy.visual.ImageStim(
        win=win,
        image=filename,
        units="pix"
    )
    size_x = img.size[0]
    size_y = img.size[1]
    img.size = [size_x, size_y]   #scale image
    img.draw()
    win.flip()
    PhotoOnset = Exp_cl.getTime()
    psychopy.core.wait(imageDur)
    
    #ISI 
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(jitter3[i])
    
    #---collect response----        
    X[i+20,0] = subj_id;
    X[i+20,1] = i+1; #trial number
    if this_trial is 'Neutral':
        X[i+20,2] = get_num(neu_list[0][neu_counter]);
    elif this_trial is 'Negative':
        X[i+20,2] = get_num(neg_list[0][neg_counter]);
    X[i+20,3] = PhotoOnset; #Time photo was presented in overall exp timeline
    X[i+20,4] = myRatingScale.getRating()
    
    # Okay end of loop, incrementing counter
    neu_counter = neu_counter+1
    neg_counter = neg_counter+1
    
    
   
    
Cue_img.draw()
win.flip()
psychopy.core.wait(2)   
Cue_offset = Exp_cl.getTime()


# collect cue timing out of block
Xcue[blocknum,0]=Cue_onset;
Xcue[blocknum,1]=Cue_offset;

#Interblock rest
fixation_text.draw()
win.flip()
psychopy.core.wait(20)

#
#----Save data----
np.savetxt(
    data_path,
    X,
    delimiter=",",
    fmt='%.2f',
    header="Subject ID, Trial#, Stim_ID, Photo_Onset, Response"
)

np.savetxt(
    data_path2,
    Xcue,
    delimiter=",",
    fmt='%.0i',
    header="Cue_onset, Cue_offset"
)
#---end run----
finish_text.draw()
win.flip()
print Exp_cl.getTime()
psychopy.event.waitKeys()