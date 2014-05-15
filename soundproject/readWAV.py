import wave, struct
from numpy import array                    

def readWAV(fileN):
  waveFile = wave.open(fileN, 'r')   
  length = waveFile.getnframes()
  outdata = []

  for i in range(0, length):
    waveData = waveFile.readframes(1)

    try:
      data = struct.unpack('<h', waveData)
      outdata.append(data[0])
    except:
      raise

  return array(outdata)
