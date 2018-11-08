#!/Users/Stilts/PsychoPyBuild/bin/python 
# -*- coding: utf-8 -*-

#####################
#####==IMPORTS==#####
#####################

import csv, os
import customFunctions as fun # my own function for preprocessing the text

#############################
#####==BASIC VARIABLES==#####
#############################

FGC = (1, 1, 1) #white
BGC = (0, 0, 0) #grey
TEXTSIZE = 42 #text size for stim (not instructions)
TEXTCORDS = (0, 0) #Centre of screen
beat_freq = 1/3  #0.417 #2.4Hz
frameInterval = 0.0166667 #framerate.... CHECK THIS
sound_delay = .08 # 0.003 for processing command + .102 for soundcard/driver processing and sound coming out of earphones
trial_duration = 10 # seconds
probe_duration = 5 # seconds
n_tap_trials = 6

_thisDir = os.path.abspath(os.path.dirname(__file__)) #change to local directory
os.chdir(_thisDir)

#####################
#####==STIMULI==#####
#####################

###===INSTRUCTIONS===###
part1Intro = fun.instImport('Stimuli/Instructions/Part1.txt')
part2Intro = fun.instImport('Stimuli/Instructions/Part2.txt')
part3Intro = fun.instImport('Stimuli/Instructions/Part3.txt')
part4Intro = fun.instImport('Stimuli/Instructions/Part4.txt')
bottom_text = fun.instImport('Stimuli/Instructions/bottom_text.txt')

###===SENTENCES===###
sub_cong = fun.sentencePreProcess('Stimuli/Sentences/Subj_extracted.txt', 'congruent', 'ternary', 'subject')
sub_incong1 = fun.sentencePreProcess('Stimuli/Sentences/Subj_extracted.txt', 'incongruent1', 'ternary', 'subject') 
sub_incong2 = fun.sentencePreProcess('Stimuli/Sentences/Subj_extracted.txt', 'incongruent2', 'ternary', 'subject') 

obj_cong = fun.sentencePreProcess('Stimuli/Sentences/Obj_extracted.txt', 'congruent', 'ternary', 'object') 
obj_incong1 = fun.sentencePreProcess('Stimuli/Sentences/Obj_extracted.txt', 'incongruent1', 'ternary', 'object') 
obj_incong2 = fun.sentencePreProcess('Stimuli/Sentences/Obj_extracted.txt', 'incongruent2', 'ternary', 'object') 

prac = fun.sentencePreProcess('Stimuli/Sentences/Practise.txt', 'other', 'other', 'prac')

###===PROBES===###
probe_mc_pos = fun.probePreProcess('Stimuli/Probes/MC_positive_probes.txt')
probe_mc_neg = fun.probePreProcess('Stimuli/Probes/MC_negative_probes.txt')

probe_rc_subpos_objneg = fun.probePreProcess('Stimuli/Probes/RC_subpos_objneg_probes.txt')
probe_rc_subneg_objpos = fun.probePreProcess('Stimuli/Probes/RC_subneg_objpos_probes.txt')

prac_probes = fun.probePreProcess('Stimuli/Probes/Practise.txt')

###===QUESTIONAIRE===###
gsi_part1 = fun.instImport('Stimuli/Questionnaire/GSI_1-31.txt')
gsi_part2 = fun.instImport('Stimuli/Questionnaire/GSI_32-38.txt')
gsi_part2_scales = [['0','1', '2', '3', '4-5', '6-9', '10+'],
                    ['0', '0.5', '1', '1.5', '2', '3-4', '5+'],
                    ['0', '1', '2', '3', '4-6', '7-10', '11+'], 
                    ['0', '0.5', '1', '2', '3', '4-6', '7+'], 
                    ['0', '0.5', '1', '2', '3-5', '6-9', '10+'], 
                    ['0', '1', '2', '3', '4', '5', '6+'],
                    ['0-15mins', '15-30mins', '30-60mins', '60-90mins', '2hrs', '2-3hrs', '4+hours']]

###=== TAPPING TRIALS ===###
tap_trip = {'audio_file':'triplets.wav', 'tap_type':'triplets'}
tap_ls1 = {'audio_file':'long_short1.wav', 'tap_type':'long short1'}
tap_ls2 = {'audio_file':'long_short2.wav', 'tap_type':'long short2'}
tap_ls3 = {'audio_file':'long_short3.wav', 'tap_type':'long short3'}
