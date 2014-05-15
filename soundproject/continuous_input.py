from morse import writeMorse
from morse_read import readMorse
from morse_sound_direct import playMorse
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
        createWAV()

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
            instr = instring.pop(0)
            if (instr == 'q'):
                break
            current_file = str(int(time()*100)) + '.wav'
            fn = writeMorse(instr, debug=False, filename=current_file)
            wavfiles.append(fn)

def playWAV():

    while True:
        if len(instring) > 0:
            instr = instring.pop(0)
            if (instr == 'q'):
                break
            playMorse(instr, debug=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--wavoutput', help="Output to wav files instead of audio", default=0, type=int)
    args = parser.parse_args()

    print 'Type text to be converted to morse code, and press enter: '

    if args.wavoutput:
        mythread = createWAV_Thread(1, "createWAV", 1)
    else:
        mythread = playWAV_Thread(1, "playWAV", 1)

    mythread.start()

    while True:
        input_string = raw_input('...>  ')
        instring.append(input_string)
        if (input_string == 'q'):
            break

if __name__ == "__main__":
    main()
