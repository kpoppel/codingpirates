in_thread do
  # Set instrument
  use_synth :piano
  
  # Verse
  3.times do
    play chord( :D5, :major)
    sleep 0.25
    play chord( :D5, :major)
    sleep 0.5
    play chord( :D5, :major)
    sleep 0.25
    
    play chord( :A, :major)
    sleep 0.5
    play chord( :A, :major)
    sleep 0.5
    
    play chord( :G, :major)
    sleep 0.5
    play chord( :G, :major)
    sleep 0.5
    
    play chord( :A, :major)
    sleep 1.0
  end
  
  8.times do
    play chord( :G, :major)
    sleep 0.25
  end
  
  8.times do
    play chord( :A, :major)
    sleep 0.25
  end
  
  play chord( :D5, :major)
end

######################
# Bass
in_thread do
  use_synth :prophet
  3.times do
    play :D2, release: 0.35, amp: 0.5
    sleep 0.25
    play :D2, release: 0.35, amp: 0.5
    sleep 0.5
    play :D2, release: 0.35, amp: 0.5
    sleep 0.25
    
    play :A2, release: 0.35, amp: 0.5
    sleep 0.5
    play :A2, release: 0.35, amp: 0.5
    sleep 0.5
    
    play :G2, release: 0.35, amp: 0.5
    sleep 0.5
    play :G2, release: 0.35, amp: 0.5
    sleep 0.5
    
    play :A2, release: 0.35, amp: 0.5
    sleep 1.0
  end
  
  8.times do
    play :G2, release: 0.35, amp: 0.5
    sleep 0.25
  end
  
  8.times do
    play :A2, release: 0.35, amp: 0.5
    sleep 0.25
  end
  
  play :D2, release: 0.35, amp: 0.5
  
end

in_thread do
  33.times do
    sample :drum_heavy_kick
    sleep 0.5
  end
end

in_thread do
  sleep 0.5
  16.times do
    sample :drum_snare_hard
    sleep 1
  end
end

in_thread do
  33.times do
    sample :drum_cymbal_closed
    sleep 0.25
    sample :drum_cymbal_pedal
    sleep 0.25
  end
end

in_thread do
  
  