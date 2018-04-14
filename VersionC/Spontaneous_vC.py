#opened 12/12/16
#SERP fMRI
#Spontaneous Script Version C
#---------------------------------------------------------
#Experiment description: 3 blocks of 10 pictures each. No cue for what 
#participant should use on the block of pictures. No response needed
#Version 3(C) of 3.
#---------------------------------------------------------
import os
import serial
import sys
import numpy as np
import psychopy.gui
import psychopy.visual
import psychopy.event
import psychopy.core
from psychopy import data, logging, sound
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
#
#----Create file path for experiment timing data----
data_path = "Sponteneous_vC_"+str(subj_id)+".csv";
while os.path.exists(data_path): #if path exists, rename it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subj_id = subj_id+"000"
    data_path = "Spontenous_vC_"+str(subj_id)+".csv"
#
#----Configuration for USB serial input for scanner trigger
serial_settings = {
    'mount': '/dev/tty.USA19H141P1.1',   # May need to change per computer
    'baud': 115200,
    'timeout': .0001
}
fmri_settings = {
    'sync': '5',         # character to use as the sync timing event
}
#
ser = serial.Serial(
    serial_settings['mount'],
    serial_settings['baud'],
    timeout = serial_settings['timeout']
)

#
#----Declare experiment variables
num_stim = 30
num_reps = 10
num_vars = 5 #variables: subj_ID, trial#, photoID, Photo Onset, Cue Onset
PhotoStim_List = ["7004.jpg", "7009.jpg", "7010.jpg", "7179.jpg", "2493.jpg", "7050.jpg", "7045.jpg", "7705.jpg", "7950.jpg", "2345.1.jpg", "6415.jpg", "6231.jpg", "6560.jpg", "3195.jpg", "9903.jpg", "6540.jpg", "2352.2.jpg", "9253.jpg", "6263.jpg", "3301.jpg", "9410.jpg", "3030.jpg", "3140.jpg", "3060.jpg", "9412.jpg", "3130.jpg", "2703.jpg", "3101.jpg", "3110.jpg", "3063.jpg"];
shuffle(PhotoStim_List);#randomize trial order
#break randomized photo stim into 3 groups of 10
PhotoBlock1 = PhotoStim_List[0:10];
PhotoBlock2 = PhotoStim_List[10:20];
PhotoBlock3 = PhotoStim_List[20:]

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
#
#
#----Declare image and text variables
welcome_text = psychopy.visual.TextStim(
    win=win,
    text="Waiting for scanner...",
    color=[1, 1, 1],
    height=35
)
#
intro_text = psychopy.visual.TextStim(
    win = win,
    text= "The task will now begin",
    color=[1,1,1],
    height=35
)
#
fixation_text = psychopy.visual.TextStim(
    win=win,
    text="+",
    color=[1,1,1],
    height=35
)
#
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

#----Set up opening of exp. with fMRI trigger-------
#---------------------------------------------------------
#welcome_text.draw()
#win.flip()
#psychopy.event.waitKeys()
#

ser.flushInput()
trigger = ''
while trigger != fmri_settings['sync']:
    welcome_text.draw()
    win.flip()
    trigger = ser.read()
ser.close()
#
#---------------------------------------------------------
#----Begin experiment blocks------------------------------
#---------------------------------------------------------
#Set Exp clock to 0 at beginning of experiment
Exp_cl.reset(0)

#let subject know experiment is about to begin
intro_text.draw()
win.flip()
psychopy.core.wait(2)

#fixation
fixation_text.draw()
win.flip()
psychopy.core.wait(20)
#
#
Cue_img.draw()
Cue_onset = Exp_cl.getTime()
win.flip()
psychopy.core.wait(2)
#
#----------------------------
#----------BLOCK 1-----------
#----------------------------
assert len(PhotoBlock1) == len(jitter1) #Make sure both presentation groupings are equal

for i in range(0, num_reps):
    filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ PhotoBlock1[i]
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
    psychopy.core.wait(7)
    
    #ISI
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(jitter1[i])
    
    
#---collect response----
    
    X[i,0] = subj_id;
    X[i,1] = i+1; #trial number
    X[i,2] = get_num(PhotoBlock1[i]);
    X[i,3] = PhotoOnset; #Time photo was presented in overall exp timeline
    X[i,4] = Cue_onset;

Cue_img.draw()
win.flip()
psychopy.core.wait(2)

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
#----------BLOCK 2-----------
#----------------------------
assert len(PhotoBlock2) == len(jitter2) 

for i in range(0,num_reps):
    filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ PhotoBlock2[i]
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
    psychopy.core.wait(7)
    
    #ISI
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(jitter2[i])
    
    #---collect response----
    X[i+10,0] = subj_id;
    X[i+10,1] = i+11; #trial number
    X[i+10,2] = get_num(PhotoBlock2[i]);
    X[i+10,3] = PhotoOnset; #Time photo was presented in overall exp timeline
    X[i+10,4] = Cue_onset;

Cue_img.draw()
win.flip()
psychopy.core.wait(2)

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
assert len(PhotoBlock3) == len(jitter3)

for i in range(0,num_reps):
    filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ PhotoBlock3[i]
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
    psychopy.core.wait(7)
    
    #ISI 
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(jitter3[i])
    
    #---collect response----
    X[i+20,0] = subj_id;
    X[i+20,1] = i+21; #trial number
    X[i+20,2] = get_num(PhotoBlock3[i]);
    X[i+20,3] = PhotoOnset;
    X[i+20,4] = Cue_onset;
    
Cue_img.draw()
win.flip()
psychopy.core.wait(2)

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
    fmt='%.0i',
    header="Subject ID, Trial#, Stim ID, Photo Onset, Cue Onset"
)
#---end run----
finish_text.draw()
win.flip()
print Exp_cl.getTime()
psychopy.event.waitKeys()