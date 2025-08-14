# Drum beat using arrays

bd = [1,0,0,0,1,0,1,0,0,1,0,0,1,0,0,0]
sd = [0,0,1,0,0,0,1,0,0,0,1,0,0,1,1,0]
hh = [0,1,1,2,1,1,2,0,1,0,1,0,1,0,1,0]

use_bpm 80

live_loop :drum1 do
  16.times do |idx|
    sample :bd_haus if bd[idx] == 1
    sample :drum_snare_hard if sd[idx] == 1
    case hh[idx]
    when 1
      sample :drum_cymbal_closed
    when 2
      sample :drum_cymbal_pedal
    end
    
    sleep 0.25
  end
end

