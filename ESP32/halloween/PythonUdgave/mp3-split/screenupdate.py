#Importer nødvendige moduler
import time
from hal import display

#Definer variable
Lines = [["",True],["",True],["",True],["",True]] # 4 tekst linjer med scroll aktiv
Picture = ""
Split = 40 # Hvor langt ude af x aksen på displayet skal teskst begynde

#Benyttes til at omdanne icon til pixels
def Icon():    
    for y, row in enumerate(Picture[2]):
        for x, c in enumerate(row):
            display.pixel(x+Picture[0], y+Picture[1], c)
  
#Opdaterer skærmen
def UpdateScreen():
        
    while True:
        LinesBackup = Lines # Benyttes til at afbryde loop, hvis der kommer ny tekst
        i = 0
        j=[] # liste til scroll tællere pr. linje

        # Indsæt 0 i j listen, en for hver linje (0-3)
        while i < len(Lines):
            j.append(0)
            i+=1

        #Opdater selve skærmen
        while True:
            i = 0
            display.fill(0) # clear skærm
            display.rotate(False) # rotering af skærm
            Icon() # indsæt icon pixels på skærm
            
            while i < len(Lines): # For hver linje
                # Hvis linjen er længere end der er plads til på skærmen og der må scrolles
                if (len((Lines[i][0])) > (128-Split)/8) and Lines[i][1]: 
                    display.text(Lines[i][0][j[i]:],Split,i*8,1) #Skriv linjen men fjern "j" antal karakterer fra starten af linjen
                    if (len(Lines[i][0]) - j[i] - (128-Split)/8) > 0: #Hvis der stadig  er bogstaver tilbage i linjen
                        j[i] += 1 # fjern et ekstra bogstav i næste runde
                    else:
                        j[i] = 0 # start linje [i] forfra
                else: # Linjen skal ikke scrolles elle der er plads og linjen skrives
                    display.text(Lines[i][0],Split,i*8,1)
                i += 1
            
            display.show()
            time.sleep_ms(250) 

            #Start forfra ved nyt valg
            if Lines != LinesBackup:
                break
            time.sleep_ms(250)

                


