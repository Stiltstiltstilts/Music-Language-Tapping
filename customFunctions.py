
#####################
#####==IMPORTS==#####
#####################

import os
import numpy as np
from psychopy import core, visual, event, data, logging
from numpy.random import shuffle

def instImport(path):
    """
    instImport is a function for importing instruction text to be used in the experiment and does the required processing
        required inputs:
                        path: path of input file (as .txt)
        outputs: 
                        Variable with processed data as a list

    """
    # probably also write checks that the path points to a .txt and the outputName is a string

    with open(path, 'r') as f: #open file as object 
        processed_text = f.readlines()
    return processed_text

def sentencePreProcess(path, congruency=None, beat_type=None, extraction=None):
    """
    stimPreProcess is a function for importing sentences from a text file, and then 1) making each sentence a list containing strings for each word, 
    and 2) converting underscores, which code for double words, into a space character within the string (e.g. "that_the" becomes "that the")
        required inputs:
                        path: path of input file (as .txt)
                        congruency: 'congruent' or 'incongruent'
                        beat_type: 'binary_beat' or 'ternary_beat'
                        extraction: 'subject' or 'object'
        outputs: 
                        Variable with processed data as a list

    """
    output_list = []
    with open(path, 'r') as f: #open stimuli file as object 
        rawText = f.readlines()
    # seperate the individual words and then turn underscore into spaces
    for sent_idx, line in enumerate(rawText): # iterate over lines in raw 
        sentence = line[:].replace('\n', '') # getting rid of the line break thing
        sentence = sentence.split(' ') # splitting the sentence up by spaces
        for word_idx, word in enumerate(sentence[:]): # iterate over words
            sentence[word_idx] = word.replace('_', ' ') # cleaning off the underscore and turning it into space
        stim_data = {'sent_stim':sentence, 'beat_type':beat_type, 
                    'congruency':congruency, 'extraction': extraction, 'sent_number': sent_idx,}
        output_list.append(stim_data)

    return output_list

def probePreProcess(path):
    """
    instImport is a function for importing probes in txt file and outputting dictionary with probe and metadata
        required inputs:
                        path: path of input file (as .txt)
        outputs: 
                        Variable with processed data as a list of dictionaries

    """
    # probably also write checks that the path points to a .txt and the outputName is a string

    with open(path, 'r') as f: #open file as object 
        processed_text = f.readlines()
    #Get other info  
    # pos or neg   
    if "positive" in os.path.basename(path):
        pos_neg = 'positive'
    elif "negative" in os.path.basename(path):
        pos_neg = 'negative'
    elif "subneg" in os.path.basename(path): # relative clauses change which statement is correct based on obj or sub extracted
        pos_neg = 'subneg_objpos'
    elif "subpos" in os.path.basename(path):
        pos_neg = 'subpos_objneg'
    else:
        pos_neg = None
    # main or relative clause
    if "MC" in os.path.basename(path):
        clause = 'main_clause'
    elif "RC" in os.path.basename(path):
        clause = 'relative_clause'
    else:
        clause = 'other'  

    final_output = []
    for n in range(len(processed_text)):
        temp = {'probe':processed_text[n].replace('\n', ''),
                        'pos_neg': pos_neg,
                        'clause': clause,
                        'probe_n': n,}
        final_output.append(temp)
    return final_output

def customHanning(M, floor):
    """ 
    this is a function to create a custom hanning window with a non-zero floor, specified by the variable 'floor'
    for example M = 0.2 means creating a hanning window with values between .2 and 1
    """
    a = 0.5 + 0.5*floor
    b = 0.5 - 0.5*floor
    M = int(M)
    custom_hanning_window = [a - b*np.cos(2 * x * np.pi /(M-1)) for x in range(M)]

    return custom_hanning_window

def check_lists_same_len(list_of_lists, message):
    it = iter(list_of_lists)
    the_len = len(next(it))
    if not all(len(l) == the_len for l in it):
        raise ValueError(message)
    return None

def trialCreator(condition_list, probe_condition_list):
    ##### check same num of sentences for 1. sentences, and 2. probes #####
    check_lists_same_len(condition_list, 'Not all conditions have same number of sentences!') 
    check_lists_same_len(probe_condition_list, 'Not all conditions have the same number of probes!')

    ################################################
    ############### Sentences ######################
    ################################################

    ##### Determine no. sents per condition #####
    n_sentences = len(condition_list[0]) 
    n_conditions = len(condition_list)
    sents_per_condition = n_sentences / n_conditions # how many sentences per condition
    assert sents_per_condition.is_integer(), "num sentences does not divide evenly into conditions"
    sents_per_condition = int(sents_per_condition) # convert to integer

    ##### create indices for each condition, and randomise order #####
    condition_idx_list = list(range(n_conditions)) * sents_per_condition # index list for n_conditions * trials_per_condition
    shuffle(condition_idx_list)  # randomise e.g. [1 0 3 2...]

    ##### return list of trial dictionaries (without probes) in original sentence order, but randomised conditions #####
    sentence_list = [ (condition_list[condition_idx_list[i]][i]) for i in range(n_sentences) ]

    ################################################
    ################## Probes ######################
    ################################################

    ##### Determine no. probes per condition #####
    n_probe_conditions = len(probe_condition_list) 
    probes_per_condition = (n_sentences / n_probe_conditions) / n_conditions 
    assert probes_per_condition.is_integer(), "num probes does not divide evenly into conditions"
    probes_per_condition =  int(probes_per_condition)

    # Create indices and randomise order
    probe_idx_list = list(range(n_probe_conditions)) * probes_per_condition # index list for n_conditions * trials_per_condition .... 
    
    ################################################
    ######### Combine sents and probes #############
    ################################################
    
    for main_cond in range(len(condition_list)):   # iterate through main conditions (0-3)
    # combine probes with main trials
        shuffle(probe_idx_list)  # randomise probe indices e.g. [1 0 1 2...]
        probe_counter = 0 # initialize probe counter
        for sent_idx, cond_idx in enumerate(condition_idx_list):
            if cond_idx == main_cond: # IF condition in list is same as condition iterator THEN 
                sentence_list[sent_idx] = {**sentence_list[sent_idx], **probe_condition_list[probe_idx_list[probe_counter]] [sentence_list[sent_idx]['sent_number']]} # 
                probe_counter += 1

    return sentence_list