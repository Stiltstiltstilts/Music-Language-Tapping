from psychopy import core, visual, logging, gui, event, prefs, data, sound, monitors
prefs.general['audioLib'] = ['pyo']
prefs.general['audioDriver'] = ['ASIO']
from numpy.random import random, randint, normal, shuffle
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import pygame.midi
import os

print(prefs.general['audioDriver'])

# check relative paths correct
_thisDir = os.path.abspath(os.path.dirname(__file__))
os.chdir(_thisDir)

# load test tone
test_tone = sound.Sound(os.path.join('Stimuli', 'Tones', 'test_tone.wav'))

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
                allowGUI=False,
                color = 'black')

clock = core.Clock()

white_flash = visual.Rect(win, width=55, height=50, fillColor='White')
white_flash.draw()
win.flip()
event.waitKeys()
try:
    for i in range(2):
        win.flip()
        core.wait(1)
        #pygame.midi.init() # initialising midi
        #drum_pad = pygame.midi.Input(pygame.midi.get_default_input_id())
        test_tone.status = NOT_STARTED
        clock.reset()
        t = 0
        while t < 2:
            t = clock.getTime()
            if t >= 0 and test_tone.status == NOT_STARTED:
                white_flash.draw()
                win.flip()
                t1 = clock.getTime()
                test_tone.play()
                t2 = clock.getTime()
                test_tone.status = STARTED
            #if drum_pad.poll():
                    #print(drum_pad.read(1))
        test_tone.stop()
        print((t2 - t1) * 1000)
        #drum_pad.close()

finally:
    #pygame.midi.quit()
    win.close()
    core.quit()