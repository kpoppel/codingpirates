#Importer nødvendige funktioner
import network, ntptime
import time
import tracks
from handle_screen import Screen
import HAL

# Constants
ONE_HOUR = 3600

# Initialise modules
hal = HAL.HAL()
screen = Screen(hal.display, "icons.json")
tracks = tracks.Tracks("sdcard.json")

# MP# player state variables
track_count=hal.music.filesinfolder()
volume = hal.music.volume(1)
track_number = 0
track_name = tracks.get_track_name(track_number)
remaining_time = tracks.get_track_length(track_number)
is_playing = False

# Hvis alarm_start_time er sat, spilles der musik på denne tid hver dag.
alarm_hours = 0 # 0 til 24 timer (0 er slukket)
alarm_start_time = 0
alarm_track_number = 0
alarm_volume = 0

#Hent tid som reference til ikke at "låse" systemet med sleep
base_time = time.time()
screen.start_update()

while True:        
    #Opdater liste til 4 linjer og scroll attribut på skærmen.
    # ["tekst på linje","True/False til om linjen må scrolles"]
    screen.lines=[
            [f"Track: {track_number+1}/{track_count}",False],
            [f"Time: {remaining_time}s",False],
            [f"Vol: {volume}", False],
            [track_name,True]
        ]
    if alarm_hours > 0:
        screen.lines[2] = [f"Vol: {volume} ({alarm_hours}t)", False]

    # Mode select
    if not hal.button_1():
        if screen.current_icon == "pirat":
            screen.current_icon = "speaker"
        elif screen.current_icon == "speaker":
            screen.current_icon = "node"
        elif screen.current_icon == "node":
            if is_playing == True:
                screen.current_icon = "start"
            else:
                screen.current_icon = "stop"
        elif screen.current_icon in ("start", "stop"):
            screen.current_icon = "alarm"
        elif screen.current_icon == "alarm":
            # exit action
            alarm_start_time = 0 if alarm_hours==0 else time.time()
            screen.current_icon = "pirat"
        else:
            # Should never get here!
            screen.current_icon = "pirat"
            
        #print(f"{screen.current_icon}")
        time.sleep_ms(250)

    if not hal.button_2():
        # value button changes values within a given state
        # (Button closest to the corner)
        
        # Select Song state
        if screen.current_icon == 'node':
            track_number = (track_number + 1) % track_count
            track_name = tracks.get_track_name(track_number)
            remaining_time = tracks.get_track_length(track_number)
            time.sleep_ms(250)
        # Set volume state
        elif screen.current_icon == 'speaker':
            volume = (hal.music.volume() + 1) % 31
            hal.music.volume(volume)
        # Start Stop states
        elif screen.current_icon == 'stop':
            is_playing = True
            screen.current_icon = "start"
            hal.music.play(track_number+1)
            time.sleep_ms(250)
        elif screen.current_icon == 'start':
            is_playing = False
            screen.current_icon = "stop"
            hal.music.stop()
            time.sleep_ms(250)
        # Set the alarm
        elif screen.current_icon == 'alarm':
            alarm_hours = (alarm_hours+1) % 25
            alarm_track_number = track_number
            alarm_volume = volume
            time.sleep_ms(250)

    # Denne blok regner på alarmen hvis den er aktiv.
    if alarm_start_time > 0 and time.time() - alarm_start_time >= alarm_hours*ONE_HOUR:
        print(f"Alarm elapsed {time.time()-alarm_start_time} >= {alarm_hours*ONE_HOUR}")
        track_number = alarm_track_number
        track_name = tracks.get_track_name(track_number)
        remaining_time = tracks.get_track_length(track_number)
        volume = alarm_volume
        hal.music.volume(alarm_volume)
        hal.music.play(track_number+1)
        alarm_start_time = time.time()
        base_time = time.time()
        screen.current_icon = "start"
        is_playing = True
        
    # Denne blok skifter nummer og opdaterer resterende tid i displayet
    if time.time() - tracks.get_track_length(track_number) > base_time:
        # Play next track when the current one is done
        if not hal.music.is_playing() and is_playing:
            track_number = (track_number + 1) % track_count
            track_name = tracks.get_track_name(track_number)
            remaining_time = tracks.get_track_length(track_number)
            hal.music.play(track_number+1)
        
        # Set new base time
        base_time = time.time()
    elif is_playing == True:
        remaining_time = tracks.get_track_length(track_number) - (time.time() - base_time)
        if remaining_time < 0:
            remaining_time = 0
        time.sleep_ms(250)
        
    # Så vi ikke overloader processoren        
    time.sleep_ms(1)