#Importer nødvendige moduler
import time
import json
import _thread

class Screen:
    def __init__(self, display, iconfilename):
        self.display = display

        # internal variables
        self.lines = [["",True],["",True],["",True],["",True]] # 4 tekst linjer med scroll aktiv
        self.current_icon = "pirat"
        self.extra_icons = ["speaker_small", "alarm_small", "playlist_small", "node_small"]
        # Hvor langt ude af x aksen på displayet skal tekst begynde
        self.split = 48
        # Load icons
        try:
            f = open(iconfilename)
            self.icons = json.load(f)
            f.close()
        except:
            self.icons = None
            
        # Make a list of icon names.
        # Names are in order of insertion from Python 3.7+.
        self.icon_names = list(self.icons.keys())
    
    def icon(self, icon):
        """ Render an icon. """
        x_ofs = self.icons[icon][0]
        y_ofs = self.icons[icon][1]
        pixels = self.icons[icon][2]
        for y, row in enumerate(pixels):
            for x, data in enumerate(row):
                c = 1 if data=="1" else 0
                self.display.pixel(x+x_ofs, y+y_ofs, c)
    
    def update(self):
        """  Update the screen when called.
        """            
        while True:
            LinesBackup = self.lines # Benyttes til at afbryde loop, hvis der kommer ny tekst
            i = 0
            j=[] # liste til scroll tællere pr. linje

            # Indsæt 0 i j listen, en for hver linje (0-3)
            while i < len(self.lines):
                j.append(0)
                i+=1

            #Opdater selve skærmen
            while True:
                i = 0
                self.display.fill(0) # clear skærm
                self.icon(self.current_icon) # indsæt icon pixels på skærm
                for icon in self.extra_icons:
                    self.icon(icon)
                
                while i < len(self.lines): # For hver linje
                    # If the line is a scoll line and it is longer than the screen width
                    if self.lines[i][1] and (len((self.lines[i][0])) > (128-self.split)/8): 
                        #Skriv linjen men fjern "j" antal karakterer fra starten af linjen
                        self.display.text(self.lines[i][0][j[i]:],self.split,i*8,1)
                        #Hvis der stadig  er bogstaver tilbage i linjen
                        if (len(self.lines[i][0]) - j[i] - (128-self.split)/8) > 0:
                            j[i] += 1 # fjern et ekstra bogstav i næste runde
                        else:
                            j[i] = 0 # start linje [i] forfra
                    else:
                        # Linjen skal ikke scrolles eller der er plads og linjen skrives
                        self.display.text(self.lines[i][0],self.split,i*8,1)
                    i += 1
                
                self.display.show()
                time.sleep_ms(250) 

                #Start forfra ved nyt valg
                if self.lines != LinesBackup:
                    break

    def start_update(self):
        # Start screen update thread
        _thread.start_new_thread(self.update, ())

