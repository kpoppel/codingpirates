use_synth :tb303
use_debug false

play_intro = 0
play_space_scan = 1
play_melody = 1
play_drums = 1

define :clean_chord do |tone, ch, num|
  use_synth :mod_pulse
  #use_synth :piano
  density num do
    play chord(tone, ch), release: 0.5, cutoff: rrand(60, 120), wave: 1, amp: rrand(0.1,0.8)
    sleep 1
  end
end

define :mychord do |tone, ch, repeats|
  use_synth :prophet
  #use_synth :piano
  repeats.times do
    play choose(chord(tone, ch)), release: 0.2, cutoff: rrand(60, 120), wave: 1, amp: rrand(0.1,0.8)
    sleep 0.125
  end
end

define :dopdop do
  use_synth :saw
  32.times do
    n = (ring :e1, :e2, :e3).tick
    play n, release: 0.125, cutoff: rrand(70, 130), res: 0.9, wave: 1, amp: rrand(0.1,0.8)
    sleep 0.125
  end
end


with_fx :reverb, room: 0.8 do
  if play_space_scan == 1
    live_loop :space_scanner do
      with_fx :slicer, phase: 0.25, amp: 0.5 do
        co = (line 70, 130, steps: 8).tick
        play :e1, cutoff: co, release: 7, attack: 1, cutoff_attack: 4, cutoff_release: 4
        sleep 8
      end
    end
  end
  
  if play_intro == 1
    sample :ambi_sauna
    sample :loop_3d_printer
    sleep 3
    sample :loop_weirdo
    sleep 3
  end
  live_loop :squelch1 do
    dopdop
  end
  
  
  if play_melody == 1
    live_loop :squelch do
      use_random_seed 3000
      #mychord :E3, :m9, 32
      #mychord :G3, :m9, 16
      #mychord :A3, :m9, 16
      dopdop
      2.times do
        mychord :E3, :minor, 32
        mychord :G3, :minor, 16
        mychord :A3, :minor, 16
      end
      
      2.times do
        clean_chord :E3, :minor, 1
        clean_chord :E3, :minor, 1
        clean_chord :E3, :minor, 3
        clean_chord :F3, :minor, 1
        clean_chord :F3, :minor, 1
        clean_chord :F3, :minor, 3
      end
      clean_chord :C4, :minor, 1
      clean_chord :C4, :minor, 1
      clean_chord :C4, :minor, 2
      clean_chord :B3, :minor, 1
      clean_chord :B3, :minor, 1
      clean_chord :B3, :minor, 2
      clean_chord :C4, :minor, 1
      clean_chord :C4, :minor, 1
      clean_chord :C4, :minor, 2
      clean_chord :D4, :minor, 1
      clean_chord :D4, :minor, 1
      clean_chord :D4, :minor, 2
    end
  end
end



drum = [
  [1,0,0,0, 2,0,0,0, 1,0,0,0, 2,0,0,0],
  [1,1,1,1, 2,0,0,0, 1,0,0,0, 2,0,0,0],
  [1,0,0,0, 2,1,1,1, 1,0,0,0, 2,0,0,0],
  [1,0,0,0, 2,0,0,0, 1,1,1,1, 2,0,0,0],
  [1,0,0,0, 2,0,0,0, 1,2,1,1, 2,0,0,0]
]

cymb = [
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,1,2],
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,1,2],
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,1,2],
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,1,2],
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,1,2]
]


use_bpm 120
if play_intro == 1
  live_loop :drums do
    # Run through variations one by one:
    #5.times do |outer|
    ## Remember the end at the end.
    
    # Run through variations randomly:
    outer = rand_i(5)
    16.times do |idx|
      sample :bd_haus, cutoff: 80, rate: 0.6, amp: 2 if drum[outer][idx] == 1
      #sample :elec_snare, rate: 2 if drum[outer][idx] == 2
      sample :drum_snare_hard, rate: 2.5 if drum[outer][idx] == 2
      sample :drum_cymbal_closed, amp: 0.3 if cymb[outer][idx] == 1
      sample :drum_cymbal_pedal, amp: 0.3, attack: 0.1 if cymb[outer][idx] == 2
      #sample :elec_cymbal
      sleep 0.25
    end
    #end
  end
end

#live_loop :lunar, sync: :drums do
#  sample :ambi_lunar_land, rate: 1
#  sleep rrand(8, 10)
#end

define :bd do |d|
  density d do
    sample :bd_haus, cutoff: 80
    sleep 1
  end
end

#live_loop :bd_loop do
# run through the ring one by one.
#bd (ring, 4, 4, 4, 6, 4, 8, 4, 12).tick

#  Randomly choose one of the values:
#bd (ring, 1, 1, 0.5, 0.5, 3, 3, 0.5, 0.25, 0.3).choose
#  bd (ring, 0.5, 1, 0.25, 1, 3).choose
#end
