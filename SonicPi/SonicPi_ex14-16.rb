# Hvis du ikke har gennemf�rt �velserne 1-13, er det en rigtig god id� at g�re det f�rst.
# Jeg bruger alle de ting der er gennemg�et tidligere, og forklarer dem ikke igen her.
#
# Nu er det tid til at s�tte noget musik sammen.  Vi kender til synths, samples, effekter
# og rytmer, og hvordan vi koder det hele.
#
#

# Nummer 14.
#  Grundrytme.
# Ethvert stykke musik indeholder en eller anden form for rytmeskema og vald af toneart osv.
# G� p� musikskolen for at blive rigtig klog p� det :-)
# Her koder vi, og s� er det bare hvad der lyder godt i vores �rer.
# Lad os starte med trommerne, fordi det er nemt og s�tter bunden i lydbilledet.
#
if 0 == 1
  # Vi tager et roligt tempo
  use_bpm 60
  
  # Hov, hvad er det nu for et rod med '2'? L�s koden l�ngere nede...
  hh = [
    [1,2,1,2,1,2,1,2],
    [1,2,1,2,1,2,1,2],
    [1,2,1,2,2,2,2,2],
    [1,2,1,1,1,2,2,2],
  ]
  sd = [
    [0,0,0,0,1,0,0,0],
    [0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,0,1],
  ]
  bd = [
    [1,0,0,0,1,0,0,0],
    [1,0,0,0,1,1,0,0],
    [1,0,0,0,1,1,1,1],
    [0,1,0,0,0,1,0,0],
  ]
  
  in_thread do
    4.times do
      8.times do |idx|
        # for at skabe enenu mere variation, kan vi bruge flere instrumenter af
        # samme slags, men med forskellig lyd i samme array.
        # Her har vi to forskellige lyde for high-hat
        variation = rrand_i(0,3) # l�ngden af vores array
        sample :drum_cymbal_pedal, amp: 0.5, attack: 0.1 if hh[variation][idx] == 1
        sample :drum_cymbal_closed, amp: 0.5 if hh[variation][idx] == 2
        variation = rrand_i(0,3) # l�ngden af vores array
        sample :drum_snare_hard, amp: 0.6 if sd[variation][idx] == 1
        variation = rrand_i(0,3) # l�ngden af vores array
        sample :drum_bass_hard, finish: 0.15, rate: 0.7 if bd[variation][idx] == 1
        sleep 0.25
      end
    end
  end
end

# Nummer 15.
#  Vi skal have noget bas. Masser af bas.
#
# Vi skal have noget mere i grundlyden, og en bas er altid fed at have.
#
# Her introducerer jeg funktioner, fordi vi med dem meget nemmere kan l�se hvordan
# det samlede musikstykke g�r, n�r de enkelte instrumenter ligesom tages uden for
# parentes og kan arbejdes med for sig selv.
#
# Vi f�r indtil videre to funktioner, en for trommerne, og en for bassen.
if 0 == 1
  # Vi tager et roligt tempo
  use_bpm 60
  
  define :drums do
    hh = [
      [1,2,1,2,1,2,1,2],
      [1,2,1,2,1,2,1,2],
      [1,2,1,2,2,2,2,2],
      [1,2,1,1,1,2,2,2],
    ]
    sd = [
      [0,0,0,0,1,0,0,0],
      [0,1,0,0,0,0,0,0],
      [0,0,0,0,0,1,0,0],
      [0,0,0,0,0,0,0,1],
    ]
    bd = [
      [1,0,0,0,1,0,0,0],
      [1,0,0,0,1,1,0,0],
      [1,0,0,0,1,1,1,1],
      [0,1,0,0,0,1,0,0],
    ]
    
    4.times do
      8.times do |idx|
        # for at skabe enenu mere variation, kan vi bruge flere instrumenter af
        # samme slags, men med forskellig lyd i samme array.
        # Her har vi to forskellige lyde for high-hat
        variation = rrand_i(0,3) # l�ngden af vores array
        sample :drum_cymbal_pedal, amp: 0.5, attack: 0.1 if hh[variation][idx] == 1
        sample :drum_cymbal_closed, amp: 0.5 if hh[variation][idx] == 2
        variation = rrand_i(0,3) # l�ngden af vores array
        sample :drum_snare_hard, amp: 0.6 if sd[variation][idx] == 1
        variation = rrand_i(0,3) # l�ngden af vores array
        sample :drum_bass_hard, finish: 0.15, rate: 0.7 if bd[variation][idx] == 1
        sleep 0.25
      end
    end
  end
  
  # Lad os bruge den nye funktion til trommerne:
  1.times do
    drums
  end
  
  # Ok, en ny en til bassen
  define :bassline do
    16.times do
      sample :bass_woodsy_c, finish: 0.16, rpitch: :E1 - :c0-24, amp: 0.3
      sleep 0.25+0.125
      sample :bass_woodsy_c, finish: 0.05, rpitch: :E1 - :c0-12, amp: 0.3
      sleep 0.125
    end
  end
  
  # Og den pr�ver vi ogs� lige:
  1.times do
    bassline
  end
  
  # Og s� s�tter vi dem sammen:
  1.times do
    sleep 4
    in_thread do
      drums
    end
    in_thread do
      bassline
    end
  end
  
  # Ok, vi har to funktioner, og er klar til at s�tte noget guitar p� til den
  # store finale.. n�sten.
