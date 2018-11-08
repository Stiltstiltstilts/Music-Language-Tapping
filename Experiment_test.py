#!/Users/Stilts/PsychoPyBuild/bin/python

################################################
################# Imports ######################
################################################
from psychopy import core, visual, logging, gui, event, prefs, data
import pyo
prefs.general['audioLib'] = ['pyo']
prefs.general['audioDevice'] = ['Built-in Output']
from psychopy import sound
from numpy.random import random, randint, normal, shuffle
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os
import sys
#import itertools
import numpy as np
from constants import *

GlobalClock = core.Clock()  # Track time since experiment starts

################################################
############### Basic checks ###################
################################################
# check relative paths correct
_thisDir = os.path.abspath(os.path.dirname(__file__))
os.chdir(_thisDir)

################################################
####### Collect experiment session info ########
################################################
# Exp name
expName = 'MeterSyntax'
# Define experiment info
expInfo = {'session':'001', 'participant':'001',
    'handedness':'', 'gender':'', 'native language': '', 'age': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName,)
if dlg.OK == False:
    core.quit()  # user pressed cancele
expInfo['date'] = data.getDateStr()

# Create filename for data file (absolute path + name)
filename = _thisDir + os.sep + 'data/{0}'.format(expInfo['participant'])

with open('data/{}participant_info.txt'.format(expInfo['participant']), 'w') as log_file:
    log_file.write('Session\t' +
                    'Participant\t' +
                    'Handedness\t' +
                    'Gender\t' +
                    'Native_language\t' +
                    'Age\t' + '\n')
 
    log_file.write('\t'.join([str(expInfo['session']),
                            str(expInfo['participant']),
                            str(expInfo['handedness']),
                            str(expInfo['gender']),
                            str(expInfo['native language']),
                            str(expInfo['age'])]) + '\n')
    log_file.flush()


################################################
################ Setup logfile #################
################################################
# save a log file for detailed verbose info
logFile = logging.LogFile(filename+'.log', level=logging.DATA)
# this outputs to the screen, not a file
logging.console.setLevel(logging.WARNING)

################################################
################# Variables ####################
################################################
####====Auditory Stimuli====####
binary_beat = sound.Sound('Stimuli/Tones/binary_beat.wav', secs=-1)
binary_beat.setVolume(1)
ternary_beat = sound.Sound('Stimuli/Tones/ternary_beat.wav', secs=-1)
ternary_beat.setVolume(1)

# setup window
win = visual.Window(fullscr=True,
                monitor='Laptop',  
                units='deg',
                allowGUI=False)

trialClock = core.Clock()

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess 60Hz

################################################
########## Trial list construction #############
################################################
############ main sentences ############
assert len(sub_cong) == len(obj_cong), "number of sentences not the same" # check that number of sentences between conditions match. Incong conditions generated from same source hence not needed here.
main_conditions = [sub_cong, sub_incong, obj_cong, obj_incong,]  
nSentences = len(sub_cong) 
main_sentence_chunk_size = int(nSentences / len(main_conditions)) # how many sentences per condition
main_condition_index = list(range(len(main_conditions))) * main_sentence_chunk_size # list nSentences long of condition indicies
shuffle(main_condition_index)  # randomise 
main_condition_list = [ (main_conditions[main_condition_index[i]][i]) for i in range(nSentences) ] #create list of trial dictionaries (without probes) in original order

############ main probes + combine with main trials ############
assert len(probe_mc_neg) == len(probe_mc_pos) == len(probe_rc_subneg_objpos) == len(probe_rc_subpos_objneg), "number of probes not the same"
main_probes = [probe_mc_pos, probe_mc_neg,
               probe_rc_subpos_objneg, probe_rc_subneg_objpos,]
