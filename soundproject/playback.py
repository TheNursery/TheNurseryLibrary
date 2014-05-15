#!/usr/bin/env python

import alsaaudio, sys

from numpy import arange        # like range, but supports floating point
from math import pi, sin

channels = 2
sample_size = 1                     # bytes per sample
frame_size = channels * sample_size # bytes per frame
frame_rate = 44100                   # frames per second
byte_rate = frame_rate * frame_size # bytes per second
# 1 second worth of data per pcm.write() call
# decrease if shorter notes are needed
period_size = frame_rate

pcm = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
pcm.setchannels(channels)
pcm.setformat(alsaaudio.PCM_FORMAT_U8)
def quantize(f):                # map (-1..1) -> [0..256)
    return int((f+1)*127)       # depends on PCM format
pcm.setrate(frame_rate)
pcm.setperiodsize(period_size)

def sine_wave(freq):
    wave = [chr(quantize(sin(x))) * channels for x
            in arange(0, 2*pi, 2*pi / (frame_rate / freq))]
    wave_data = "".join(wave)
    (nwaves, extra_bytes) = divmod(period_size * frame_size, len(wave_data))
    pcm.write((wave_data * nwaves) + wave_data[:extra_bytes])

for i in range(10):
    sine_wave(220)
    sine_wave(440)
