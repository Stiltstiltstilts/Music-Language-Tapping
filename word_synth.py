##### IMPORTS #####
from gtts import gTTS
import librosa
from pydub import AudioSegment
import numpy as np
from constants import sub_cong, sub_incong1, sub_incong2, obj_cong, obj_incong1, obj_incong1, obj_incong2, prac
import os

######################
##### PARAMETERS #####
######################
rise_sec = .03333333 # in seconds
beat_length = 1/2.5 # in seconds
sentence_stimuli = [prac,] #[obj_cong, sub_cong]
sub_congruencies = [sub_cong, sub_incong1, sub_incong2]
obj_congruencies = [obj_cong, obj_incong1, obj_incong2]
cong_lists = [obj_congruencies, sub_congruencies]
condition_names = ['Practise'] #['object_congruent', 'object_incongruent1', 'object_incongruent2',
                #'subject_congruent', 'subject_incongruent1', 'subject_incongruent2',]
extractions = ['practise']   #['object','subject']

practise = True

single_dur = beat_length * 1000 # in ms

#####################
##### FUNCTIONS #####
#####################
# define GTTS function to output synthesised speech
def synthWord(word, filename, language="en"):
    "outputs mp3 of word"
    tts = gTTS(text=word, lang=language,)
    tts.save("{}.mp3".format(filename))

########################
##### START SCRIPT #####
########################

# ensure in correct dir
_thisDir = os.path.abspath(os.path.dirname(__file__))
os.chdir(_thisDir)

for fold in condition_names:
        audio_fold = os.path.join(_thisDir, 'Stimuli', 'Audio', fold)
        if not os.path.exists(audio_fold):
                os.mkdir(audio_fold)

