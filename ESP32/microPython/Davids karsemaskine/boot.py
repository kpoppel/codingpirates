from machine import freq
from HAL import HAL
from Wifi import Wifi
import ntptime, time

freq(80000000) # fix af periodisk brug af for meget strøm ved opstart af wifi

hal = HAL()

wifi=Wifi('Wifi.json')
ntptime.host= 'dk.pool.ntp.org' #vælg dansk NTP server
display=hal.display

#On/Off tidspunkter for de tre leds
GRON = [
    ['18:35','00:35'],
    ['06:35','12:35']
    ]

ROD = [
    ['00:35','06:35'],
    ['12:35','18:35']
    ]

BLA = [
    ['06:35','12:35'],
    ['18:35','00:35']
    ]

#Match On/off med led(gpio)
Leds = [[GRON,hal.gron],[ROD,hal.rod],[BLA,hal.bla]]

#Fiks tidszone
def cettime():
    year = time.localtime()[0]       #get current year
    HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),2,0,0,0,0,0)) #Time of March change to CEST
    HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),3,0,0,0,0,0)) #Time of October change to CET
    now=time.time()
    if now < HHMarch :               # we are before last sunday of march
        cet=time.localtime(now+3600) # CET:  UTC+1H
    elif now < HHOctober :           # we are before last sunday of october
        cet=time.localtime(now+7200) # CEST: UTC+2H
    else:                            # we are after last sunday of october
        cet=time.localtime(now+3600) # CET:  UTC+1H
    return(cet)

def SetTime():
    print("Local time before synchronization：%s" %str(time.localtime())) #vis tid før ntp
    ntptime.settime()
    print("Local time after synchronization：%s" %str(time.localtime())) #vis tid efter ntp

#vis dato, dag og klokke på display
def ShowTime():
    #now = time.localtime()
    now=cettime()
    day = ['MANDAG', 'TIRSDAG', 'ONSDAG', 'TORSDAG', 'FREDAG', 'L0RDAG', 'S0NDAG']
    print("Date: {} {}/{}-{}".format(day[now[6]], now[2], now[1], now[0]))
    print("Time: {:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5]))
    display.fill(0)
    display.text("Ugedag: {}".format(day[now[6]]), 0, 0, 1)
    display.text("Klokke: {:02d}:{:02d}:{:02d}".format(now[3], now[4], now[5]),0,8,1)      
    display.text("Dato  : {}/{}-{}".format(now[2], now[1], str(now[0])[2:]), 0, 16, 1)
    display.show()

# rutine til at tænde og slukke led
def LedOnOff():
    now=cettime()
    c = 0
    while c < len(Leds):
        for l in Leds:
            for t in l[0]:
                TimeStart=t[0].split(':')
                TimeSlut=t[1].split(':')
                if ((TimeStart[0]==str(now[3])) and (TimeStart[1]==str(now[4])) and (now[5]==0)):
                    print ('time ok')
                    l[1].on()
                if ((TimeSlut[0]==str(now[3])) and (TimeSlut[1]==str(now[4])) and (now[5]==0)):
                    print ('time off')
                    l[1].off()
        c+=1
        

while True:
    SetTime()
    cnt= 0
    while cnt < 600:
        cnt +=1
        ShowTime()
        LedOnOff()
        time.sleep(1)
    
    