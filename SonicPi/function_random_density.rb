# functions and density loops

# This is a function.  Parameter "d".
define :hats do |d|
  density d do
    sample :drum_cymbal_closed
    sleep 1
  end
end

live_loop :hats do
  # run through the ring one by one.
  #hats (ring, 4, 4, 4, 6, 4, 8, 4, 12).tick
  
  #  Randomly choose one of the values:
  hats (ring, 4, 4, 4, 4, 6, 6, 8, 8, 12).choose
end


