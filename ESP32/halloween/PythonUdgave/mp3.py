from dfplayermini import Player

from time import sleep

music = Player(pin_TX=25, pin_RX=26)

print("Files on SD card")
number_of_files = music.filesinfolder()
print(number_of_files)

print("Current volume")
volume = music.volume()
print(volume)

print("Set volume")
music.volume(12)

print("Start play")
music.play(1)
sleep(2)

print("Stop playback")
music.stop()
sleep(2)

print("Fadeout")
music.play(1)
music.fade(10000, to=0)
sleep(12)

print("Fadein")
music.fade(10000, to=10)
sleep(12)

print("Play next")
music.play_next()
sleep(10)

print("Play previous")
music.play_prev()
sleep(10)

print("Pause playback")
music.pause()
sleep(3)

print("Resume playback")
music.play()
sleep(3)

print("Play loop (needs short sample)")
music.loop()
music.play(2)
sleep(20)

### The module commands seem to bring the module into a dead zone
### where no more UART commands will be received.
#print("Set module in sleep mode (save power)")
#music.module_sleep()
#print(f"Expect -1 from querying volume: %d", music.volume())
#sleep(2)

#print("Wakeup module from sleep mode")
#music.module_wake()
#print(f"Expect 10 from querying volume: %d", music.volume())
#sleep(2)

print("Play some more...")
music.play(3)
