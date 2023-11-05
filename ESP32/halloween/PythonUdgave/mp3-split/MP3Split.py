#Importer nødvendige funktioner
import time, icon, _thread, screenupdate
from sange import Tracks
from hal import *

#Definer variable
TrackNumber = 1
Play = False
time.sleep(1)
TrackCount=music.filesinfolder()
Volume = music.volume()
TrackName = "Unknown"

#Indæst ikoner fra icon.py i en liste
Icons = (icon.Pirat, icon.Node, icon.Select, icon.StartStop, icon.Speaker)

# Sæt start icon
Picture = Icons[0]

#opdater screenupdate med icon
screenupdate.Picture = Picture
          
#Afspil det valgte nummer og opdater display med Node for at spille.
def PlayTrack(PlayTrack=1):
    global TrackNumber
    global Picture
    TrackNumber = PlayTrack
    Picture = icon.Node
    music.play(TrackNumber)

#Sætter volume
def VolumeSet():
    vol = music.volume()
    if vol < 30:
        vol += 1
    else:
        vol=0
    music.volume(vol)
    return (vol)

#Valg af nummer
def SongSelect():
    global TrackNumber

    if TrackNumber < TrackCount:
        TrackNumber += 1
    else:
        TrackNumber = 1

#Start eller stop afspilning. 
def SetStartStop(Play):
    
    if not Play: # Hvis der ikke afspilles så start afspilning
        Play = True
        PlayTrack(TrackNumber)
    else: #ellers stop afspilning
        Play = False
        music.stop()
    return(Play)

# Definer 4 linjer til skærm
screenupdate.Lines=[
    ["Tracks: " + str(TrackCount),False],
    ["Track#: " + str(TrackNumber),False],
    ["Volume: " + str(Volume),False],
    [TrackName,False]
    ]

# Definer hvor skærmen skal splittes mellem icon og tekst
screenupdate.Split=40

#START SKÆRM som tråd
_thread.start_new_thread(screenupdate.UpdateScreen, ())


IconCount = 0
#Hent tid som reference til ikke at "låse" systemet med sleep
BaseTime = time.time()

while True:
    #TrackName hentes fra Tracks listen i sange.py
    TrackName = Tracks[TrackNumber -1]
    
    #Opdater icon på skærmen
    screenupdate.Picture = Picture
    
    #Opdater liste til 4 linjer og scroll attribut på skærmen. ["tekst på linje","True/False til om linjen må scrolles"]
    screenupdate.Lines=[
        ["Tracks: " + str(TrackCount),False],
        ["Track#: " + str(TrackNumber),False],
        ["Volume: " + str(Volume),False],
        [TrackName,True]
        ]
    if not SelectBTN(): # Hvis der trykkes på Select knappen
        IconCount += 1
        time.sleep_ms(250)
        if IconCount == len(Icons):
            IconCount = 0
        Picture = Icons[IconCount]

    if not ValueBTN(): # Hvis der trykkes på Value knappen
        # Select Song
        if IconCount == 2: #Hvis IconCount = 2 er det sang valg
            SongSelect()
            time.sleep_ms(250)

        # Start Stop
        if IconCount == 3: #Hvis IconCount = 3 er det start stop af musik
            Play = SetStartStop(Play)

        # Set volume
        if IconCount == 4: #Hvis IconCount = 4 er det volume valg
            Volume = VolumeSet()

    if time.time() - 10 > BaseTime: # hvis der er gået mere end 10 sekunder siden BaseTime blev sat.
        #Der kontrolleres om der skal spilles musik og hvor vidt der spilles.
        #Næste nummer startes hvis der skal spilles og der ikke spilles
        if not music.is_playing() and Play:
            if TrackNumber < TrackCount:
                TrackNumber += 1
            else:
                TrackNumber = 1
            PlayTrack(TrackNumber)
        
        #BaseTime resettes
        BaseTime = time.time()
        


