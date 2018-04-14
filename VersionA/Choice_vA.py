#opened 12/7/16
#SERP fMRI 
#Choice Version A
#---------------------------------------------------------
#Experiment description: 1 block of 60 pictures (30 from the spontaneous trial, 30 novel photos). 
#Participants view pictures then answer 2 questions after each picture: one on Affect
#and one on which version of regulation (if any) they chose to use.
#Version 1(A) of 3.
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
data_path = "Choice_vA_"+str(subj_id)+".csv";
while os.path.exists(data_path): #if path exists, rename it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subj_id = subj_id+"000"
    data_path = "Choice_vA_"+str(subj_id)+".csv"
#
#----Declare experiment variables
#
num_vars = 5; #variables: subj_ID, trial#, photoID, Affect_Resp, Tech_Resp
num_stim = 60;
num_reps = 60;
PhotoStim_List = ["7012.jpg", "7032.jpg", "7705.jpg", "7056.jpg", "7002.jpg", "7950.jpg", "7010.jpg", "7009.jpg", "7050.jpg", "2053.jpg", "6263.jpg", "9421.jpg", "3195.jpg", "3500.jpg", "3181.jpg", "3051.jpg", "3017.jpg", "9322.jpg", "6212.jpg", "2095.jpg", "9183.jpg", "2703.jpg", "9252.jpg", "3015.jpg", "3001.jpg", "9185.jpg", "9075.jpg", "3000.jpg", "6520.jpg", "3170.jpg", "9910.jpg", "2375.1.jpg", "9428.jpg", "6243.jpg", "9220.jpg", "9184.jpg", "3220.jpg", "9800.jpg", "6231.jpg", "9253.jpg", "2352.2.jpg", "9600.jpg", "9902.jpg", "6315.jpg", "3110.jpg", "3101.jpg", "6563.jpg", "2800.jpg", "3059.jpg", "2205.jpg", "3301.jpg", "9635.1.jpg", "3266.jpg", "3060.jpg", "3030.jpg", "3010.jpg", "3140.jpg", "3068.jpg", "3063.jpg", "3064.jpg"];
shuffle(PhotoStim_List);#randomize trial order
X=np.zeros((num_stim,num_vars));   #Create blank vector to store responses
#
#-----------------------------
#----Open experiment window----
#-----------------------------
win = psychopy.visual.Window(
    size=[1280, 800],
    units="pix",
    fullscr=False,
    color=[-1, -1, -1]
)
#For Affect Question
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
#For Technique Question
myRatingScale2 = visual.RatingScale(
    win, 
    choices=map(str, range(1,5)),
    low=1, high=4, 
    precision=1, 
    markerStart=1.5, 
    size=1.5, 
    showAccept=True, 
    leftKeys="1", rightKeys="2", 
    noMouse=False
)

#
#
#----Declare image and text variables
welcome_text = psychopy.visual.TextStim(
    win=win,
    text="Welcome. Press any key to start the experiment...",
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
myItem2 = visual.TextStim(
    win=win, 
    text="What did you do to deal with the image you just saw?\n\n1=Reframed it to be more positive\n2=Reframed it to be less negative\n3=Thought about something else\n4=Other", 
    wrapWidth=1000, 
    height=30,
    color=[1, 1, 1]
)

#
finish_text = psychopy.visual.TextStim(
    win=win,
    text="Please wait...",
    color=[1, 1, 1],
    height=35,
    wrapWidth=1000
)
#----Set up opening of exp. with fMRI trigger-------
#---------------------------------------------------------
welcome_text.draw()
win.flip()
psychopy.event.waitKeys()

#---------------------------------------------------------
#----Begin experiment blocks------------------------------
#---------------------------------------------------------
#let subject know experiment is about to begin
intro_text.draw()
win.flip()
psychopy.core.wait(2)

#fixation
fixation_text.draw()
win.flip()
psychopy.core.wait(2)
#
#
#----------------------------
#----------BLOCK 1-----------
#----------------------------
    
for i in range(0, num_reps):
    filename ="/Users/whalenlab/Desktop/Experiments/SERP/IAPS/"+ PhotoStim_List[i]
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
    psychopy.core.wait(7)
    
    #ISI pre
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(2)
    
    #collect response for Affect Question
    myRatingScale.reset()
    while myRatingScale.noResponse:  # show & update until a response has been made
        myItem.draw()
        myRatingScale.draw()
        win.flip()
    
    Affect_Resp = myRatingScale.getRating()
    print 'rating =', myRatingScale.getRating()
    print 'history', myRatingScale.getHistory()
    
    
    #Collect response for Technique Question
    myRatingScale2.reset()
    while myRatingScale2.noResponse:
        myItem2.draw()
        myRatingScale2.draw()
        win.flip()
    
    Tech_Resp = myRatingScale2.getRating()
    print 'technique rating =', myRatingScale2.getRating()
    print 'Technique history=', myRatingScale2.getHistory()
    
    
#---collect response within Matrix X----
    X[i,0] = subj_id;
    X[i,1] = i+1; #trial number
    X[i,2] = get_num(PhotoStim_List[i]);
    X[i,3] = Affect_Resp;
    X[i,4] = Tech_Resp;
    
    #ISI
    fixation_text.draw()
    win.flip()
    psychopy.core.wait(2) 
    
#Interblock rest
fixation_text.draw()
win.flip()
psychopy.core.wait(5)
#
#
#
#----Save data----
np.savetxt(
    data_path,
    X,
    delimiter=",",
    fmt='%.0i',
    header="Subject ID, Trial#, Stim ID, Affect_Resp, Tech_Resp"
)
#---end run----
finish_text.draw()
win.flip()
psychopy.event.waitKeys()