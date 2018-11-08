import wave
import numpy as np
import pygame

##### Parameters #####
SAMPLERATE = 48000  # Hz
AMPLITUDE = 10000
NCHANNELS = 1 # mono: sound played identically in both channels
SOUNDLEN = .4 
SOUNDFREQ = 800

##### Constructing tone #####

# calculate the total amount of cycles in the SOUNDLEN
ncycles = SOUNDLEN * SOUNDFREQ

# calculate the total amount of samples per SOUNDLEN
nsamples = SOUNDLEN * SAMPLERATE

# calculate samples per cycle
spc = nsamples / ncycles

# stepsize: distance between samples within a cycle
stepsize = (2*np.pi) / spc

# create a range of numbers between 0 and 2*pi
x = np.arange(0, 2*np.pi, stepsize)

# make a sine wave out of the range
sine = np.sin(x)

# increase the amplitude
tone = sine * AMPLITUDE

# repeat the sine wave for the length of the tone
tone = np.tile(tone, int(ncycles))

##### MIXING IT ALL TOGETHER #####

# initialise mixer module (it requires the sampling rate and num of channels)
pygame.mixer.init(frequency=SAMPLERATE, channels=NCHANNELS)

# create sound out of the allsines vector
tone = pygame.mixer.Sound(tone.astype('int16')) 

# open new wave file objects
tonefile = wave.open('test_tone.wav', 'w')

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