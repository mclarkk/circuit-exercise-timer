# Circuit Timer

Circuit Timer is a program for providing timing, cueing, and optional music control for circuit exercises. The default timing configuration and sound effects mimic the at-home workouts hosted online during the coronavirus lockdown by Katherine at [Bay Strength](https://www.baystrength.com/). In no way is this program a substitute for that great community or a personal trainer.

## Install and Run

You will probably need to install two dependencies via `pip`:

```
pip install playsound
pip install gTTS
```

After cloning this repo, run the program with `python circuit_timer.py`.

## Configure

There are a number of configurable options, which can be found at the top of `circuit_timer.py`.

- `num_exercises` determines how many exercises there are in a circuit. Default is five.
- `num_circuits` determines how many circuits (repeats of exercise sets) there are in a workout. Default is five.
- `exercise_duration_sec` determines how long each individual exercise is. A sound and speech cue will play halfway through, which during asymmetric exercises helps to indicate when users should switch sides. (Default is 40 seconds.)
- `circuit_break_duration_min` determines how long breaks are between circuits. (Default is three minutes.)
- `switch_exercise_duration_sec` determines how much time users are given to switch between exercises during a circuit. (Default is 10 seconds.)
- `circuit_countdown_duration_sec` determines how much warning users are given to get ready before the start of a circuit. (Default is 10 seconds.)
- `music_player_enabled` determines whether to play/pause music automatically. Currently only Mac + Spotify is supported, but adding other players or OSes is theoretically straightforward. By default this is set to True, but will be automatically disabled on non-Mac systems.

## Notes

You may not need to use gTTS (Google Text-to-Speech). It is only used to create a synthetic speech file if one doesn't already exist for the utterance in question. I checked in the sound files generated for

## Sound effect sources:

- beep: https://freesound.org/people/CGEffex/sounds/96640/
- whistle: https://freesound.org/people/tommon/sounds/40754/
- airhorn: https://freesound.org/people/jacksonacademyashmore/sounds/414208/
- gong: http://www.wavsource.com/snds_2020-03-30_7102365145747638/sfx/gong.wav
