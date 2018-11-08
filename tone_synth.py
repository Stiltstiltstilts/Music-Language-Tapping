##### IMPORTS #####
from pydub import AudioSegment
import numpy as np
import os

##### PARAMETERS #####
single_dur = (1/2.5) * 1000 # 400ms

_thisDir = os.path.abspath(os.path.dirname(__file__))
os.chdir(_thisDir)

##### SOUNDS #####
tone_seq = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "ternary_beat_tap.wav"), format="wav")

low_tone = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "low_tone.wav"), format="wav")

gap_tone = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "tone_gap.wav"), format="wav")

silence = AudioSegment.silent(duration = single_dur)

##### ASSEMBLY #####
# first create silences, if necessary
for beat in range (20):
    tone_seq = tone_seq.overlay(silence, position = (single_dur * 3) + beat * (3 * single_dur), gain_during_overlay = -1000)
    tone_seq = tone_seq.fade(to_gain=-20.0, start= ((single_dur * 3) - 50) + beat * (3 * single_dur), duration=50)
    tone_seq = tone_seq.fade(to_gain=+20.0, start= ((single_dur * 3) - 0) + beat * (3 * single_dur), duration=50)
    
for beat in range (4):
    tone_seq = tone_seq.overlay(low_tone, position = beat * (3 * single_dur))

##### SAVING #####
os.chdir(os.path.join(_thisDir, 'Stimuli', 'Tones'))
file_handle = tone_seq.export("long_short3.wav", format="wav")