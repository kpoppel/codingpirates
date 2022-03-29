use_synth :tb303
use_debug false

play_fx = 0
play_space_scan = 0
play_melody = 0
play_drums = 0
play_drum_bridge = 0
play_dopdop = 0

live_loop :coordinator do
  play_fx = 1
  sleep 2
  play_fx = 2
  sleep 8
  play_dopdop = 1
  play_space_scan = 1
  sleep 16
  play_melody = 1
  sleep 18
  play_drums = 1
  8.times do
    sleep 14
    play_drums = 0
    play_drum_bridge = rrand_i(1,3)
    sleep 2
    play_drum_bridge = 0
    play_drums = 1
    sleep 4
    play_fx = rrand_i(0,2)
  end
  play_dopdop = 0
  play_space_scan = 0
  play_melody = 0
  play_drums = 0
  play_fx = 3
  sleep 10
end


define :clean_chord do |tone, ch, num|
  #use_synth :mod_pulse
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
    play choose(chord(tone, ch)), release: 0.2, cutoff: rrand(60, 120), amp: rrand(0.1,0.8)
    sleep 0.125
  end
end

define :dopdop do
  use_synth :saw
  32.times do
    n = (ring :e1, :e2, :e3).tick
    play n, release: 0.125, cutoff: rrand(70, 130), amp: rrand(0.1,0.8)
    sleep 0.125
  end
end

live_loop :fx do
  case play_fx
  when 1
    play_fx = 0
    sample :vinyl_rewind
  when 2
    play_fx = 0
    sample :ambi_sauna
    sample :loop_3d_printer
    sleep 3
    sample :loop_weirdo
    sleep 2
  when 3
    play_fx = 0
    sample :vinyl_rewind, rate: -1
  end
  sleep 1
end


with_fx :reverb, room: 0.8 do
  live_loop :space_scanner do
    if play_space_scan == 1
      with_fx :slicer, phase: 0.25, amp: 0.5 do
        co = (line 70, 130, steps: 8).tick
        play :e1, cutoff: co, release: 7, attack: 1, cutoff_attack: 4, cutoff_release: 4
      end
    end
    sleep 8
  end
  
  
  live_loop :squelch1 do
    if play_dopdop == 1
      dopdop
    else
      sleep 1
    end
  end
  
  
  
  #sleep 32
  use_random_seed 3000
  live_loop :squelch do
    if play_melody == 1
      #mychord :E3, :m9, 32
      #mychord :G3, :m9, 16
      #mychord :A3, :m9, 16
      #dopdop
      2.times do
        mychord :E3, :minor, 32
        mychord :G3, :minor, 16
        mychord :A3, :minor, 16
        #mychord :C3, :minor, 32
        #mychord :G3, :minor, 16
        #mychord :C4, :minor, 16
      end
      #mychord :G3, :minor, 16
      #mychord :C4, :minor, 16
      #mychord :F4, :minor, 16
      #mychord :E4, :minor, 16
      #mychord :D4, :minor, 16
      #mychord :C5, :minor, 16
      #mychord :G4, :minor, 16
      #mychord :G4, :minor, 16
      #mychord :F4, :minor, 16
      #mychord :E4, :minor, 16
      #mychord :D4, :minor, 16
      #mychord :E4, :minor, 16
      
      #mychord :C3, :minor, 16
      #mychord :G3, :minor, 16
      #mychord :A3, :minor, 16
      
      #clean_chord :D3, :minor, 1
      #clean_chord :G3, :minor, 1
      #clean_chord :A3, :minor, 1
      #clean_chord :C3, :minor, 1
      #clean_chord :G3, :minor, 1
      #clean_chord :A3, :minor, 1
      #play_pattern_timed [:c2, :g2, :c3, :ds3], [0.5/3], release: 0.5, phase: 0.25
      
      #      2.times do
      #        clean_chord :E3, :minor, 1
      #        clean_chord :E3, :minor, 1
      #        clean_chord :E3, :minor, 3
      #        clean_chord :F3, :minor, 1
      #        clean_chord :F3, :minor, 1
      #        clean_chord :F3, :minor, 3
      #      end
      #      clean_chord :C4, :minor, 1
      #      clean_chord :C4, :minor, 1
      #      clean_chord :C4, :minor, 2
      #      clean_chord :B3, :minor, 1
      #      clean_chord :B3, :minor, 1
      #      clean_chord :B3, :minor, 2
      #      clean_chord :C4, :minor, 1
      #      clean_chord :C4, :minor, 1
      #      clean_chord :C4, :minor, 2
      #      clean_chord :D4, :minor, 1
      #      clean_chord :D4, :minor, 1
      #      clean_chord :D4, :minor, 2
      #      print rrand_i(0, 10)
      #      if rrand_i(0, 10) > 6
      #        play_drums = 0
      #      else
      #        play_drums = 1
      #      end
      #      print play_drums
      
      #      print play_intro
      #      case play_intro
      #      when 0
      #        play_intro = 1
      #      when 1
      #        play_intro = 2
      #      when 2
      #        play_intro = 0
      #      end
      #      print play_intro
      #    end
    else
      sleep 4
    end
  end
