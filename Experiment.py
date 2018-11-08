
################################################
################# Imports ######################
################################################
from psychopy import core, visual, logging, gui, event, prefs, data, sound, monitors
prefs.general['audioLib'] = ['pyo']
prefs.general['audioDriver'] = ['ASIO']
from numpy.random import random, randint, normal, shuffle
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import pygame.midi
import os
import sys
import numpy as np
from constants import *
from customFunctions import trialCreator

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
expName = 'Word_tapping_fun_times'
# Define experiment info
expInfo = {'session':'001', 'participant':'001',
    'handedness':'', 'gender':'', 'native language': '', 'age': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName,)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()
# Create filename for data file (absolute path + name)
filename = _thisDir + os.sep + 'data/{0}'.format(expInfo['participant'])

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

# setup window
mon = monitors.Monitor(name = 'OptiPlex 7440',
                        width = 1920,
                        distance = 80)
mon.setWidth(80)
mon.setSizePix([1920, 1080])

win = visual.Window(fullscr=True,
                size = [1920, 1080],
                monitor=mon,
                units='deg',
                allowGUI=False)

trialClock = core.Clock()

# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess 60Hz

with open('data/{}participant_info.txt'.format(expInfo['participant']), 'w') as log_file:
    log_file.write('Session\t' +
                    'Participant\t' +
                    'Handedness\t' +
                    'Gender\t' +
                    'Native_language\t' +
                    'Age\t' +
                    'frameRate\t' + '\n')
 
    log_file.write('\t'.join([str(expInfo['session']),
                            str(expInfo['participant']),
                            str(expInfo['handedness']),
                            str(expInfo['gender']),
                            str(expInfo['native language']),
                            str(expInfo['age']),
                            str(expInfo['frameRate'])]) + '\n')
log_file.close()

################################################
########## Trial list construction #############
################################################

# Main sentences
main_conditions = [sub_cong, sub_incong1, sub_incong2, obj_cong, obj_incong1, obj_incong2,]  
main_probes = [probe_mc_pos, probe_mc_neg, probe_rc_subpos_objneg, probe_rc_subneg_objpos,]
sentence_list = trialCreator(main_conditions, main_probes) # using function in customFunctions.py script to randomise and assemble sentences and probes

# Combining main and assorted trials into one list
all_trials = sentence_list
all_trials = data.TrialHandler(trialList = all_trials[:], nReps = 1, method = 'random', extraInfo = expInfo, name = 'all_trials')
thisTrial = all_trials.trialList[0]  # so we can initialise stimuli with some values

# Practice trials
prac_list = [ {**prac[i], **prac_probes[i]} for i in range(len(prac)) ]
prac_list = data.TrialHandler(trialList = prac_list[:], nReps = 1, method = 'sequential', extraInfo = expInfo, name = 'practice_trials')
thisPracTrial = prac_list.trialList[0]  # so we can initialise stimuli with some values

