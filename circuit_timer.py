################################################################################
# Configurable                                                                 #
################################################################################

# num_exercises = 5
# num_circuits = 5
# exercise_duration_sec = 40
# circuit_break_duration_min = 3
# switch_exercise_duration_sec = 10
# circuit_countdown_duration_sec = 10
num_exercises = 2
num_circuits = 2
exercise_duration_sec = 20
circuit_break_duration_min = 0.33
switch_exercise_duration_sec = 10
circuit_countdown_duration_sec = 10
music_player_enabled = True

sound_effect_directory = "sound_effects/"
tts_directory = "speech_cues/"

exercise_start_sound = sound_effect_directory + "airhorn.mp3"
exercise_halfway_sound = sound_effect_directory + "whistle.mp3"
exercise_end_sound = sound_effect_directory + "airhorn.mp3"
circuit_end_sound = sound_effect_directory + "airhorn.mp3"
workout_end_sound = sound_effect_directory + "gong.wav"
countdown_beep = sound_effect_directory + "beep.mp3"

################################################################################
# Imports                                                                      #
################################################################################

from time import time, sleep
import random
from math import ceil
from playsound import playsound
from gtts import gTTS
if music_player_enabled:
    import os
    import platform

################################################################################
# Global variables                                                             #
################################################################################

exercise_half_duration_sec = int(exercise_duration_sec/2)
circuit_break_duration_sec = circuit_break_duration_min * 60
countdown_sound_sec = 3

################################################################################
# Music player config                                                          #
################################################################################

mac_play_spotify = 'osascript -e \'tell application "spotify" to play\''
mac_pause_spotify = 'osascript -e \'tell application "spotify" to pause\''

if platform.system() == 'Darwin': # macOS
    play_music_cmd = mac_play_spotify
    pause_music_cmd = mac_pause_spotify
else:
    print("Music player support is currently limited to Spotify on MacOS")
    music_player_enabled = False

################################################################################
# State transition function                                                    #
################################################################################

def main():
    global state
    while state != finished:
        state()
        if state == circuit_countdown:
            state = exercise_start
        elif state == exercise_start:
            state = exercise_first_half
        elif state == exercise_first_half:
            state = exercise_halfway
        elif state == exercise_halfway:
            state = exercise_second_half
        elif state == exercise_second_half:
            state = exercise_end
        elif state == exercise_end and exercises_not_finished():
            state = switch_exercise
        elif state == exercise_end and exercises_finished():
            state = circuit_end
        elif state == switch_exercise:
            state = exercise_start
        elif state == circuit_end and circuits_not_finished():
            state = circuit_break
        elif state == circuit_end and circuits_finished():
            state = workout_end
        elif state == circuit_break:
            state = circuit_countdown
        elif state == workout_end:
            state = finished
        else:
            print("Reached unknown state")
            state = finished

################################################################################
# State actions                                                                #
################################################################################

def circuit_countdown():
    print("Circuit {}".format(circuit_count + 1))
    say("Get ready! {} seconds".format(circuit_countdown_duration_sec))
    elapsed_time = 0
    if circuit_count == num_circuits - 1:
        elapsed_time += say("Last round!")
    elif circuit_count == num_circuits - 2:
        elapsed_time += say("Two rounds to go!")
    sleep(max(circuit_countdown_duration_sec - countdown_sound_sec - elapsed_time, 0))
    play_countdown(countdown_beep)
    if music_player_enabled: os.system(play_music_cmd)

def exercise_start():
    global rollover_elapsed_time
    rollover_elapsed_time = 0
    print("    Exercise {}".format(exercise_count + 1))
    start_time = time()
    playsound(exercise_start_sound)
    elapsed_time = time() - start_time
    elapsed_time += say("Start")
    rollover_elapsed_time += elapsed_time

def exercise_first_half():
    global rollover_elapsed_time
    sleep(max(exercise_half_duration_sec - rollover_elapsed_time, 0))
    rollover_elapsed_time = 0

def exercise_halfway():
    global rollover_elapsed_time
    start_time = time()
    playsound(exercise_halfway_sound)
    elapsed_time = time() - start_time
    elapsed_time += say("Halfway")
    rollover_elapsed_time = elapsed_time

def exercise_second_half():
    global rollover_elapsed_time
    if circuit_count == num_circuits - 1 and exercise_count == num_exercises - 1:
        duration = exercise_half_duration_sec - countdown_sound_sec - rollover_elapsed_time
        sleep(duration/2)
        elapsed_time = say("Keep it up!")
        sleep(duration/2 - elapsed_time)
        rollover_elapsed_time = 0
    else:
        sleep(max(exercise_half_duration_sec - countdown_sound_sec - rollover_elapsed_time, 0))
        rollover_elapsed_time = 0
    play_countdown(countdown_beep)

def exercise_end():
    global exercise_count
    exercise_count += 1
    playsound(exercise_end_sound)

def switch_exercise():
    elapsed_time = say("Get ready for the next exercise")
    sleep(max(switch_exercise_duration_sec - countdown_sound_sec - elapsed_time, 0))
    play_countdown(countdown_beep)

def circuit_end():
    global exercise_count
    global circuit_count
    exercise_count = 0
    circuit_count += 1
    playsound(circuit_end_sound)
    if music_player_enabled: os.system(pause_music_cmd)

def circuit_break():
    elapsed_time = 0
    if circuit_count == ceil(num_circuits / 2):
        if num_circuits % 2 == 0:
            elapsed_time += say("Woo! Halfway done!")
        else:
            elapsed_time += say("Woo! Over halfway done!")
    elapsed_time += say(random.choice(["Good job!", "Woo",
        "Did you do anything fun this weekend?",
        "Nice hustle", "You're doing great",
        "Nice work", "Have any plans for this weekend?"]))
    sleep(max(circuit_break_duration_sec - circuit_countdown_duration_sec - elapsed_time, 0))

def workout_end():
    playsound(workout_end_sound)
    say("That's it! Nice work.")
    say("Have a good day, and see you soon!")

def finished():
    pass

# state variables
state = circuit_countdown
exercise_count = 0
circuit_count = 0
rollover_elapsed_time = 0

################################################################################
# Helper functions                                                             #
################################################################################

def exercises_finished():
    return exercise_count == num_exercises

def exercises_not_finished():
    return not exercises_finished()

def circuits_finished():
    return circuit_count == num_circuits

def circuits_not_finished():
    return not circuits_finished()

def get_tts_filename(utterance):
    name = utterance.lower()
    name = name.replace(" ", "_")
    remove = ["!", ",", ".", "?", "'"]
    for char in remove:
        name = name.replace(char, "")
    return tts_directory + name + ".mp3"

################################################################################
# Audio functions                                                              #
################################################################################

def play_countdown(beep_file):
    for i in range(3):
        playsound(beep_file)
        sleep(0.8)

def say(utterance):
    start_time = time()
    tts_filename = get_tts_filename(utterance)
    try:
        playsound(tts_filename)
    except OSError:
        myobj = gTTS(text=utterance, lang='en', slow=False)
        myobj.save(tts_filename)
        playsound(tts_filename)
    elapsed_time = time() - start_time
    return elapsed_time


if __name__ =="__main__":
    main()
