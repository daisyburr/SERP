#visual display
import psychopy.visual
# actions manipulating display
import psychopy.event
#gui is for saving data, apprebiation for graphic user interface, to attach the experiment to the file
import psychopy.gui
import os
import sys
import numpy as np
from random import randint
from random import shuffle
import psychopy.core

def get_num(x):
    return int(''.join(ele for ele in x if ele.isdigit()))


#subject ID
gui=psychopy.gui.Dlg()
gui.addField("Subject ID: ")
gui.show()
subj_id=gui.data[0]

data_path="SERPresponses_part2_"+str(subj_id)+".csv";
while os.path.exists(data_path): #if path exists, remame it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subj_id = subj.id+"000"
    data_path = "SERPresponses_part2_"+str(subj_id)+".csv"

#defining experimental variables
n_trials=20; # number of trials"
n_vars=9; # sub_id; Trial#; Picture ID, Response1, response2, response3, quescode1, quescode2,  quescode3
trial_list=["2053.jpg", "2205.jpg", "2301.jpg", "2345.1.jpg", "2455.jpg", "2457.jpg", "2703.jpg", "2750.jpg", "2751.jpg", "2900.1.jpg", "3181.jpg", "3350.jpg", "9220.jpg", "9429.jpg", "9530.jpg", "9584.jpg", "9900.jpg", "9921.jpg", "9926.jpg", "1201.jpg"];
np.random.shuffle(trial_list); #randomize order of images
n_ques_trials=3; #number of question trials
post_questions=["positive1.jpg", "negative2.jpg", "arousal3.jpg"];
X=np.zeros((n_trials, n_vars))


#welcome window
win=psychopy.visual.Window(
    size=[1280, 800],
    units="pix",
    fullscr=False, #true false alwyays caps
    color=[-1, -1, -1]
)
    
#welcome text
welcome_text="The second part of the experiment will now begin.\n\nPress any key to continue."
text=psychopy.visual.TextStim(
    win=win,
    alignHoriz='center',
    text=welcome_text,
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
text.draw()
win.flip()
psychopy.event.waitKeys()



#instruction page
instruction_text="You will see the same series of negative images. After each image, you will be asked some questions about how you feel.\n\nPress any key to start."
text=psychopy.visual.TextStim(
    win=win,
    text=instruction_text,
    color=[1, 1, 1],
    alignHoriz='center',
    height=40,
    wrapWidth=1200
)
text.draw()
win.flip()
psychopy.event.waitKeys()

# trials

for i in range(0, n_trials): 
    filename="Pilotimages/"+trial_list[i]
    print filename
    img=psychopy.visual.ImageStim(
        win=win, 
        image=filename,
        units="pix")
    size_x=img.size[0]
    size_y=img.size[1]
    img.size=[size_x, size_y] #scaling size of image
    img.draw()
    
    
    win.flip()
    psychopy.core.wait(7)
    print X
    np.random.shuffle(post_questions)
    
    #Nested for loop for post-jpg questions
    for j in range(0,n_ques_trials):
        question_placement = 350
        filename="SERP Post questions/" + post_questions[j]
        img=psychopy.visual.ImageStim(
            win=win,
            image=filename,
            units="pix")
        size_x = img.size[0]
        size_y = img.size [1]
        img.size = [size_x * 1.5, size_y * 1.5]
        img.draw()
        text1="1        2        3        4        5        6        7";
        text2="not at all                                          very strongly";
        text_line1=psychopy.visual.TextStim(
            win=win,
            text=text1,
            color=[1, 1, 1],
            pos=(0,-question_placement+100),
            alignHoriz='center',
            height=40,
            wrapWidth=1200)
        text_line1.draw()
        text_line2=psychopy.visual.TextStim(
            win=win,
            text=text2,
            color=[1, 1, 1],
            pos=(0, -question_placement+50),
            alignHoriz='center',
            height=40,
            wrapWidth=1200)
        text_line2.draw()
        #display to subject
        win.flip()
        #collect response
        keys = psychopy.event.waitKeys(keyList=["1", "2", "3", "4", "5", "6", "7"])
        X[i,j+3] = keys[0];
        X[i,j+6] = get_num(post_questions[j])
        
        
        text3="+"
        text_line3=psychopy.visual.TextStim(
            win=win,
            text=text3,
            color=[1, 1, 1],
            alignHoriz='center',
            height=40,
            wrapWidth=1200)
        text_line3.draw()
        win.flip()
        psychopy.core.wait(1)
       
    X[i,0] = subj_id;
    X[i,1] = i+1;
    X[i,2] = get_num(trial_list[i]);
    print X[i]
    

#save data to file
np.savetxt(
    data_path,
    X,
    delimiter=",",
    header="sub_id, Trial#, Picture ID, R1, R2, R3, QC1, QC2, QC3"
)
    
    
    
#goodbyetext
goodbye_text="Please let the experimenter know that you are done with this portion of the experiment."
text=psychopy.visual.TextStim(
    win=win,
    alignHoriz='center',
    text=goodbye_text,
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
text.draw()
win.flip()
psychopy.event.waitKeys()
    