end

drum = [
  [1,0,0,0, 2,0,0,0, 1,0,0,0, 2,0,0,0],
  [1,1,1,1, 2,0,0,0, 1,0,0,0, 2,0,0,0],
  [1,0,0,0, 2,1,1,1, 1,0,0,0, 2,0,0,0],
  [1,0,0,0, 2,0,0,0, 1,1,1,1, 2,0,0,0],
  [1,0,0,0, 2,0,0,0, 1,2,1,1, 2,0,0,0],
  [0,1,0,1, 2,1,0,0, 1,1,1,1, 2,2,2,2]
]

cymb = [
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,1,2],
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,1,2],
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,3,0],
  [1,2,1,2, 1,2,1,2, 1,2,1,2, 1,2,3,0],
  [1,2,1,1, 2,1,2,2, 1,2,1,1, 2,1,2,2],
  [1,1,1,1, 2,2,2,2, 1,1,1,1, 2,2,2,2]
]

live_loop :drums do
  if play_drums == 1
    use_bpm 120
    # Run through variations one by one:
    #5.times do |outer|
    ## Remember the end at the end.
    
    # Run through variations randomly:
    outer = rand_i(6)
    16.times do |idx|
      sample :bd_haus, cutoff: 80, rate: 0.6, amp: 2 if drum[outer][idx] == 1
      #sample :elec_snare, rate: 2 if drum[outer][idx] == 2
      sample :drum_snare_hard, rate: 2.5 if drum[outer][idx] == 2
      sample :drum_cymbal_closed, amp: 0.3 if cymb[outer][idx] == 1
      sample :drum_cymbal_pedal, amp: 0.3, attack: 0.1 if cymb[outer][idx] == 2
      sample :drum_cymbal_hard, amp: 0.3, attack: 0.1, release: 4 if cymb[outer][idx] == 3
      #sample :elec_cymbal
      sleep 0.25
    end
    #end
  else
    sleep 1
  end
end

define :drum_snap do
  snap = 0.03
  sample :drum_snare_hard, rate: 2.5
  sleep snap
  sample :drum_snare_hard, rate: 2.4
  sleep 1.0/4-snap
end

live_loop :drum_bridge, sync: :drums do
  use_bpm 120
  case play_drum_bridge
  when 1
    8. times do
      sample :bd_haus, rate: 1
      sleep 1.0/4
    end
    8.times do
      sample :drum_snare_hard, rate: 2.5
      sleep 1.0/4
    end
  when 2
    2.times do
      2. times do
        sample :bd_haus, rate: 1
        sleep 1.0/4
      end
      drum_snap
      sample :bd_haus, rate: 1
      sleep 1.0/4
      drum_snap
      drum_snap
    end
    2. times do
      sample :bd_haus, rate: 1
      sleep 1.0/4
    end
    sleep 0.5
  when 3
    3.times do
      sample :drum_snare_hard, rate: 2.5
      sleep 1.0/4
    end
    sleep 1.0/4
    sample :drum_snare_hard, rate: 2.5
    sleep 1.0/2
    sample :drum_snare_hard, rate: 2.5
    sleep 1.0/4
    sample :drum_snare_hard, rate: 2.5
    sleep 1.0/2
    sample :bd_haus, rate: 1
    sleep 1.0/4
    2.times do
      sample :drum_tom_hi_hard, rate: 0.8
      sleep 1.0/4
    end
    2.times do
      sample :drum_tom_mid_hard, rate: 0.8
      sleep 1.0/4
    end
    2.times do
      sample :drum_tom_lo_hard, rate: 0.8
      sleep 1.0/4
    end
    
  else
    sleep 1
  end
end

#live_loop :fietsen do
#  sleep 0.25
#  sample :guit_em9, rate: -1
#  sleep 7.75
#end

#live_loop :lunar, sync: :drums do
#  sample :ambi_lunar_land, rate: 1
#  sleep rrand(8, 10)
#end

#define :bd do |d|
#  density d do
#    sample :bd_haus, cutoff: 80
#    sleep 1
#  end
#end

#live_loop :bd_loop do
# run through the ring one by one.
#bd (ring, 4, 4, 4, 6, 4, 8, 4, 12).tick

#  Randomly choose one of the values:
#bd (ring, 1, 1, 0.5, 0.5, 3, 3, 0.5, 0.25, 0.3).choose
#  bd (ring, 0.5, 1, 0.25, 1, 3).choose
#end
