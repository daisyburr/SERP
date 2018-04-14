#opened 12/12/16
#SERP fMRI
#Run 2 Version A
#---------------------------------------------------------
#Experiment description: 3 blocks of 15 pictures each. Cue before each block 
#denoting which form of regulation (Positive reappraisal, negative reappraisal, 
#or Distraction) to use on the block of pictures. Version 1(A) of 3.
#---------------------------------------------------------
from __future__ import division
import os
import serial
import sys
import numpy as np
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
#
#----Create file path for experiment timing data----
data_path = "InstrRun2vA_"+str(subj_id)+".csv";
while os.path.exists(data_path): #if path exists, rename it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subj_id = subj_id+"000"
    data_path = "InstrRun2vA_"+str(subj_id)+".csv"
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

#----Declare experiment variables
#
num_vars = 8; #variables: subj_ID, trial#, photoID, response, R_History, Photo Onset, Question Onset
num_stim = 30;
num_reps = 10;
PhotoStim_List = ["7020.jpg", "2411.jpg", "2493.jpg", "2002.jpg", "7235.jpg", "7000.jpg", "7179.jpg", "7161.jpg", "7247.jpg", "9908.jpg", "3103.jpg", "6540.jpg", "3550.1.jpg", "2345.1.jpg", "6415.jpg", "9903.jpg", "9414.jpg", "6312.jpg", "3150.jpg", "3350.jpg", "6313.jpg", "3131.jpg", "9413.jpg", "9187.jpg", "3530.jpg", "9433.jpg", "3005.1.jpg", "9412.jpg", "3071.jpg", "3080.jpg"];
shuffle(PhotoStim_List);#randomize trial order
#break randomized photo stim into 3 groups of 10
PhotoBlock1 = PhotoStim_List[0:10];
PhotoBlock2 = PhotoStim_List[10:20];
PhotoBlock3 = PhotoStim_List[20:]
QuesStim_List = ["PositiveReapp1.jpg", "NegativeReapp2.jpg", "Distance3.jpg"];


#IF YOU WANT FIXED RANDOM NUMBERS (I.E., ACROSS SUBJECTS)
#SET THE RANDOM NUMBER GENERATOR SEED (1, 2, 3) FOR THE THREE BLOCKS
#create 3 groups of 20 random ISIs between 2 and 6 within a uniform 
#distribution that all add up to 80 seconds (total time of ISIs in 1 block)
Block1Seed = np.random.seed(1)
jitter1 = np.random.uniform(low=2, high=6, size=20);
jitter1 = jitter1 / np.sum(jitter1) * 80

PreISI_bl1 = jitter1[::2] #make sure rundown of Pre jitters per trial skip every other so as not to repeat post-Jitters
PostISI_bl1 = jitter1[1::2] #make sure Post jitters per trial start at the second number and then skip every other
#
Block2Seed = np.random.seed(2)
jitter2 = np.random.uniform(low=2, high=6, size=20);
jitter2 = jitter2 / np.sum(jitter2) * 80

PreISI_bl2 = jitter2[::2]
PostISI_bl2 = jitter2[1::2]
#
Block3Seed = np.random.seed(3)
jitter3 = np.random.uniform(low=2, high=6, size=20);
jitter3 = jitter3 / np.sum(jitter3) * 80

