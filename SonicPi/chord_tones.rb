define :dopdop do
  # Prøv forskellige synthesizers
  use_synth :beep
  use_synth :blade
  use_synth :bnoise
  use_synth :chipbass
  use_synth :chiplead
  use_synth :chipnoise
  use_synth :cnoise
  use_synth :dark_ambience
  use_synth :piano
  use_synth :tri
  use_synth :prophet
  use_synth :hoover
  use_synth :saw
  32.times do
    # Prøv forskellige toner:
    n = (ring :e1, :e2, :e3).tick
    #n = (ring :e1, :g1, :a1).tick
    #n = chord( :e1, :major7).tick
    play n, release: 0.125, cutoff: rrand(70, 130), amp: rrand(0.1,0.8)
    sleep 0.125
  end
end

live_loop :hi do
  dopdop
end
