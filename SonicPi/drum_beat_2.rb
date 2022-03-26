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


use_bpm 98

live_loop :drums do
  # Run through variations one by one:
  #5.times do |outer|
  ## Remember the end at the end.
  
  # Run through variatins randomly:
  outer = rand_i(5)
  16.times do |idx|
    sample :drum_heavy_kick if drum[outer][idx] == 1
    sample :drum_snare_hard if drum[outer][idx] == 2
    sample :drum_cymbal_closed, amp: 0.3 if cymb[outer][idx] == 1
    sample :drum_cymbal_pedal, amp: 0.3, attack: 0.1 if cymb[outer][idx] == 2
    sleep 0.25
  end
  #end
end

