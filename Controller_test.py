
import pygame.midi
from psychopy import core, visual, logging, gui, event, prefs, data, sound, monitors
prefs.general['audioLib'] = ['pyo']
import os

trialClock = core.Clock()

extraction = 'object'
congruency = 'congruent'
sent_number = 2

sound_file = sound.Sound(os.path.join('Stimuli', 'Audio', (extraction + '_' + congruency), ('sent' + str(sent_number + 1) + '.wav')))#sound_file = sound.Sound('Stimuli\Audio\object_congruent\sent4.wav')

pygame.midi.init()
devices = pygame.midi.get_count()
devices

#input_dev = pygame.midi.get_default_input_id()

#drum_pad = pygame.midi.Input(pygame.midi.get_default_input_id())

thang = [1,2,3,4]

for i in thang:
    drum_pad = pygame.midi.Input(pygame.midi.get_default_input_id())
    trialClock.reset()
    t = 0
    sound_file.play()
    start_time = pygame.midi.time()
    while t < 8:
        t = trialClock.getTime()

        # Starting polling
        if drum_pad.poll():
            data = drum_pad.read(1)

            for event in data:
                control = print(event[0])
                timestamp = print(event[1] - start_time)

    drum_pad.close()
