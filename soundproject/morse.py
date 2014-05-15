import wave
import random
import struct
import math
import argparse

DOT_LENGTH = 10000
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

def tone(length, frequency=900.0, framerate=44100, amplitude=0.5):

    period = int(framerate / frequency)
    if amplitude > 1.0: amplitude = 1.0
    if amplitude < 0.0: amplitude = 0.0

    amplitude = amplitude * 32767

    vals = []
    for i in range(length):
        val = int(float(amplitude) * math.sin(2.0*math.pi*float(frequency)*(float(i%period)/float(framerate))))
        pv = struct.pack('h', val)
        vals.append(pv)

    valstr = ''.join(vals)
    return valstr

def space(length):

    vals = []
    for i in range(length):
        pv = struct.pack('h', 0)
        vals.append(pv)

    valstr = ''.join(vals)
    return valstr

def writeMorse(output_string, debug=False, filename='morse_output.wav'):

    noise_output = wave.open(filename, 'w')
    noise_output.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))

    values = []
    
    output_string = output_string.upper()

    for char in output_string:
        if char.isspace():
            packed_value = wspace()
            values.append(packed_value)
            if (debug): print char
        else:
            morse_str = MORSE_DICT[char];
            for dd in morse_str:
                if dd == '-':
                    packed_value = dash()
                elif dd == '.':
                    packed_value = dot()
                else:
                    print 'character not understood:', dd
                    break
                values.append(packed_value)
            packed_value = lspace()
            values.append(packed_value)
            if (debug): print char, morse_str

    value_str = ''.join(values)
    noise_output.writeframes(value_str)

    noise_output.close()

    return filename

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="Run with Debug Output", default=0, type=int)
    parser.add_argument('-f', '--filename', help="Filename to write wav file", default='morse_output.wav', type=str)
    parser.add_argument('output_string', help="String to convert to morse")
    args = parser.parse_args()

    fn = writeMorse(args.output_string, debug=args.debug, filename=args.filename)

    print 'Wrote file to ', fn

if __name__ == "__main__":
    main()
