import time
import sys
from machine import DAC, Pin, freq
import gc
import random
import _thread

# Garbage collector og MCU clock
gc.enable()
gc.collect()
freq(240000000)

# Opsætning af DAC
dacPin1 = Pin(25) # Connect to speaker
dac1 = DAC( dacPin1 )

class WavToDAC():
    BUF_SZ = 30000
    fileSize = 0
    sampleRate = 0
    dataSize = 0
    bitsPerSample = 0
    buffer = [bytearray(BUF_SZ), bytearray(BUF_SZ)]
    remainingData = 0
    
    def __init__(self, filename):
        self.file_handle = open("/Hyper_pop_loop.wav","rb")
        self.read_file_header()
        self.lock_0 = _thread.allocate_lock()  # The Lock instance
        self.lock_1 = _thread.allocate_lock()  # The Lock instance
        _thread.start_new_thread(self.to_dac, (self.lock_0, self.lock_1))
        _thread.start_new_thread(self.read_file, (self.lock_0, self.lock_1))
        
    def read_file_header(self):
        """
        Læs WAV filens headers og skriv noget information omkring filen.
        """
        mark = self.file_handle.read(4)
        if (mark != b'RIFF'):
            print("Not a RIFF WAV file.")
            self.file_handle.close()
            sys.exit(1)
        fileSize = int.from_bytes(self.file_handle.read(4),"little")
        print("File size = {} bytes".format(fileSize))
        fileType = self.file_handle.read(4)
        if (fileType != b'WAVE'):
            print("Not WAV content")
            self.file_handle.close()
            sys.exit(2)

        chunk = self.file_handle.read(4)
        lengthFormat = 0
        audioFormat = 0
        numChannels = 0
        self.sampleRate = 0
        byteRate = 0
        blockAlign = 0
        self.dataSize = 0
        self.bitsPerSample = 0

        if (chunk == b'fmt '):
            lengthFormat = int.from_bytes(self.file_handle.read(4),"little")
            audioFormat = int.from_bytes(self.file_handle.read(2),"little") 
            numChannels = int.from_bytes(self.file_handle.read(2),"little")
            self.sampleRate = int.from_bytes(self.file_handle.read(4),"little")
            byteRate = int.from_bytes(self.file_handle.read(4),"little") 
            blockAlign = int.from_bytes(self.file_handle.read(2),"little") 
            self.bitsPerSample = int.from_bytes(self.file_handle.read(2),"little")
        
            print(f"Length of format data = {lengthFormat}")
            print(f"Audio's format = {audioFormat}")
            print(f"Number of channel(s) = {numChannels}")
            print(f"Sample rate = {self.sampleRate}")
            print(f"Byte rate = {byteRate}")
            print(f"Block align = {blockAlign}")
            print(f"Bits per sample = {self.bitsPerSample}")
            if (audioFormat != 1):
                print("Audio format not PCM.")
                self.file_handle.close()
                sys.exit(3)
            
            chunk = self.file_handle.read(4)
            if (chunk == b'LIST'):
                print("Found LIST header")
                self.dataSize = int.from_bytes(self.file_handle.read(4),"little")
                print(f"Data size = {self.dataSize}")
                chunk = self.file_handle.read(self.dataSize)
                
            chunk = self.file_handle.read(4)
            if (chunk != b'data'):
                print("data header not found in Wav file.")
                self.file_handle.close()
                sys.exit(5)
            print("Found data header")
            self.dataSize = int.from_bytes(self.file_handle.read(4),"little")
            print(f"Data size = {self.dataSize}")
            self.remainingData = self.dataSize

    def run_forever(self):
        print("Running forever")
        while True:
            await asyncio.sleep(10)

    def to_dac(self, lock_0, lock_1):
        print("DAC")
        time.sleep_ms(5)
        tm = int(1000000/self.sampleRate)
        while self.remainingData > 0:
            lock_0.acquire()
            print("td_l0")
            for i in range(self.BUF_SZ):
                dac1.write(self.buffer[0][i])
                time.sleep_us(tm)
            lock_0.release()

            time.sleep_ms(1)
            lock_1.acquire()
            print("td_l1")
            for i in range(self.BUF_SZ):
                dac1.write(self.buffer[1][i])
                time.sleep_us(tm)
            lock_1.release()
            time.sleep_ms(1)
            
        dac1.write( 0 )
 
    
    def read_file(self, lock_0, lock_1):
        while self.remainingData > 0:
            lock_0.acquire()
            print("rf_l0")
            for i in range(self.BUF_SZ):
                self.buffer[0][i] = random.randint(0,255)
            lock_0.release()

            time.sleep_ms(1)
            lock_1.acquire()
            print("rf_l1")
            for i in range(self.BUF_SZ):
                self.buffer[1][i] = random.randint(0,32)
            lock_1.release()
            time.sleep_ms(1)
            
    

def read_file(file_handle):
    """
    Læs data fra filen ind i skiftevis buffer[0] og buffer[1]
    """
    # Read file into a buffer
    global BUF_SZ
    global buffer
    global ready_buffer_num
    global playing_buffer_num
    global dataSize
    remainingData = 10000#dataSize
    readSize = BUF_SZ

    ready_buffer_num =  10000
    load_buffer = 0
    while remainingData > 0:
        print(remainingData, playing_buffer_num, ready_buffer_num)
        if playing_buffer_num != ready_buffer_num:
            # Read part of the file
            self.file_handle.readinto(buffer[load_buffer], readSize)
            remainingData -= readSize
            if remainingData < readSize:
                readSize = remainingData
            if bitsPerSample > 8:
                # Convert 16 bit to 8 bit samples
                idx = 0
                for i in range(1, len(buffer), 2):
                    buffer[load_buffer][idx] = (buffer[load_buffer][i] ^ 0x00000080)
                    idx += 1
            # Repeat until file is done
            ready_buffer_num = (ready_buffer_num + 1) % 2
            load_buffer = (ready_buffer_num + 1) % 2
            print("Buffer ready", ready_buffer_num, load_buffer)
        else:
            time.sleep_ms(1)
        #print(ready_buffer_num, playing_buffer_num, end="-")
        #print(buffer[load_buffer])
    ready_buffer_num = -1


    
############### main program
def main(filename):
    w2d = WavToDAC(filename)
    #w2d.run_forever()

main("/Hyper_pop_loop.wav")
#try:
#    asyncio.run(main("/Hyper_pop_loop.wav"))
#finally:
#    asyncio.new_event_loop()  # Clear retained state
    
# Tråden venter på en klar buffer of spiller den.
#self.file_handle = open("/Hyper_pop_loop.wav","rb")
#read_file_header(self.file_handle)
#_thread.start_new_thread(play_wav, ())
#ready_buffer_num = 100
#read_file(self.file_handle)
#self.file_handle.close()
