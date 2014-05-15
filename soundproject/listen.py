from time import time
import os

wavfiles = []

for i in range(100):
    current_file = str(int(time()*100)) + '.wav'
    os.system("arecord -f cd -d 10 " + current_file)
    wavfiles.append(current_file)