for main_cond in range(len(main_conditions)):   # iterate through main conditions
    probe_list = list(range(len(main_probes))) * int((nSentences / len(main_probes)) / len(main_conditions))  
    shuffle(probe_list)
    probe_counter = 0
    for sent_index in range(len(main_condition_list)):
        if main_condition_index[sent_index] == main_cond:
            main_condition_list[sent_index] = {**main_condition_list[sent_index], **main_probes[probe_list[probe_counter]] [main_condition_list[sent_index]['sent_number']]} 
            probe_counter += 1

trial_list = []  # initialising

############ Assorted sentences ############
assorted_condition_list = [ (i, assorted[i]) for i in range(len(assorted)) ] 

############ Assorted probes ############
assorted_probes = [probe_ass_neg, probe_ass_pos]
n_ass_probes = len(probe_ass_neg)
assorted_probe_chunk_size = int(n_ass_probes / len(assorted_probes))
assorted_probe_index = list(range(len(assorted_probes))) * assorted_probe_chunk_size
shuffle(assorted_probe_index)
assorted_probe_list = [ (i,assorted_probes[assorted_probe_index[i]][i]) for i in range(len(assorted)) ] 

############ Combining stuff ############
assorted_trials = [ {**assorted_condition_list[i][1], **assorted_probe_list[i][1]} for i in range(len(assorted_condition_list)) ]
all_trials = main_condition_list
all_trials.extend(assorted_trials)
all_trials = data.TrialHandler(trialList = all_trials[:2], nReps = 1, method = 'random', extraInfo = expInfo, name = 'all_trials') 
thisTrial = all_trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

############ Practice trials ############
prac_list = [ {**prac[i], **prac_probes[i]} for i in range(len(prac)) ]
for trial in range(len(prac)):
    if trial <= 1:
        prac_list[trial]['beat_type'] = 'binary'
    else:
        prac_list[trial]['beat_type'] = 'ternary'
prac_list = data.TrialHandler(trialList = prac_list[:], nReps = 1, method = 'sequential', extraInfo = expInfo, name = 'practice_trials')
thisPracTrial = prac_list.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisPracTrial != None:
    for paramName in thisPracTrial:
        exec('{} = thisPracTrial[paramName]'.format(paramName))


