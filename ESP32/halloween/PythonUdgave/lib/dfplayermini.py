import utime, time
from machine import UART, Timer

class Player:
    MAX_VOLUME = 30
    
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
        """ Play a track.
            track_id: If specified, play this track number (1-2999)
            If not specified playback from last selected. After reset this is 0.
            Track 0 is the same as track 1.  A track number larger than the number
            of tracks on the SD card will play the last track.
        """
        if track_id is None:
            self.cmd(0x0D)
        elif isinstance(track_id, int):
            self.cmd(0x03, track_id >> 8, track_id & 0xFF)
    
    def play_next(self):
        """ Play next track
        """
        self.cmd(0x01)
        
    def play_prev(self):
        """ Play previous track
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
    
    def filesinfolder(self):
        return self.query(0x48)
