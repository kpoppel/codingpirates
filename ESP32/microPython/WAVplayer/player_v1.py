## Code from : https://www.jarutex.com/index.php/2022/02/05/9596/
import time
import sys
from machine import DAC, Pin, freq
import gc

gc.enable()
gc.collect()
freq(240000000)

dacPin1 = Pin(25) # Connect to speaker
dacPin2 = Pin(26) # Connect with adcPin1

dac1 = DAC( dacPin1 )
dac2 = DAC( dacPin2 )

def playWavFile( fName ):
    monoFile = open(fName,"rb")
    mark = monoFile.read(4)
    if (mark != b'RIFF'):
        print("Don't use WAV!")
        monoFile.close()
        sys.exit(1)
    fileSize = int.from_bytes(monoFile.read(4),"little")
    print("File size = {} bytes".format(fileSize))
    fileType = monoFile.read(4)
    if (fileType != b'WAVE'):
        print("ไDon't use WAV!!")
        monoFile.close()
        sys.exit(2)

    chunk = monoFile.read(4)
    lengthFormat = 0
    audioFormat = 0
    numChannels = 0
    sampleRate = 0
    byteRate = 0
    blockAlign = 0

    if (chunk == b'fmt '):
        lengthFormat = int.from_bytes(monoFile.read(4),"little")
        audioFormat = int.from_bytes(monoFile.read(2),"little") 
        numChannels = int.from_bytes(monoFile.read(2),"little")
        sampleRate = int.from_bytes(monoFile.read(4),"little")
        byteRate = int.from_bytes(monoFile.read(4),"little") 
        blockAlign = int.from_bytes(monoFile.read(2),"little") 
        bitsPerSample = int.from_bytes(monoFile.read(2),"little")
    
        print("Length of format data = {}".format(lengthFormat))
        print("Audio's format = {}".format(audioFormat))
        print("Number of channel(s) = {}".format(numChannels))
        print("Sample rate = {}".format(sampleRate))
        print("Byte rate = {}".format(byteRate))
        print("Block align = {}".format(blockAlign))
        print("Bits per sample = {}".format(bitsPerSample))
        
        minValue = 255
        maxValue = 0
    
        chunk = monoFile.read(4)
        if (chunk == b'LIST'):
            print("Found LIST header")
            dataSize = int.from_bytes(monoFile.read(4),"little")
            print("Data size = {}".format(dataSize))
            chunk = monoFile.read(dataSize)
            
        chunk = monoFile.read(4)
        if (chunk != b'data'):
            print("Don't use WAV!!!!")
            monoFile.close()
            sys.exit(5)
        print("Found data header")
        dataSize = int.from_bytes(monoFile.read(4),"little")
        print("Data size = {}".format(dataSize))

        # Ready for some playing!
        remainingData = dataSize
        BUF_SZ = 100000
        buffer = bytearray(BUF_SZ)
        readSize = BUF_SZ
        while remainingData > 0:
            if bitsPerSample > 8:
                # Read part of the file
                monoFile.readinto(buffer, readSize)
                remainingData -= readSize
                if remainingData < readSize:
                    readSize = remainingData
                     
                #print(remainingData)
                # Convert 16 bit to 8 bit samples
                idx = 0
                for i in range(1, len(buffer), 2):  # (i=1, j=0; i<len; i+=2, j++):
                    buffer[idx] = (buffer[i] ^ 0x00000080)#.to_bytes(1, "little")
                    idx += 1
                #buffer = buffer[:25000]
                # Play
                # Repeat until file is done
                #print(len(buffer))
            
            # play
            tm = int(1000000/sampleRate)
            for i in range(BUF_SZ/2):
                data = buffer[i]
                dac1.write( data )  
                time.sleep_us(tm)
            #print("---------------------------")
            #del buffer
        
        if (audioFormat != 1):
            print("Not supported in cases where PCM is not used!!!")
            monoFile.close()
            sys.exit(3)
        monoFile.close()
        dac1.write( 0 )
    
############### main program
playWavFile("/Hyper_pop_loop.wav")
