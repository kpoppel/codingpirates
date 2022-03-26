# Density function plays the number of
# times specifies within one beat.

density 3 do
  sample :bd_haus
  sleep 1
end

density 7 do
  sample :bd_haus
  sleep 1
end

use_synth :pluck

# Now a live loop using density and a
# ring array(?) to give the density function
# various values per beat.
live_loop :dense do
  density (ring, 4, 4, 6, 8).tick do
    # The scale uses the notes of a chord
    # to play individual tones within
    # the chord.
    play scale( :e3, :major_pentatonic).choose
    sleep 1
  end
end

live_loop :metronome, sync: :dense do
  sample :bd_klub
  sleep 1
end
