#Importer nødvendige funktioner
import time
import tracks
from handle_screen import Screen
import HAL

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

#Hent tid som reference til ikke at "låse" systemet med sleep
base_time = time.time()
screen.start_update()

while True:        
    #Opdater liste til 4 linjer og scroll attribut på skærmen.
    # ["tekst på linje","True/False til om linjen må scrolles"]
    screen.lines=[
            [f"Track: {track_number+1}/{track_count}",False],
            [f"Time: {remaining_time}s",False],
            [f"Volume: {volume}", False],
            [track_name,True]
        ]

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

        