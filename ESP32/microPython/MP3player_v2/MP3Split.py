#Importer nødvendige funktioner
import time
from TrackManager import TrackManager
from handle_screen import Screen
import HAL

# Initialise modules
hal = HAL.HAL()
screen = Screen(hal.display, "icons.json")
player = TrackManager(hal.music, "sdcard.json")
volume = hal.music.volume(1)

# MP3 player state variables
# Her ser vi hvordan man kan ignorere returnerede værdier:
(_, _, _, remaining_time) = player.select_next_track()
# Alternativt kunne man også bare kalde funktionen og så køre:
#remaining_time = player.current_track_length

playlist_names = player.get_playlist_names()
playlist_index = playlist_names.index(player.current_playlist)
start_time = 0
is_playing = False

# Hvis alarm_start_time er sat, spilles der musik på denne tid hver dag.
alarm_hours = 0 # 0 til 24 timer (0 er slukket)
alarm_start_time = 0
alarm_track_folder = 0
alarm_track_number = 0
alarm_volume = 0
# Playliste
current_playlist = None

# Start screen update
screen.start_update()

while True:        
    #Opdater liste til 4 linjer og scroll attribut på skærmen.
    # ["tekst på linje","True/False til om linjen må scrolles"]
    screen.lines=[
            [player.current_track_name,True],
            [f"{player.current_playlist}/{player.current_track_folder}/{player.current_track_number}", True],
            [f"{remaining_time}s",False],
            [f"{volume}", False]
        ]
    if alarm_hours > 0:
        screen.lines[3] = [f"{volume} ({alarm_hours}t)", False]

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
            screen.current_icon = "playlist"
        elif screen.current_icon == "playlist":
            screen.current_icon = "alarm"
        elif screen.current_icon == "alarm":
            # exit action
            alarm_start_time = 0 if alarm_hours==0 else time.time()
            screen.current_icon = "pirat"
        else:
            # Should never get here!
            screen.current_icon = "pirat"
        time.sleep_ms(250)

    if not hal.button_2():
        # value button changes values within a given state
        
        # Select Song state
        if screen.current_icon == 'node':
            (_, _, _, remaining_time) = player.select_next_track()
            time.sleep_ms(250)
        # Set volume state
        elif screen.current_icon == 'speaker':
            volume = (hal.music.volume() + 1) % 31
            hal.music.volume(volume)
        # Start playing music
        elif screen.current_icon == 'stop':
            hal.music.volume(volume)
            player.play()
            start_time = time.time()
            screen.current_icon = "start"
            is_playing = True
            time.sleep_ms(250)
        # Stop playing music
        elif screen.current_icon == 'start':
            hal.music.stop()
            screen.current_icon = "stop"
            is_playing = False
            time.sleep_ms(250)
        # Select a playlist
        elif screen.current_icon == 'playlist':
            playlist_index = (playlist_index+1) % len(playlist_names)
            player.select_playlist(playlist_names[playlist_index])
            time.sleep_ms(250)
        # Set the alarm
        elif screen.current_icon == 'alarm':
            alarm_hours = (alarm_hours+1) % 25
            alarm_track_number = player.current_track_number
            alarm_track_folder = player.current_track_folder
            alarm_playlist = player.current_playlist
            alarm_volume = volume
            time.sleep_ms(250)

    # Denne blok regner på alarmen hvis den er aktiv.
    if alarm_start_time > 0 and time.time() - alarm_start_time >= alarm_hours*3600:
        #print(f"Alarm elapsed {time.time()-alarm_start_time} >= {ONE_DAY}")
        alarm_start_time = time.time()
        player.select_playlist(alarm_playlist)
        (_, _, _, remaining_time) = player.select_track(alarm_track_folder, alarm_track_number)
        hal.music.volume(alarm_volume)
        start_time = time.time()
        player.play()
        screen.current_icon = "start"
        is_playing = True
        
    # Denne blok skifter nummer og opdaterer resterende tid i displayet.
    if is_playing == True:
        elapsed_time = time.time() - start_time
        if elapsed_time > player.current_track_length and not hal.music.is_playing():
            # Play next track when the current one is done and MP3 player is done too
            # (we could have wrong JSON data)
            (_, _, _, remaining_time) = player.select_next_track()
            player.play()
        
            # Set new base time
            start_time = time.time()
        else:
            remaining_time = player.current_track_length - elapsed_time
            if remaining_time < 0:
                remaining_time = 0
        time.sleep_ms(250)
    # Så vi ikke overloader processoren
    time.sleep_ms(1)