# Tapping trials
tap_conditions = [tap_trip, tap_ls1, tap_ls2, tap_ls3,]
tap_list = data.TrialHandler(trialList = tap_conditions[:], nReps = 4, method = 'random', extraInfo = expInfo, name = 'tapping_trials')
thisTapTrial = tap_list.trialList[0]  # so we can initialise stimuli with some values

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
    probe_text = visual.TextStim(win, pos=[0,0], color=FGC, alignHoriz='center', name='top_probe', text="placeholder")
    pygame.midi.init() # initialising midi
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

    # ===== LOG FILES ====== #
    # File for all trial information without tapping info 
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
    log_file.close()

    # File for tapping info in main trials
    with open('data/{}tapping_log.txt'.format(expInfo['participant']), 'w') as tap_file:
        tap_file.write('Trial\t' + 
                        'Beat\t' +
                        'Congruency\t' +
                        'Sentence_extraction\t' +
                        'Probe_clause\t' +
                        'Accuracy\t' +
                        'button\t' +
                        'timestamp' + '\n')
    tap_file.close()
    
    # File for tapping info in tapping-only trials
    with open('data/{}tap_only_log.txt'.format(expInfo['participant']), 'w') as tap_only_file:
        tap_only_file.write('Trial\t' + 
                        'tap_type\t' +
                        'button\t' +
                        'timestamp' + '\n')
    tap_only_file.close()

    ################################################
    ############## START EXPERIMENT ################
    ################################################
    
    # ===== TAPPING TRIALS INTRO ====== #
    
    if expInfo['participant'] == "test":
        counter = len(part1Intro) - 1
    else:
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
    
    # ===== TAPPING TRIALS ====== 
    trial_num = 0
    for thisTapTrial in tap_list: 
        trial_num += 1
        drum_pad = pygame.midi.Input(pygame.midi.get_default_input_id())
        # Abbeviate parameter names... e.g. thisPracTrial['beat_type'] becomes beat_type
        if thisTapTrial != None:
            for paramName in thisTapTrial:
                exec('{} = thisTapTrial[paramName]'.format(paramName))
        trialComponents = []
        file_loc = os.path.join('Stimuli', 'Tones', str(audio_file))
        audio_stim = sound.Sound(file_loc)  
        audio_stim.status = NOT_STARTED
        trialComponents.extend([audio_stim]) 
        t = 0
        tap_data = []
        trialClock.reset()  # clock
        continueRoutine = True
        while continueRoutine:
            t = trialClock.getTime()
            ##### 1. start/stop beat_stim  #####
            if t >= 0.0 and audio_stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                start_time = pygame.midi.time() # keep track of sound start time to adjust taps later
                audio_stim.play()  # start the sound (it finishes automatically)
                fixation.setAutoDraw(True)

            ##### 2. check for midi input and save #####
            if drum_pad.poll():
                tap_data.append(drum_pad.read(1))

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
        audio_stim.stop()  # ensure sound has stopped at end of routine
        fixation.setAutoDraw(False)
        drum_pad.close()

        # log tapping info for this trial
        with open('data/{}tap_only_log.txt'.format(expInfo['participant']), 'a') as tap_only_file:
            for tap in tap_data:
                tap_only_file.write('\t'.join([str(trial_num),
                        str(tap_type),
                        str(tap[0][0]),
                        str(tap[0][1] - start_time)]) + '\n')
        tap_only_file.close()

        ####====Space to continue====####
        event.clearEvents(eventType='keyboard')
        space_cont.draw()
        win.flip()
        thisKey = event.waitKeys(keyList=['space'])
        while not 'space' in thisKey:
            thisKey = event.waitKeys(keyList=['space'])

        core.wait(.5)

    # ===== PRACTISE TRIALS INTRO ====== #
    counter = 0
    while counter < len(part2Intro):
        # === set top text === #
        message1.setText(part2Intro[counter]) 
        # === set bottom text === #
        if counter == 0:
            message2.setText(bottom_text[0])
        elif counter in range(1, (len(part2Intro) - 1)):
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

    # ===== PRACTICE TRIALS ====== #
    trial_num = 0
    for thisPracTrial in prac_list:  
        trial_num += 1
        # Abbeviate parameter names... e.g. thisPracTrial['beat_type'] becomes beat_type
        if thisPracTrial != None:
            for paramName in thisPracTrial:
                exec('{} = thisPracTrial[paramName]'.format(paramName))

        probe_resp = event.BuilderKeyResponse()
        
        ####====SETUP TRIAL COMPONENTS LIST====####
        # initialize trial components list
        trialComponents = []
        audio_stim = sound.Sound( str(os.path.join('Stimuli', 'Audio', 'Practise', ('sent' + str(sent_number + 1) + '.wav'))) ) 
        trialComponents.extend([audio_stim,]) # add audio stim to trialComponents list

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

        ####====START PRACTISE TRIAL ROUTINE====####
        while continueRoutine: 
            # get current time
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
            ##### 1. start/stop beat_stim  #####
            if t >= 0.0 and audio_stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                audio_stim.tStart = t
                audio_stim.frameNStart = frameN  # exact frame index
                audio_stim.play()  # start the sound (it finishes automatically)
                fixation.setAutoDraw(True)

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
        audio_stim.stop()  # ensure sound has stopped at end of routine
        fixation.setAutoDraw(False)

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
                if probe_resp.keys == 'n' and (trial_num == 1 or trial_num == 2):
                    probe_resp.corr = 1
                    feedback.setText("correct")
                    feedback.draw()
                    thing = False
                elif probe_resp.keys == 'y' and (trial_num == 3 or trial_num == 4):
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
        elif thisKey[0] == 'backspace' and counter > 0:
            counter -= 1
        else:
            counter += 1

    trial_num = 0 # initialise trial number

    # ===== MAIN TRIALS ====== #
    for thisTrial in all_trials:  
        drum_pad = pygame.midi.Input(pygame.midi.get_default_input_id())

        trial_num += 1
        ####====ABBREVIATE PARAMETER NAMES====####
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))

        probe_resp = event.BuilderKeyResponse() # initialising

        ####====SETUP TRIAL COMPONENTS LIST====####
        # initialize trial components list
        trialComponents = []

        # add auditory stimuli component
        audio_stim = sound.Sound( str(os.path.join('Stimuli', 'Audio', (extraction + '_' + congruency), ('sent' + str(sent_number + 1) + '.wav'))) ) 

        trialComponents.extend([audio_stim],) # add beat stim to trialComponents list

        # set probe text for the trial
        probe_text.setText(probe)

        ####====BASIC ROUTINE CHECKS====####
        continueRoutine = True
        # keep track of which components have finished
        for thisComponent in trialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        t = 0
        tap_data = []
        trialClock.reset()  # clock
        frameN = -1
        
        ####====START MAIN TRIAL ROUTINE====####
        while continueRoutine: 
            t = trialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            
            ##### 1. start/stop beat_stim  #####
            if t >= 0.0 and audio_stim.status == NOT_STARTED:
                # keep track of start time/frame for later
                audio_stim.tStart = t
                audio_stim.frameNStart = frameN  # exact frame index
                start_time = pygame.midi.time() # keep track of sound start time to adjust taps later
                audio_stim.play()  # start the sound (it finishes automatically)
                fixation.setAutoDraw(True)

            ##### 2. check for midi input  #####
            if drum_pad.poll():
                tap_data.append(drum_pad.read(1))

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
        audio_stim.stop()  # ensure sound has stopped at end of routine
        fixation.setAutoDraw(False)

        ####====Probe====####
        # 3.  display probe text e.g. "The boy helped the girl?" #####
        probe_text.tStart = t
        probe_text.setAutoDraw(True)
        response_keys.setAutoDraw(True)

        drum_pad.close()

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

                with open('data/{}trial_log.txt'.format(expInfo['participant']), 'a') as log_file: 
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
                log_file.close()
                probe_text.setAutoDraw(False)
                thing = False
        with open('data/{}tapping_log.txt'.format(expInfo['participant']), 'a') as tap_file:
            for tap in tap_data:
                tap_file.write('\t'.join([str(trial_num),
                        str(beat_type),
                        str(congruency),
                        str(extraction),
                        str(clause),
                        str(probe_resp.corr),
                        str(tap[0][0]),
                        str(tap[0][1] - start_time)]) + '\n')
        tap_file.close()
        win.flip()
        core.wait(.5)

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

        core.wait(.5)
    logging.flush()
    
    ################################################
    ############## GSI QUESTIONNAIRE ################
    ################################################
    # ===== INSTRUCTIONS 3 ====== #
    counter = 0
    while counter < len(part4Intro):
        message1.setText(part4Intro[counter])
        if counter == 0:
            message2.setText(bottom_text[0])
        elif counter in range(1, (len(part4Intro) - 1)):
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
    pygame.midi.quit()
    win.close()
    core.quit()
