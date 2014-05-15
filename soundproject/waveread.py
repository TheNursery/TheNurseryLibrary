import wave
import struct                     

def wavRead(fileN):
  waveFile = wave.open(fileN, 'r')   
  NbChanels = waveFile.getnchannels()
  data = []
  for x in range(NbChanels):
      data.append([])
  for i in range(0,waveFile.getnframes()):               
      waveData = waveFile.readframes(1)   
      data[i%(NbChanels)].append(int(struct.unpack("<h", waveData)[0]))

  RetAR = []
  BitDebth = waveFile.getsampwidth()*8
  for x in range(NbChanels):
       RetAR.append(np.array(data[x]))
       RetAR[-1] = RetAR[-1]/float(pow(2,(BitDebth-1)))
  fs = waveFile.getframerate()
  return RetAR,fs   