##### CREATE EACH WORD STIM USING GTTS #####
# loop through sentence extraction types (subject and object)
for cond_idx, condition in enumerate(sentence_stimuli):   

        # create folder for each condition
        temp_fold = os.path.join(_thisDir, 'Stimuli', 'temp', extractions[cond_idx])
        if not os.path.exists(temp_fold): 
                os.mkdir(temp_fold)

        # loop through each sentence condition (e.g. sent1, sent2, etc)
        for sent_idx, trial_dict in enumerate(condition):   
                sentence = trial_dict['sent_stim']
                # create folder for each sentence and populate with words.mp3
                fold_name = 'sent' + str(sent_idx+1) # e.g. 'sent1', 'sent2' etc
                fold_dir = os.path.join(_thisDir, 'Stimuli', 'temp', extractions[cond_idx], fold_name) 
                os.mkdir(fold_dir)
                os.chdir(fold_dir)
                for word_idx, word in enumerate(sentence):
                        synthWord(word, "{}".format((str(word_idx + 1) + word)).zfill(len(word) + 2))

                ##### PREPROCESS EACH WORD AND COMBINE INTO WHOLE SENTENCE #####
                f = []
                # return list of .mp3 files in folder
                for (dirpath, dirnames, filenames) in os.walk(fold_dir):
                        f.extend(filenames)

                ##### loop through each .mp3 word file #####
                for word_file in f:
                        os.chdir(fold_dir)
                        # Load speech file
                        word, sr = librosa.load(word_file)

                        word, sil_idx = librosa.effects.trim(word) # trimming silence

                        # detect onset
                        onset = librosa.onset.onset_detect(word, units = 'samples') # , backtrack=True
                        onset = onset[0] # just return the first onset

                        # PARAMETERS FOR STRETCHING
                        original_word_len = (len(word))/sr # in secs
                        original_samp = len(word)
                        rise_samp = int(sr * rise_sec) # convert rise len to samples
                        end_dur = int(beat_length * sr) # convert beat len to samples...should be 7350
                        
                        uncorrected_stretch = original_samp / end_dur
                        corrected_onset = int(onset / uncorrected_stretch)

                        # compute stretch factor
                        stretch_factor = original_samp / ( end_dur + (corrected_onset - rise_samp) )

                        # Stretch
                        word = librosa.effects.time_stretch(word, stretch_factor)

                        # compute stretched onset
                        #onset = int(onset / stretch_factor)
                        onset = librosa.onset.onset_detect(word, units = 'samples')
                        onset = onset[0] # just return the first onset

                        # start sound file from the rise-len before the onset
                        word = word[int(onset - rise_samp):]

                        # correction procedure because librosa stretch doens't work properly
                        # compute diff between desired duration and actual
                        difference = end_dur - len(word)

                        # zero pad the difference
                        if difference > 0:
                                word = np.pad(word, (0,difference), 'constant')
                        elif difference < 0:
                                word = word[:difference]  
                        else:
                                word = word

                        # determine filename and save audio
                        processed_filename = (os.path.splitext(word_file)[0] + ".wav")
                        librosa.output.write_wav(processed_filename, word, sr)

                ##### COMBINING SOUNDFILES #####
                # Create list of sentence folders in current dir
                #folds = []
                #for folder in [f for f in os.listdir(os.path.join(_thisDir, 'sub_cong')) if os.path.isdir(f)]:
                #        folds.append(folder)


                # Return list of wav files in folder
                wav_files = []
                for file in [f for f in os.listdir('.') if f.endswith('.wav')]:
                        wav_files.extend([file])

                if not practise:
                        for cong_idx, congs in enumerate(cong_lists[cond_idx]):
                                os.chdir(fold_dir)
                                trial_dict2 = congs[sent_idx]
                                if trial_dict2['extraction'] == 'subject':
                                        if trial_dict2['congruency'] == 'congruent':
                                                total_dur = (single_dur * 11) + (single_dur * 14)
                                                tone_displacement = single_dur * 11
                                        elif trial_dict2['congruency'] == 'incongruent1':
                                                total_dur = (single_dur * 12) + (single_dur * 14)
                                                tone_displacement = single_dur * 12
                                        elif trial_dict2['congruency'] == 'incongruent2':
                                                total_dur = (single_dur * 10) + (single_dur * 14)
                                                tone_displacement = single_dur * 10
                                elif trial_dict2['extraction'] == 'object':
                                        if trial_dict2['congruency'] == 'congruent':
                                                total_dur = (single_dur * 8) + (single_dur * 11)
                                                tone_displacement = single_dur * 8
                                        elif trial_dict2['congruency'] == 'incongruent1':
                                                total_dur = (single_dur * 9) + (single_dur * 11)
                                                tone_displacement = single_dur * 9
                                        elif trial_dict2['congruency'] == 'incongruent2':
                                                total_dur = (single_dur * 7) + (single_dur * 11) 
                                                tone_displacement = single_dur * 7

                                # Create blank slate to add audio to
                                final_stim = AudioSegment.silent(duration = total_dur)

                                # import tone file and add to start of final_stim
                                if trial_dict2['extraction'] == 'subject':
                                        tone = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "ternary_beat_2.wav"), format="wav")
                                else:
                                        tone = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "ternary_beat.wav"), format="wav")
                                final_stim = final_stim.overlay(tone)

                                # loop through words in sentence creating word objects for each and join together
                                for word_idx, word in enumerate(wav_files):  
                                        exec('{} = AudioSegment.from_file(word, format="wav")'.format('word' + str(word_idx + 1)))
                                        if trial_dict['extraction'] == 'object':
                                                exec('final_stim = final_stim.overlay({}, position = tone_displacement + (word_idx * single_dur))'.format('word' + str(word_idx + 1)))
                                        elif trial_dict['extraction'] == 'subject':
                                                if word_idx < 2:
                                                        exec('final_stim = final_stim.overlay({}, position = tone_displacement + (word_idx * single_dur))'.format('word' + str(word_idx + 1)))
                                                elif word_idx >= 2 and word_idx < 4:
                                                        exec('final_stim = final_stim.overlay({}, position = tone_displacement + ((word_idx + 1) * single_dur))'.format('word' + str(word_idx + 1)))
                                                elif word_idx >= 4:
                                                        exec('final_stim = final_stim.overlay({}, position = tone_displacement + ((word_idx + 2) * single_dur))'.format('word' + str(word_idx + 1)))


                                # save the eventual file in a different folder?
                                
                                os.chdir(os.path.join(_thisDir, 'Stimuli', 'Audio', condition_names[(3*cond_idx)+cong_idx]))
                                file_handle = final_stim.export("{}.wav".format(fold_name), format="wav")
                if practise:
                        os.chdir(fold_dir)
                        if sent_idx == 0:
                                total_dur = (single_dur * 11) + (single_dur * 14)
                                tone_displacement = single_dur * 11
                                tone = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "ternary_beat_2.wav"), format="wav")
                        elif sent_idx == 1:
                                total_dur = (single_dur * 9) + (single_dur * 11)
                                tone_displacement = single_dur * 9
                                tone = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "ternary_beat.wav"), format="wav")
                        elif sent_idx == 2:
                                total_dur = (single_dur * 10) + (single_dur * 14)
                                tone_displacement = single_dur * 10
                                tone = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "ternary_beat_2.wav"), format="wav")
                        elif sent_idx == 3:
                                total_dur = (single_dur * 9) + (single_dur * 11)
                                tone_displacement = single_dur * 9
                                tone = AudioSegment.from_file(os.path.join(_thisDir, 'Stimuli', 'Tones', "ternary_beat.wav"), format="wav")

                        # Create blank slate to add audio to
                        final_stim = AudioSegment.silent(duration = total_dur)

                        final_stim = final_stim.overlay(tone)

                        # loop through words in sentence creating word objects for each and join together
                        for word_idx, word in enumerate(wav_files):  
                                exec('{} = AudioSegment.from_file(word, format="wav")'.format('word' + str(word_idx + 1)))
                                if sent_idx == 1 or sent_idx == 3:
                                        exec('final_stim = final_stim.overlay({}, position = tone_displacement + (word_idx * single_dur))'.format('word' + str(word_idx + 1)))
                                elif sent_idx == 0 or sent_idx == 2:
                                        if word_idx < 2:
                                                exec('final_stim = final_stim.overlay({}, position = tone_displacement + (word_idx * single_dur))'.format('word' + str(word_idx + 1)))
                                        elif word_idx >= 2 and word_idx < 4:
                                                exec('final_stim = final_stim.overlay({}, position = tone_displacement + ((word_idx + 1) * single_dur))'.format('word' + str(word_idx + 1)))
                                        elif word_idx >= 4:
                                                exec('final_stim = final_stim.overlay({}, position = tone_displacement + ((word_idx + 2) * single_dur))'.format('word' + str(word_idx + 1)))
                        
                        # save the eventual file in a different folder?
                        os.chdir(os.path.join(_thisDir, 'Stimuli', 'Audio', 'Practise'))
                        file_handle = final_stim.export("{}.wav".format(fold_name), format="wav")

                                




