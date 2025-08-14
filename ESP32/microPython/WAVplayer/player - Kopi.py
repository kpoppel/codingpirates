## Code from : https://www.jarutex.com/index.php/2022/02/05/9596/
import time
import sys
from machine import DAC, Pin, freq
import gc
import _thread

gc.enable()
gc.collect()
freq(240000000)

dacPin1 = Pin(25) # Connect to speaker
dacPin2 = Pin(26) # Connect with adcPin1

dac1 = DAC( dacPin1 )
dac2 = DAC( dacPin2 )

BUF_SZ = 50000
buffer = [bytearray(BUF_SZ), bytearray(BUF_SZ)]
buffer_num = -1
sampleRate = 44100

def read_file(fName):
    wav_file = open(fName,"rb")
    mark = wav_file.read(4)
    if (mark != b'RIFF'):
        print("Not a RIFF WAV file.")
        wav_file.close()
        sys.exit(1)
    fileSize = int.from_bytes(wav_file.read(4),"little")
    print("File size = {} bytes".format(fileSize))
    fileType = wav_file.read(4)
    if (fileType != b'WAVE'):
        print("Not WAV content")
        wav_file.close()
        sys.exit(2)

    chunk = wav_file.read(4)
    lengthFormat = 0
    audioFormat = 0
    numChannels = 0
    global sampleRate
    byteRate = 0
    blockAlign = 0

    if (chunk == b'fmt '):
        lengthFormat = int.from_bytes(wav_file.read(4),"little")
        audioFormat = int.from_bytes(wav_file.read(2),"little") 
        numChannels = int.from_bytes(wav_file.read(2),"little")
        sampleRate = int.from_bytes(wav_file.read(4),"little")
        byteRate = int.from_bytes(wav_file.read(4),"little") 
        blockAlign = int.from_bytes(wav_file.read(2),"little") 
        bitsPerSample = int.from_bytes(wav_file.read(2),"little")
    
        print("Length of format data = {}".format(lengthFormat))
        print("Audio's format = {}".format(audioFormat))
        print("Number of channel(s) = {}".format(numChannels))
        print("Sample rate = {}".format(sampleRate))
        print("Byte rate = {}".format(byteRate))
        print("Block align = {}".format(blockAlign))
        print("Bits per sample = {}".format(bitsPerSample))
        if (audioFormat != 1):
            print("Audio format not PCM.")
            wav_file.close()
            sys.exit(3)
        
        chunk = wav_file.read(4)
        if (chunk == b'LIST'):
            print("Found LIST header")
            dataSize = int.from_bytes(wav_file.read(4),"little")
            print("Data size = {}".format(dataSize))
            chunk = wav_file.read(dataSize)
            
        chunk = wav_file.read(4)
        if (chunk != b'data'):
            print("data header not found in Wav file.")
            wav_file.close()
            sys.exit(5)
        print("Found data header")
        dataSize = int.from_bytes(wav_file.read(4),"little")
        print("Data size = {}".format(dataSize))

        # Read file into a buffer
        global BUF_SZ
        remainingData = dataSize
        readSize = BUF_SZ
        global buffer
        global buffer_ready
        while remainingData > 0:
            # Read part of the file
            wav_file.readinto(buffer, readSize)
            buffer_ready = False
            remainingData -= readSize
            if remainingData < readSize:
                readSize = remainingData
            if bitsPerSample > 8:
                #print(remainingData)
                # Convert 16 bit to 8 bit samples
                idx = 0
                for i in range(1, len(buffer), 2):  # (i=1, j=0; i<len; i+=2, j++):
                    buffer[idx] = (buffer[i] ^ 0x00000080)#.to_bytes(1, "little")
                    idx += 1
                #buffer = buffer[:25000]
                # Play
                # Repeat until file is done
                print(len(buffer))
            buffer_ready = True
        wav_file.close()

def play_wav(  ):
    global sampleRate
    global buffer_ready
    global buffer
    print(BUF_SZ, buffer_ready)
    while not buffer_ready:
        time.sleep_us(1000)
        
    tm = int(1000000/sampleRate)
    while True:
        print(BUF_SZ, buffer_ready)
        if buffer_ready:
               # play
            for i in range(BUF_SZ/2):
                dac1.write( buffer[i] )  
                time.sleep_us(tm)
                #print(buffer[i],end=";")
        else:
            time.sleep_us(tm)
    
    dac1.write( 0 )
    
############### main program
_thread.start_new_thread(play_wav, ())
read_file("/Hyper_pop_loop.wav")
#playWavFile("/Hyper_pop_loop.wav")
