#!/usr/bin/env python
""" Script to test your hearing at high frequencies """

from soundproject.playback import sine_wave

raw_input("WARNING: Please ensure you turn down your headphone/speakers to their\n"
          "lowest setting. Once you have done so press any button to continue\n"
         )
raw_input("The script will play you a tone, if you can hear it press any button to\n"
      "continue. Once you CANT hear the tone enter 'n'. You can exit the program\n"
      "at any time with Ctrl+C")

max_freq = 30000
df = 1000
freq = 5000.0
quit_test = 0
while quit_test == 0: 
    print "Frequency is {}".format(freq)
    sine_wave(freq)
    quit_test = (raw_input("Can you still here it?") == "n") + (freq > max_freq)
    freq += df

