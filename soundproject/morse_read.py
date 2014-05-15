from pylab import plot, xlabel, ylabel, show, subplot
from scipy import fft, arange, ifft, conj, real
from numpy import sin, linspace, pi, sqrt, array, rint, zeros, delete, argmin
from scipy.signal import hilbert, firwin, lfilter
from scipy.io.wavfile import read, write
from readWAV import readWAV
import argparse

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
    '9': '----.',  ' ': '/'
    }

INV_MORSE = dict((v, k) for k, v in MORSE_DICT.iteritems())

def plotSpectru(y, Fs):
    n = len(y) # lungime semnal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(n/2)] # one side frequency range
    
    Y = fft(y)/n # fft computing and normalization
    Y = Y[range(n/2)]
    
    plot(frq,abs(Y),'r') # plotting the spectrum
    xlabel('Freq (Hz)')
    ylabel('|Y(freq)|')

def envelope(data):
    
    data = data - sum(data)/len(data)

    env = sqrt(data**2 + hilbert(data)*conj(hilbert(data)))
    return env

def envelope2(data, Fs):
    N = 10
    Fc = 10
    h = firwin(N, Fc)
    y = lfilter(h, 1.0, data)
    return y

def truncate(env):
    maxdata = max(env)
    out = zeros(len(env))
    for i in range(len(env)):
        if (env[i] > 0.1*maxdata):
            out[i] = maxdata
        else:
            out[i] = -maxdata
    return out

def lengths(data):
    l = 0
    lens = []
    for i in range(len(data)-1):
        l = l + 1
        if data[i] * data[i+1] < 0:
            if data[i] < 0:
                lens.append(-l)
            else:
                lens.append(l)
            l = 0

    lens = array(lens)
    while max(abs(lens)) > 200*min(abs(lens)):
        lens = delete(lens, argmin(abs(lens)))

    lens = rint(lens / float(min(abs(lens))))

    return lens

def morse(lens):
    morse_list = []
    i = 0
    while i < len(lens):
        if (lens[i] > 0):
            if lens[i] < 2.0:
                morse_list.append('.')
                i = i + 1
            else:
                morse_list.append('-')
                i = i + 1
        else:
            if (lens[i] < -2.0) and (lens[i] > -5.0):
                morse_list.append(' ')
            elif (lens[i] < -5.0):
                morse_list.append(' / ')
            i = i + 1
        
    morse_str = ''.join(morse_list)
    morse_strs = morse_str.split(' ')
    return morse_strs
     
def getascii(morse):
    asc = []
    for str in morse:
        try:
            asc.append(INV_MORSE[str])
        except: 
            pass
    ascstr = ''.join(asc)
    return ascstr

def readMorse(filename, debug=False):
    Fs = 44100;  # sampling rate

    if (debug):
        print 'Reading wav file: ', filename

#    filename = 'test.wav'
    if (debug): print 'First trying to read using scipy.io.wavfile...'
    try:
        rate, data = read(filename)
        if (debug): print 'Read file  using scipy.io.wavfile'
    except:
        if (debug): print 'Scipy package failed, trying readWAV...'
        try:
            data=readWAV(filename)
            if (debug): print 'Read file  using readWAV.readWAV'
        except:
            print 'Failed to read file'
            raise

    if len(data.shape) > 1:
        data = data[:,1]

    y=data
    avg = 1.0*sum(y)/len(y)
    if (debug):
        print avg
    ynew = y - avg
    if (debug):
        avg2 = 1.0*sum(ynew)/len(ynew)
        print avg2

    y1 = envelope(ynew)
    y2 = truncate(y1)

    if (debug):
        timp=len(y)/float(Fs)
        t=linspace(0,timp,len(y))

        subplot(3, 1, 1)
        plot(t,y1, 'r')
        plot(t, y2, 'b')
        xlabel('Time')
        ylabel('Amplitude')
        subplot(3, 1, 2)
        plot(t, ynew, 'b')
        plot(t, y, 'r')
        xlabel('Time')
        ylabel('Amplitude')
        subplot(3, 1, 3)
        plotSpectru(y, Fs)
        show()

    lns = lengths(y2)
    
    if (debug):
        print lns
    
    mrstrs = morse(lns)

    if (debug):
        print mrstrs
    
    message = getascii(mrstrs)
    
    if (debug):
        print(message)

    return message

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help="Run with Debug Output", default=0, type=int)
    parser.add_argument('filename', help="The file to generate.")
    args = parser.parse_args()

    message = readMorse(args.filename, args.debug)

    print message

if __name__ == "__main__":
    main()