PreISI_bl3 = jitter3[::2]
PostISI_bl3 = jitter3[1::2]

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
myRatingScale = visual.RatingScale(
    win=win, 
    choices=map(str, range(-4, 5)), 
    low=-4, high=4, 
    precision=1, 
    labels=('Negative', 'Positive'), 
    markerStart=4, 
    size=1.5, 
    showAccept=False, 
    leftKeys="1", rightKeys="2", 
    maxTime=4, 
    noMouse=True
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
PosReap_text = psychopy.visual.TextStim(
    win=win,
    text="Reframe these images to be more positive",
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
#
NegReap_text = psychopy.visual.TextStim(
    win=win,
    text="Reframe these images to be less negative",
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
#
Dist_text = psychopy.visual.TextStim(
    win=win,
    text="Think about something else",
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
#
myItem = psychopy.visual.TextStim(
    win=win,
    text="How negative or positive do you feel?",
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000,
    alignHoriz='center'
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
ser = serial.Serial(
    serial_settings['mount'],
    serial_settings['baud'],
    timeout = serial_settings['timeout']
)
ser.flushInput()
trigger = ''
while trigger != fmri_settings['sync']:
    welcome_text.draw()
    win.flip()
    trigger = ser.read()

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
#----------------------------
#----------BLOCK 1-----------
#----------------------------
assert len(PhotoBlock1) == len(PreISI_bl1) == len(PostISI_bl1) #Make sure all 3 presentation groupings are equal

filename = "/Users/whalenlab/Desktop/Experiments/SERP/QuestStim/" + QuesStim_List[0]
img = psychopy.visual.ImageStim(
        win=win,
        image=filename,
        units="pix"
    )
size_x = img.size[0]
size_y = img.size[1]
img.size = [size_x*.5, size_y*.5]   #scale image
img.draw()
win.flip()
psychopy.core.wait(2)

for i in range(0, num_reps):

    filename ="/Users/Whalenlab/Desktop/Experiments/SERP/IAPS/"+ PhotoBlock1[i]
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
    
    #ISI pre
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(PreISI_bl1[i])
    
    #need to collect response--
    myRatingScale.reset()
    while myRatingScale.noResponse:  # show & update until a response has been made
        myItem.draw()
        key = ser.read()
        psychopy.event._onPygletKey(symbol=key, modifiers=None, emulated=True)
        myRatingScale.draw()
        win.flip()
    
    Response_History = len(myRatingScale.getHistory())
    Response = myRatingScale.getRating()
    print 'Example 1: rating =', myRatingScale.getRating()
    print 'response time=', myRatingScale.getRT()
    print 'history', myRatingScale.getHistory()
    QuesOnset = Exp_cl.getTime()
    
    
#---collect response----
    X[i,0] = subj_id;
    X[i,1] = i+1; #trial number
    X[i,2] = get_num(QuesStim_List[0]);
    X[i,3] = get_num(PhotoBlock1[i]);
    X[i,4] = Response;
    X[i,5] = Response_History; #buttons pressed, if any
    X[i,6] = PhotoOnset; #Time photo was presented in overall exp timeline
    X[i,7] = QuesOnset; #Time question was presented in overall exp timeline
    
    #ISI
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(PostISI_bl1[i]) #ADJUST THIS PER BLOCK NUMBER
    
Cue_img.draw()
win.flip()
psychopy.core.wait(2)

#Interblock rest
fixation_text.draw()
win.flip()
psychopy.core.wait(20)
#
#
#----------------------------
#----------BLOCK 2-----------
#----------------------------
assert len(PhotoBlock2) == len(PreISI_bl2) == len(PostISI_bl2) 

filename = "/Users/whalenlab/Desktop/Experiments/SERP/QuestStim/" +QuesStim_List[1]
img = psychopy.visual.ImageStim(
        win=win,
        image=filename,
        units="pix"
    )
size_x = img.size[0]
size_y = img.size[1]
img.size = [size_x*.5, size_y*.5] 
img.draw()
win.flip()
psychopy.core.wait(2)

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
    
    #ISI pre question
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(PreISI_bl2[i])
    
    #need to collect response--HOW TO DO THIS WITH A SLIDING SCALE ON BUTTON BOXES!!!!!
    myRatingScale.reset()
    while myRatingScale.noResponse:  # show & update until a response has been made
        myItem.draw()
        key = ser.read()
        psychopy.event._onPygletKey(symbol=key, modifiers=None, emulated=True)
        myRatingScale.draw()
        win.flip()
    
    Response_History = len(myRatingScale.getHistory())
    Response = myRatingScale.getRating()
    print 'Example 1: rating =', myRatingScale.getRating()
    print 'response time=', myRatingScale.getRT()
    print 'history', myRatingScale.getHistory()
    QuesOnset = Exp_cl.getTime()
    
    
#---collect response----
    X[i+10,0] = subj_id;
    X[i+10,1] = i+11; #trial number
    X[i+10,2] = get_num(QuesStim_List[1]); 
    X[i+10,3] = get_num(PhotoBlock1[i]);
    X[i+10,4] = Response;
    X[i+10,5] = Response_History;#how to export keys from button box to "," file?
    X[i+10,6] = PhotoOnset; #Time photo was presented in overall exp timeline
    X[i+10,7] = QuesOnset; #Time question was presented in overall exp timeline
    

    
    #ISI post question
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(PostISI_bl2[i])
    

Cue_img.draw()
win.flip()
psychopy.core.wait(2)

#Interblock rest
fixation_text.draw()
win.flip()
psychopy.core.wait(20)
#
#
#----------------------------
#----------BLOCK 3-----------
#----------------------------
assert len(PhotoBlock3) == len(PreISI_bl3) == len(PostISI_bl3)

filename = "/Users/whalenlab/Desktop/Experiments/SERP/QuestStim/" + QuesStim_List[2]
img = psychopy.visual.ImageStim(
        win=win,
        image=filename,
        units="pix"
    )
size_x = img.size[0]
size_y = img.size[1]
img.size = [size_x*.5, size_y*.5] 
img.draw()
win.flip()
psychopy.core.wait(2)


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
    
    #ISI pre question
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(PreISI_bl3[i])
    
#need to collect response--HOW TO DO THIS WITH A SLIDING SCALE ON BUTTON BOXES!!!!!
    myRatingScale.reset()
    while myRatingScale.noResponse:  # show & update until a response has been made
        myItem.draw()
        key = ser.read()
        psychopy.event._onPygletKey(symbol=key, modifiers=None, emulated=True)
        myRatingScale.draw()
        win.flip()
    
    Response_History = len(myRatingScale.getHistory())
    Response = myRatingScale.getRating()
    print 'Example 1: rating =', myRatingScale.getRating()
    print 'response time=', myRatingScale.getRT()
    print 'history', myRatingScale.getHistory()
    QuesOnset = Exp_cl.getTime()
    
    
#---collect response----
    X[i+20,0] = subj_id;
    X[i+20,1] = i+21; #trial number
    X[i+20,2] = get_num(QuesStim_List[2]); 
    X[i+20,3] = get_num(PhotoBlock1[i]);
    X[i+20,4] = Response;
    X[i+20,5] = Response_History;#how to export keys from button box to "," file?
    X[i+20,6] = PhotoOnset; #Time photo was presented in overall exp timeline
    X[i+20,7] = QuesOnset; #Time question was presented in overall exp timeline
    
    
    #ISI
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(PostISI_bl3[i])

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
    header="Subject ID, Trial#, Ques ID, Stim ID, Response, R_History, Photo Onset, Ques Onset"
)
#---end run----
finish_text.draw()
win.flip()
print Exp_cl.getTime()
psychopy.event.waitKeys()