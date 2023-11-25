##
## C library for inspiration found here:
## https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299
import utime, time
from machine import UART, Timer

class Player:
    MAX_VOLUME = 30
    EQ_NORMAL = 0
    EQ_POP = 1
    EQ_ROCK = 2
    EQ_JAZZ = 3
    EQ_CLASSIC = 4
    EQ_BASS = 5
    PLAY_MODE_REPEAT = 0
    PLAY_MODE_FOLDER_REPEAT = 1
    PLAY_MODE_SINGLE_REPEAT = 2
    PLAY_MODE_RANDOM = 3
    
    def __init__(self, pin_TX, pin_RX):
        self.uart = UART(1, 9600, tx=pin_TX, rx=pin_RX)
        self.cmd(0x3F)  # send initialization parametres
        self._fadeout_timer = Timer(-1)

        # Device resets at volume 30 - we init for 10
        self._volume = 10
        self._fade_reset_volume = self._volume
        self._fade_to_volume = 0
        self.volume(self._volume)

    def cmd(self, command, para1=0, para2=0):
        """
        The module communication protocol always has this sequence:
          $S VER Len CMD Feedback para1 para2 sumh suml $O
          
          $S = 0x7E
          VER = version information (0xFF in all the examples)
          Len = numberof bytes after Len
          CMD = command byte
          Feedback = 0x00: no feedback, 0x01: need feedback
          para1 = query high byte
          para2 = query low byte
          sumh,suml = 2 Byte accumulation and verification not including $S
          $O = 0xEF
          
          The device can handle ignoring the checksum and just sending the stop byte.
          So that is what we do.
        """
        query = bytes([0x7E, 0xFF, 0x06, command,
                       0x00, para1, para2,
                       0xEF])
        print(query)
        self.uart.write(query)
        time.sleep_ms(200)

    def query(self, command, para1=0, para2=0):
        """
        Query the module
        """
        retry=True
        while (retry):
            self.uart.flush()
            self.cmd(command, para1, para2)
            time.sleep_ms(200)
            in_bytes = self.uart.read()
            if not in_bytes: #timeout
                return -1
            if len(in_bytes)==10 and in_bytes[1]==255 and in_bytes[9]==239:
                retry=False
        return in_bytes[6]
    
    # playback
    def play(self, track_id=None):
        """ Play a track from the filesystem root or anywhere it seems.
            track_id: integer [1, 3000]
            If not specified playback from last selected. After reset this is 0.
            Track 0 is the same as track 1.  A track number larger than the number
            of tracks on the SD card will play the last track.
            Note: files must be named 0001something.mp3 or .wav
            Note: play a track numbered larger than one in the root folder
                  just picks the next one from the folders.
            """
        if track_id is None:
            # Just start play
            self.cmd(0x0D)
        elif isinstance(track_id, int):
            # Play specific track based on name
            self.cmd(0x03, track_id >> 8, track_id & 0xFF)
    
    def play_folder(self, folder_id, track_id):
        """ Play file from a folder.
            folder_id: integer [1, 99]
            track_id: integer [1, 255]
            Note: files must be named 01/001something.mp3 or .wav
        """
        self.cmd(0x0F, folder_id & 0xFF, track_id & 0xFF)

    def play_large_folder(self, folder_id, track_id):
        """ Play file from folders supporting 3000 tracks.
            If using folders with upto 3000 tracks, only folder ids
            from 01 to 15 are allowed: 4 bit folder id, 12 bit track id
            folder_id: integer [1, 15]
            track_id: integer [1, 3000]
        """
        self.cmd(0x14, (folder_id & 0xF << 4) + (track_id >> 8 & 0xF), track_id & 0xFF)

    def play_mp3(self, track_id):
        """ Play file from MP3 folder.
            track_id: integer [1, 3000]
            Note: files must be named MP3/0001something.mp3 or .wav
        """
        self.cmd(0x12, track_id >> 8, track_id & 0xFF)
        
    def play_advert(self, track_id):
        """ Play file from ADVERT folder.
            This will play the track in the middle of an already playing one
            then return to the original playback.
            track_id: integer [1, 3000]
            Note: files must be named ADVERT/0001something.mp3 or .wav
        """
        self.cmd(0x13, track_id >> 8, track_id & 0xFF)
        
    def play_next(self):
        """ Play next track
            Not limited to root or stays within a folder
        """
        self.cmd(0x01)
        
    def play_prev(self):
        """ Play previous track.
            Not limited to root or stays within a folder
        """
        self.cmd(0x02)
    
    def pause(self):
        """ Pause playing
        """
        self.cmd(0x0E)

    def stop(self):
        """ Stop playing
        """
        self.cmd(0x16)

    def equaliser(self, mode=None):
        """
        Set equaliser mode.
        Use the EQ_* values in the class.
        None queries the module for the current setting.
        """
        if mode is None:
            return self.query(0x44)
        else:
            self.cmd(0x07, 0x00, mode)
            return mode
        
    def playback_mode(self, mode=None):
        """
        Playback mode can be one of the modes from the PLAY_MODE_* constants.
        None queries the module for the current setting.
        """
        if mode is None:
            return self.query(0x45)
        else:
            self.cmd(0x08, 0x00, mode)
            return mode
        
    def fade(self, fade_ms=3000, to=0, reset=False):
        """
        Adjust the volume from the current level to 'to' value over fade_ms.
        Pause playback when volume reaches 'to' value.
        If 'reset' is True, volume will be reset to the original value, otherwise
        stay at the 'to' value.
        """
        # Set volume end value
        self._fade_to_volume = to
        # Set volume reset value
        if reset:
            self._fade_reset_volume = self._volume
        else:
            self._fade_reset_volume = to

        # Start timer at intervals
        fade_ms_per_step = int(fade_ms / abs(self._volume - to))
        self._fadeout_timer.init(
            period=fade_ms_per_step,
            callback=self._fade_process)

    def _fade_process(self, timer):
        """
        Timer callback.  Every time it is called we can adjust the volume by 1 step.
        """
        if self._volume < self._fade_to_volume:
            self.volume_up()
        elif self._volume > self._fade_to_volume:
            self.volume_down()
        else:
            self._fadeout_timer.deinit()
            # If the current volume and reset volume is not equal reset was True.
            # In this case we pause the music and reset the volume.  Else just go on.
            if self._volume != self._fade_reset_volume:
                self.pause()
                self.volume(self._fade_reset_volume)
            #print("fadeout finished")

    def loop_track(self, track_id):
        self.cmd(0x08, track_id >> 8, track_id & 0xFF)

    def loop(self):
        self.cmd(0x19)

    def loop_disable(self):
        self.cmd(0x19, 0x00, 0x01)

    def is_playing(self):
        """
        Query the moduse for playback status.
        It will return 1 if playing, 0 or 2 otherwise.
        This function returns a boolean.
        """
        if self.query(0x42) == 1:
            return True
        else:
            return False

    def is_paused(self):
        """
        Query the moduse for playback status.
        It will return 2 if paused, 0 or 1 otherwise.
        This function returns a boolean.
        """
        if self.query(0x42) == 2:
            return True
        else:
            return False

    # volume control

    def volume_up(self):
        self._volume += 1
        self.cmd(0x04)

    def volume_down(self):
        self._volume -= 1
        self.cmd(0x05)

    def volume(self, volume=None):
        """ Set or query volume.
            volume: None or 0-30
            If not specified the device is queried for volume setting.
        """
        if volume is None:
            self._volume = self.query(0x43)
        else:
            self._volume = int(sorted([0, volume, self.MAX_VOLUME])[1])
            #print("volume", self._volume)
            self.cmd(0x06, 0x00, self._volume)
        
        return self._volume

    # hardware

    def module_sleep(self):
        self.cmd(0x0A)

    def module_wake(self):
        self.cmd(0x0B)

    def module_reset(self):
        self.cmd(0x0C)
        
    # file handling
    def filesinfolder(self, folder_id=None):
        if isinstance(folder_id, int):
            # Query number of tracks in a specific folder
            print("Sorry, filesin folder with folder name does not seem to return correct data.")
            return self.query(0x4E, folder_id >> 8, folder_id & 0xFF)
        else:
            return self.query(0x48)

    def folders(self):
        """ Return the number of folders on device """
        return self.query(0x4F)