end

# Nummer 16.
#  Vi tilf�jer noget guitarlyd.
#
# Der er nogle guitarsamples i Sonic Pi, men de er lidt lange, og vi skal
# have klippet lidt i en af dem.
if 0 == 1
  use_bpm 60
  
  # Her er grundlyden vi arbejder med
  if 1 == 1
    1.times do
      sample :guit_em9
      sleep 10
    end
  end
  
  # Den vil vi gerne have ned til bare lige at spille de f�rste toner af akkorden
  # Vi pr�ver forskellige v�rdier, indtil den rammer rigtigt.
  if 0 == 1
    1.times do
      # for lang
      sample :guit_em9, finish: 0.5
      sleep 5
      # for lang
      sample :guit_em9, finish: 0.25
      sleep 5
      # for kort?
      sample :guit_em9, finish: 0.125
      sleep 5
      # for lang
      sample :guit_em9, finish: 0.2
      sleep 5
      # lidt for lang
      sample :guit_em9, finish: 0.150
      sleep 5
      # perfekt!
      sample :guit_em9, finish: 0.147
      sleep 5
    end
  end
  
  # S� skal vi spille denne her akkord i forskellige toneh�jder
  # Det bliver lidt kedeligt at skulle spille den samme akkord
  # hele vejen gennem vores stykke...
  #
  # rpitch parameteren �ndrer p� rate og pitch s� det passer med
  # tonerne p� et klaver.  Det er smart, nu vi allerede ved akkorden
  # er en Em9, og den f�rste tone er alts� E.
  # Hvis vi nu kan tr�kke oktaver fra og l�gge til, kan vi spille
  # med det her sample ligesom vi �nsker.
  #
  # Brug lidt tid p� at forst� denne her del, det er meget nyttigt!
  if 0 == 1
    1.times do
      # Her er den samme lyd som f�r:
      sample :guit_em9, finish: 0.147
      sleep 2
      # Og her med rpitch - de lyder ens:
      sample :guit_em9, finish: 0.147, rpitch: :C0-:c0
      sleep 2
      # Vi kan ogs� overbevise os om at tonen er et E:
      use_synth :piano
      play :E3
      sample :guit_em9, finish: 0.147, rpitch: :C0-:c0
      sleep 2
      
      # S� g�r vi i gang med at spille toner:
      8.times do
        sample :guit_em9, finish: 0.147, rpitch: :E0-:c0
        sleep 1
        sample :guit_em9, finish: 0.147, rpitch: :A0-:c0
        sleep 1
        sample :guit_em9, finish: 0.147, rpitch: :G0-:c0
        sleep 1
      end
    end
  end
  
  # endelig er vi klar til at definere vores guitarlyd:
  define :guitar do
    with_fx :reverb, room: 0.7 do
      4.times do
        sample :guit_em9, finish: 0.147, rpitch: :e0-:c0
        sleep 2
        sample :guit_em9, finish: 0.147, rpitch: :G0-:c0
        sleep 1
        sample :guit_em9, finish: 0.147, rpitch: :G0-:c0
        sleep 1
      end
    end
  end
  
  # Og teste den:
  if 0 == 1
    1.times do
      guitar
    end
  end
  
end


#-------------------------------------
if 0 == 1
  use_bpm 60
  in_thread do
    32.times do
      sample :bass_woodsy_c, finish: 0.16, rpitch: :E1 - :c0-24, amp: 0.3
      sleep 0.25+0.125
      sample :bass_woodsy_c, finish: 0.05, rpitch: :E1 - :c0-12, amp: 0.3
      sleep 0.125
    end
  end
  in_thread do
    16.times do
      sample :drum_bass_hard, finish: 0.15, rate: 0.7
      sleep 1
    end
  end
  in_thread do
    with_fx :reverb, room: 1.0 do
      8.times do
        sleep 1
        sample :drum_snare_hard, amp: 0.6
        sleep 1
      end
    end
  end
  in_thread do
    with_fx :reverb, room: 0.7 do
      4.times do
        sample :guit_em9, finish: 0.147, rpitch: :e0-:c0
        sleep 2
        sample :guit_em9, finish: 0.147, rpitch: :G0-:c0
        sleep 1
        sample :guit_em9, finish: 0.147, rpitch: :G0-:c0
        sleep 1
      end
    end
  end
  
  64.times do
    with_fx :reverb, room: 0.4 do
      sample :drum_cymbal_closed, amp: 0.5
      sleep 0.25
    end
  end
end

#-----------------------------------------------------------