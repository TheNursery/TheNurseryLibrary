from morse import writeMorse, playMorse
from morse_read import readMorse
from time import time
import thread
import threading
import argparse

instring = []
wavfiles = []

class createWAV_Thread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        doMorse()

class playWAV_Thread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        playWAV()

def createWAV():

    while True:
        if len(instring) > 0:
            instr, freq, dl = instring.pop(0)
            if (instr == 'q'):
                break
            current_file = str(int(time()*100)) + '.wav'
            fn = writeMorse(instr, debug=False, filename=current_file,
                            frequency=freq, dot_length=dl)
            wavfiles.append(fn)

def playWAV():

    while True:
        if len(instring) > 0:
            instr, freq, dl = instring.pop(0)
            if (instr == 'q'):
                break
            playMorse(instr, debug=False,
                      frequency=freq, dot_length=dl)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wavfile', 
                        help="Output as wav file", default=0, type=int)
    parser.add_argument('-l', '--dot_length', 
                        help="Length of one dot", default=1000, type=int)
    parser.add_argument('-F', '--frequency', 
                        help="Carrier frequency", default=450.0, type=float)
    args = parser.parse_args()

    freq = args.frequency
    dot_length = args.dot_length

    print 'Type text to be converted to morse code, and press enter: '

    if args.wavfile:
        mythread = createWAV_Thread(1, "createWAV", 1)
    else:
        mythread = playWAV_Thread(1, "playWAV", 1)

    mythread.start()

    while True:
        input_string = raw_input('...>  ')
        instring.append((input_string, freq, dot_length))
        if (input_string == 'q'):
            break

if __name__ == "__main__":
    main()
