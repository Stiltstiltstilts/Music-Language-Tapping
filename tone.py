# -*- coding: utf-8 -*-

################################################
################# Imports ######################
################################################

import wave
import numpy as np
import pygame
from scipy import signal
import matplotlib.pylab as plt
from matplotlib import pyplot
import customFunctions as fun


################################################=
################# Parameters ###################
################################################

BASE_AMP = 10000 # amplitude of nonaccented tone... −32,768 to +32,767 range for 16bit
ACCENT_AMP = 20000 # amplitude of accented tone... −32,768 to +32,767 range for 16bit
SAMPLERATE = 48000  # Hz
NCHANNELS = 1 # mono: sound played identically in both channels
SOUNDLEN = 1/2.5   
SOUNDFREQ = 333 # Hz... 333 is about Ab in pitch

finalDuration = SOUNDLEN #* (3*20 + 1) #seconds
nTones = int(finalDuration/SOUNDLEN) # how many sounds per the total duration

################################################
########### Constructing Pure Tone #############
################################################

# calculate the total amount of cycles in the SOUNDLEN
ncycles = SOUNDLEN * SOUNDFREQ

# calculate the total amount of samples per SOUNDLEN
nsamples = int(SOUNDLEN * SAMPLERATE)
print(nsamples)
# calculate samples per cycle
spc = nsamples / ncycles

# stepsize: distance between samples within a cycle
stepsize = (2*np.pi) / spc

# create a range of numbers between 0 and 2*pi
x = np.arange(0, 2*np.pi, stepsize)

# make a sine wave out of the range
sine = np.sin(x)

# increase the amplitude
sine_nonaccent = sine * BASE_AMP
sine_accent = sine * ACCENT_AMP

# repeat the sine wave for the length of the tone
tone_nonaccent = np.tile(sine_nonaccent, int(ncycles))
if len(tone_nonaccent) > nsamples:
    tone_nonaccent = tone_nonaccent[:nsamples]
elif len(tone_nonaccent) < nsamples:
    diff = nsamples - len(tone_nonaccent)
    tone_nonaccent = np.pad(tone_nonaccent, (0,diff), 'constant', constant_values = 0)

tone_accent = np.tile(sine_accent, int(ncycles))
if len(tone_accent) > nsamples:
    tone_accent = tone_accent[:nsamples]
elif len(tone_accent) < nsamples:
    diff = nsamples - len(tone_accent)
    tone_accent = np.pad(tone_accent, (0,diff), 'constant', constant_values = 0)

################################################
############ Modulating Sine Tone ##############
################################################

# Modulation variables
rise_fall_ratio = 19  #(1/842)*16095 # rise_fall_ratio:1 ratio of rise and fall ramps
window_floor = 0.2 # creating window between .2 and 1

# calculate asymmetric Hanning vector (22ms rise and 394 fall)
riseLen = .033333333 #len(tone_accent) / rise_fall_ratio 
fallLen = len(tone_accent) - riseLen         

# create Hann vector for rise len * 2
riseVec = fun.customHanning((riseLen * 2), window_floor)
# delete second half of vector (after 1.0)... i.e. only want upramp
riseVec = riseVec[0:int(riseLen)]

# create Hann vector for fall len * 2
fallVec = fun.customHanning((fallLen * 2), window_floor)
# delete first half of vector
fallVec = fallVec[int(fallLen):]

# combine vectors
hannVec = np.concatenate((riseVec, fallVec),)

if len(hannVec) > len(tone_nonaccent):    # check for rounding problems with hannVec length
    hannVec = hannVec[0:len(tone_nonaccent)]

gap_vec = np.full(int(nsamples), window_floor)

# apply Hanning amplitude modulation
#tone_nonaccent = tone_nonaccent * hannVec
#tone_accent = tone_accent * hannVec
tone_gap = tone_accent * gap_vec

################################################
############## Final mixing etc ################
################################################

# tile tones to the desired length
#meter = np.concatenate((tone_accent, tone_nonaccent, tone_nonaccent),)

#final_output = np.tile(meter, int(nTones/3))

# initialise mixer module (it requires the sampling rate and num of channels)
pygame.mixer.init(frequency=SAMPLERATE, channels=NCHANNELS)

# create sound out of the allsines vector
tone = pygame.mixer.Sound(tone_gap.astype('int16')) #tone = pygame.mixer.Sound(final_output.astype('int16'))

# open new wave file objects
tonefile = wave.open('tone_gap.wav', 'w')

# set parameters for pure tone
tonefile.setframerate(SAMPLERATE)
tonefile.setnchannels(NCHANNELS)
tonefile.setsampwidth(2) # in units of bytes and 8 bits per byte = 16bit

# get buffers
tonebuffer = tone.get_raw()

# write raw buffer to the wave file
tonefile.writeframesraw(tonebuffer)

# close the wave file 
tonefile.close()

# Done!