################################################
############## Run experiment ##################
################################################
try: 
    # ==== SETUP TRIAL OBJECTS ==== #
    message1 = visual.TextStim(win, pos=[0,+3], color=FGC, alignHoriz='center', name='topMsg', text="placeholder") 
    message2 = visual.TextStim(win, pos=[0,-3], color=FGC, alignHoriz='center', name='bottomMsg', text="placeholder") 
    fixation = visual.TextStim(win,  pos=[0,0], color=FGC, alignHoriz='center', text="+")
    endMessage = visual.TextStim(win,  pos=[0,0], color=FGC, alignHoriz='center', text="The end! Thank you for participating :)")
    space_cont = visual.TextStim(win, pos=[0,0], color=FGC, text="Press space to continue")
    too_slow = visual.TextStim(win, pos=[0,0], color=FGC, text="Too slow: respond quicker next time")
    feedback = visual.TextStim(win, pos=[0,0], color=FGC, text="placeholder")
    introText = visual.TextStim(win, pos=[0,0], color=FGC, text="Placeholder")
    word_stim_list = []
    for i in range(15): # setting up text_stimuli objects... 15 is the most words in the sent_stims
            exec( '{} = visual.TextStim(win, pos=[0,0], color=FGC, text="placeholder")'.format('word' + '_' + str(i+1)) ) # create text objects
            exec( 'word_stim_list.extend([{}])'.format(str('word' + '_' + str(i+1))) ) # putting them in word_stim_list
    probe_text = visual.TextStim(win, pos=[0,0], color=FGC, alignHoriz='center', name='top_probe', text="placeholder")
    GSI = visual.RatingScale(win, name='GSI', marker='triangle',
                             textSize = 0.4, showValue = False, acceptText = 'confirm',
                              size=1.5, pos=[0.0, -0.4], 
                              choices=['Completely\n Disagree', 'Strongly\n Disagree',
                                         'Disagree', 'Neither Agree\n or Disagree', 'Agree',
                                          'Strongly\n Agree', 'Completely\n Agree'],
                             tickHeight=-1)
    response_keys = visual.TextStim(win, pos=[0,-5], height = .5, color=FGC, text="respond:'y' 'n' or 'd'")
    # ==== OTHER TRIAL VARIABLES ==== #
    clock = core.Clock()
    trial_num = 0

    ################################################
    ############## START EXPERIMENT ################
    ################################################
    
    # ===== INSTRUCTIONS 1 ====== #
    counter = 0
    while counter < len(part1Intro):
        # === set top text === #
        message1.setText(part1Intro[counter]) 
        # === set bottom text === #
        if counter == 0:
            message2.setText(bottom_text[0])
        elif counter in range(1, (len(part1Intro) - 1)):
            message2.setText(bottom_text[1])
        else: 
            message2.setText(bottom_text[2])
        # === display instructions and wait === #
        message1.draw()
        message2.draw() 
        win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(counter+1))
        win.flip()
        # === check for a keypress === #
        thisKey = event.waitKeys()
        if thisKey[0] in ['q','escape']:
            core.quit()
        elif thisKey[0] == 'backspace' and counter > 0:
            counter -= 1
        else:
            counter += 1

    for thisPracTrial in prac_list:  
        trial_num += 1
        ####====ABBREVIATE PARAMETER NAMES====####
        if thisPracTrial != None:
            for paramName in thisPracTrial:
                exec('{} = thisPracTrial[paramName]'.format(paramName))
        
        probe_resp = event.BuilderKeyResponse()

        ####====SETUP TRIAL COMPONENTS LIST====####
        # initialize trial components list
        trialComponents = []
        # add auditory stimuli component
        if beat_type == 'binary':
            beat_stim = binary_beat
            word_offset = 7 * beat_freq
        elif beat_type == 'ternary':
            beat_stim = ternary_beat
            word_offset = 8 * beat_freq
        trialComponents.extend([beat_stim]) # add beat stim to trialComponents list
        # add text stimuli components
        for i in range(len(sent_stim)): # for i in range(len(trial['sent_stim'])):
            exec('trialComponents.extend([{}])'.format('word' + '_' + str(i+1)))
            word_stim_list[i].setText(sent_stim[i])
        
        # set probe text for the trial
        probe_text.setText(probe)

        ####====BASIC ROUTINE CHECKS====####
        continueRoutine = True
        # keep track of which components have finished
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        t = 0
        trialClock.reset()  # clock
        frameN = -1
        beatDuration = len(sent_stim)*beat_freq + word_offset

        ####====START PRACTISE TRIAL ROUTINE====####
        while continueRoutine: 
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
            ##### 1. start/stop beat_stim  #####
            if t >= 0.0 + sound_delay and beat_stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                beat_stim.tStart = t
                beat_stim.frameNStart = frameN  # exact frame index
                beat_stim.play()  # start the sound (it finishes automatically)
                fixation.setAutoDraw(True)
            if beat_stim.status == STARTED and t >= beatDuration:
                beat_stim.stop()

            ##### 2.  iterate through sentence text stimuli #####   
            for word_index in range(len(sent_stim)):
                if t >= word_index * beat_freq + word_offset and word_stim_list[word_index].status == NOT_STARTED:
                    fixation.setAutoDraw(False)
                    # keep track of start time/frame for later
                    word_stim_list[word_index].tStart = t
                    word_stim_list[word_index].frameNStart = frameN  # exact frame index
                    word_stim_list[word_index].setAutoDraw(True)
                frameRemains = (beat_freq * word_index) + beat_freq + word_offset - win.monitorFramePeriod * 0.75  # most of one frame period left
                if word_stim_list[word_index].status == STARTED and t >= frameRemains:
                    word_stim_list[word_index].setAutoDraw(False)

            ##### 3.  check if all components have finished #####
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            ##### 4.  refresh the screen #####
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        ####====Ending Trial Routine====####
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        beat_stim.stop()  # ensure sound has stopped at end of routine

        ####====Probe====####
        # 3.  display probe text e.g. "The boy helped the girl?" #####
        probe_text.tStart = t
        probe_text.setAutoDraw(True)
        response_keys.setAutoDraw(True)

        ####====check for response====##### 
        probe_resp.tStart = t
        win.callOnFlip(probe_resp.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
        thing = True
        while thing: 
            win.flip()
            theseKeys = event.getKeys(keyList=['y', 'n', 'd'])
            if len(theseKeys) > 0:  # at least one key was pressed
                probe_text.setAutoDraw(False)
                response_keys.setAutoDraw(False)
                probe_resp.keys = theseKeys[-1]  # just the last key pressed
                probe_resp.rt = probe_resp.clock.getTime()
                # was this 'correct'?
                if probe_resp.keys == 'y' and trial_num == 2:
                    probe_resp.corr = 1
                    feedback.setText("correct")
                    feedback.draw()
                    thing = False
                elif probe_resp.keys == 'n' and not trial_num == 2:
                    probe_resp.corr = 1
                    feedback.setText("correct")
                    feedback.draw()
                    thing = False
                elif probe_resp.keys == 'd':
                    probe_resp.corr = 0
                    feedback.setText("(don't know)")
                    feedback.draw()
                    thing = False
                else:
                    probe_resp.corr = 0
                    feedback.setText("incorrect")
                    feedback.draw()
                    thing = False
        win.flip()
        core.wait(1)

        ####====Check if response is too slow====####
        if probe_resp.rt > probe_duration:
            too_slow.draw()
            win.flip()
            core.wait(2) 
        
        ####====Space to continue====####
        event.clearEvents(eventType='keyboard')
        space_cont.draw()
        win.flip()
        thisKey = event.waitKeys(keyList=['space'])
        while not 'space' in thisKey:
            thisKey = event.waitKeys(keyList=['space'])
        core.wait(1)

    # ===== INSTRUCTIONS 2 ====== #
    counter = 0
    while counter < len(part2Intro):
        message1.setText(part2Intro[counter])
        if counter == 0:
            message2.setText(bottom_text[0])
        elif counter in range(1, (len(part2Intro) - 1)):
            message2.setText(bottom_text[1])
        else: 
            message2.setText(bottom_text[2])
        #display instructions and wait
        message1.draw()
        message2.draw() 
        win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(counter+1))
        win.flip()
        #check for a keypress
        thisKey = event.waitKeys()
        if thisKey[0] in ['q','escape']:
            core.quit()
        elif thisKey[0] == 'backspace' and counter > 0:
            counter -= 1
        else:
            counter += 1

    # ===== LOG FILE ====== #
    with open('data/{}trial_log.txt'.format(expInfo['participant']), 'w') as log_file:
        log_file.write('Trial\t' + 
                       'Beat\t' + 
                       'Sentence\t' + 
                       'Sentence_extraction\t' + 
                       'Congruency\t' + 
                       'Probe\t' + 
                       'Probe_clause\t' + 
                       'Response\t' + 
                       'Accuracy\t' + 
                       'RT' + '\n')
        trial_num = 0
        # ===== TRIALS ====== #
        for thisTrial in all_trials:  
            trial_num += 1
            ####====ABBREVIATE PARAMETER NAMES====####
            if thisTrial != None:
                for paramName in thisTrial:
                    exec('{} = thisTrial[paramName]'.format(paramName))
            
            probe_resp = event.BuilderKeyResponse()

            ####====SETUP TRIAL COMPONENTS LIST====####
            # initialize trial components list
            trialComponents = []
            # add auditory stimuli component
            if (beat_type == 'binary' and extraction == 'subject' and congruency == 'congruent') or extraction == 'assorted':
                beat_stim = binary_beat
                word_offset = 7 * beat_freq
            elif beat_type == 'binary' and extraction == 'subject' and congruency == 'incongruent':
                beat_stim = binary_beat
                word_offset = 8 * beat_freq
            elif beat_type == 'ternary' and extraction == 'object' and congruency == 'congruent':
                beat_stim = ternary_beat
                word_offset = 8 * beat_freq
            elif beat_type == 'ternary' and extraction == 'object' and congruency == 'incongruent':
                beat_stim = ternary_beat
                word_offset = 9 * beat_freq
            trialComponents.extend([beat_stim]) # add beat stim to trialComponents list
            # add text stimuli components
            for i in range(len(sent_stim)): # for i in range(len(trial['sent_stim'])):
                exec('trialComponents.extend([{}])'.format('word' + '_' + str(i+1)))
                word_stim_list[i].setText(sent_stim[i])
            
            # set probe text for the trial
            probe_text.setText(probe)

            ####====BASIC ROUTINE CHECKS====####
            continueRoutine = True
            # keep track of which components have finished
            for thisComponent in trialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            t = 0
            trialClock.reset()  # clock
            frameN = -1
            beatDuration = len(sent_stim)*beat_freq + word_offset

            ####====START MAIN TRIAL ROUTINE====####
            while continueRoutine: 
                # get current time
                t = trialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                
                ##### 1. start/stop beat_stim  #####
                if t >= 0.0 + sound_delay and beat_stim.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    beat_stim.tStart = t
                    beat_stim.frameNStart = frameN  # exact frame index
                    beat_stim.play()  # start the sound (it finishes automatically)
                    fixation.setAutoDraw(True)
                if beat_stim.status == STARTED and t >= beatDuration:
                    beat_stim.stop()

                ##### 2.  iterate through sentence text stimuli #####   
                for word_index in range(len(sent_stim)):
                    if t >= word_index * beat_freq + word_offset and word_stim_list[word_index].status == NOT_STARTED:
                        fixation.setAutoDraw(False)
                        # keep track of start time/frame for later
                        word_stim_list[word_index].tStart = t
                        word_stim_list[word_index].frameNStart = frameN  # exact frame index
                        word_stim_list[word_index].setAutoDraw(True)
                    frameRemains = (beat_freq * word_index) + beat_freq + word_offset - win.monitorFramePeriod * 0.75  # most of one frame period left
                    if word_stim_list[word_index].status == STARTED and t >= frameRemains:
                        word_stim_list[word_index].setAutoDraw(False)

                ##### 3.  check if all components have finished #####
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in trialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                ##### 4.  refresh the screen #####
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            ####====Ending Trial Routine====####
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            beat_stim.stop()  # ensure sound has stopped at end of routine

            ####====Probe====####
            # 3.  display probe text e.g. "The boy helped the girl?" #####
            probe_text.tStart = t
            probe_text.setAutoDraw(True)
            response_keys.setAutoDraw(True)

            ####====check for response====##### 
            probe_resp.tStart = t
            win.callOnFlip(probe_resp.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
            thing = True
            while thing: 
                win.flip()
                theseKeys = event.getKeys(keyList=['y', 'n', 'd'])
                if len(theseKeys) > 0:  # at least one key was pressed
                    probe_text.setAutoDraw(False)
                    response_keys.setAutoDraw(False)
                    probe_resp.keys = theseKeys[-1]  # just the last key pressed
                    probe_resp.rt = probe_resp.clock.getTime()
                    # was this 'correct'?
                    if probe_resp.keys == 'y' and (\
                                            pos_neg == 'positive' or \
                                                ( \
                                                (pos_neg == 'subneg_objpos' and clause == 'relative_clause' and extraction == 'object') or \
                                                (pos_neg == 'subpos_objneg' and clause == 'relative_clause' and extraction == 'subject') \
                                                )):
                        probe_resp.corr = 1
                        feedback.setText("correct")
                        feedback.draw()
                    elif probe_resp.keys == 'n' and (\
                                                pos_neg == 'negative' or \
                                                ( \
                                                (pos_neg == 'subpos_objneg' and clause == 'relative_clause' and extraction == 'object') or \
                                                (pos_neg == 'subneg_objpos' and clause == 'relative_clause' and extraction == 'subject') \
                                                )):
                        probe_resp.corr = 1
                        feedback.setText("correct")
                        feedback.draw()
                    elif probe_resp.keys == 'd':
                        probe_resp.corr = 0
                        feedback.setText("(don't know)")
                        feedback.draw()
                    else:
                        probe_resp.corr = 0
                        feedback.setText("incorrect")
                        feedback.draw()
                    #======WRITE DATA TO FILE======#    
                    log_file.write('\t'.join([str(trial_num),
                                str(beat_type),
                                str(sent_stim),
                                str(extraction),
                                str(congruency),
                                str(probe),
                                str(clause),
                                str(probe_resp.keys),
                                str(probe_resp.corr),
                                str(probe_resp.rt)]) + '\n')
                    
                    log_file.flush()
                    
                    probe_text.setAutoDraw(False)
                    thing = False
            win.flip()
            core.wait(1)

            ####====Check if response is too slow====####
            if probe_resp.rt > probe_duration:
                too_slow.draw()
                win.flip()
                core.wait(2) 
            
            ####====Space to continue====####
            event.clearEvents(eventType='keyboard')
            space_cont.draw()
            win.flip()
            thisKey = event.waitKeys(keyList=['space'])
            while not 'space' in thisKey:
                thisKey = event.waitKeys(keyList=['space'])

            #thisExp.nextEntry()
            core.wait(.5)

        logging.flush()

    ################################################
    ############## GSI QUESTIONNAIRE ################
    ################################################
    # ===== INSTRUCTIONS 3 ====== #
    counter = 0
    while counter < len(part3Intro):
        message1.setText(part3Intro[counter])
        if counter == 0:
            message2.setText(bottom_text[0])
        elif counter in range(1, (len(part3Intro) - 1)):
            message2.setText(bottom_text[1])
        else: 
            message2.setText(bottom_text[2])
        #display instructions and wait
        message1.draw()
        message2.draw() 
        win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(counter+1))
        win.flip()
        #check for a keypress
        thisKey = event.waitKeys()
        if thisKey[0] in ['q','escape']:
            core.quit()
        elif thisKey[0] == 'backspace':
            counter -= 1
        else:
            counter += 1

    with open('data/{}questionnaire_log.txt'.format(expInfo['participant']), 'w') as log_file:
        log_file.write('Question_num\t' +
                       'Question\t' +
                       'Response' + '\n')

        quest_num = 1 # initialising counter 
        for question in gsi_part1:
            message1.setText(question)
            while GSI.noResponse: 
                message1.draw()
                GSI.draw()
                win.flip()
            response = GSI.getRating()
            #======WRITE DATA TO FILE======#    
            log_file.write('\t'.join([str(quest_num),
                            str( question.replace('\n','') ),
                            str( response.replace('\n','') )]) + '\n')
            
            log_file.flush()
            GSI.noResponse = True
            GSI.response = None
            quest_num += 1
            core.wait(.2)
        
        quest_num = 1 # initialising counter 
        for question in gsi_part2:
            message1.setText(question)
            GSI = visual.RatingScale(win, name='GSI', marker='triangle',
                             textSize = 0.4, showValue = False, acceptText = 'confirm',
                              size=1.5, pos=[0.0, -0.4], 
                              choices= gsi_part2_scales[quest_num - 1],
                             tickHeight=-1)
            while GSI.noResponse: 
                message1.draw()
                GSI.draw()
                win.flip()
            response = GSI.getRating()
            #======WRITE DATA TO FILE======#    
            log_file.write('\t'.join([str((quest_num + 31)),
                            str( question.replace('\n','') ),
                            str( response.replace('\n','') )]) + '\n')
            
            log_file.flush()
            GSI.noResponse = True
            GSI.response = None
            quest_num += 1
            core.wait(.2)
    endMessage.draw()
    win.flip()
    core.wait(5)
finally:
    win.close()
    core.quit()
