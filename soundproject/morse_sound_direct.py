import random
import math
import argparse
import wave
import alsaaudio

DOT_LENGTH = 1000
DASH_LENGTH = 3*DOT_LENGTH

MORSE_DICT = {
    'A': '.-',     'B': '-...',   'C': '-.-.', 
    'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',
    'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',
    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',
    
    '0': '-----',  '1': '.----',  '2': '..---',
    '3': '...--',  '4': '....-',  '5': '.....',
    '6': '-....',  '7': '--...',  '8': '---..',
    '9': '----.'
    }

def dot():
    return tone(DOT_LENGTH) + space(DOT_LENGTH)

def dash():
    return tone(DASH_LENGTH) + space(DOT_LENGTH)

def lspace():
    return space(DASH_LENGTH)

def wspace():
    return space(2*DASH_LENGTH)

def tone(length, frequency=800.0, framerate=44100, amplitude=0.5):

    period = int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0

    amplitude = amplitude * 32767

    vals = []
    for i in range(length):
        val = int(float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))))
        vals.append(str(val))

    valstr = "".join(vals)
    return valstr

def space(length):

    vals = []
    for i in range(length):
        vals.append(str(0))

    valstr = "".join(vals)
    return valstr

def playMorse(output_string, debug=False):

    channels = 1
    sample_size = 2                     # bytes per sample
    frame_size = channels * sample_size # bytes per frame
    frame_rate = 44100                   # frames per second
    byte_rate = frame_rate * frame_size # bytes per second
    # 1 second worth of data per pcm.write() call
    # decrease if shorter notes are needed
    period_size = frame_rate

    pcm = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK)
    pcm.setchannels(channels)
    pcm.setformat(alsaaudio.PCM_FORMAT_U8)
    pcm.setrate(frame_rate)
    pcm.setperiodsize(period_size)

    values = ''
    
    output_string = output_string.upper()

    for char in output_string:
        if char.isspace():
            values = values + wspace()
            if (debug): print char
        else:
            morse_str = MORSE_DICT[char];
            for dd in morse_str:
                if dd == '-':
                    values = values + dash()
                elif dd == '.':
                    values = values + dot()
                else:
                    print 'character not understood:', dd
                    break
            values = values + lspace()
            if (debug): print char, morse_str


    valstr = "".join(values)
    pcm.write(valstr)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="Run with Debug Output", default=0, type=int)
    parser.add_argument('-f', '--filename', help="Filename to write wav file", default='morse_output.wav', type=str)
    parser.add_argument('output_string', help="String to convert to morse")
    args = parser.parse_args()

    playMorse(args.output_string, debug=args.debug, filename=args.filename)

if __name__ == "__main__":
    main()
