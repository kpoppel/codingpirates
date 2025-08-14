# Her ser vi p� forskellige m�der at lave rytmer p�.
# Rytmer er faste m�nstre som et eller flere instrumenter
# spiller, og ellers gentager hen gennem et stykke musik.
# Meget ofte er det trommer, men ogs� bas og (rytme-)guitar kan
# egentlig spille de samme m�nstre hele venej gennem et nummer.
#
# Hvis du ikke har gennemf�rt �velserne 1-9, er det en rigtig
# god id� at g�re det f�rst.  Jeg introducerer en hel masse
# funktioner og m�der at skrive kode p�, som er nyttigt at kende
# f�rst.
use_debug false

# Nummer 10.
# Trommespor i �n l�kke
#
# Vi kan sagtens kode en rytme i bare en enkelt l�kke.
# Med l�kke mener jeg selvf�lgelig en "live_loop", eller
# "<n>.times" loop.  Forskellen p� de to er, at ".times"
# k�rer et bestemt antal gange, og kan v�re inde i et
# "live_loop", og et "live_loop" er ligesom en "for evigt" ting.
# N�r den n�r til enden, starter den bare forfra.
#
# Vi programmerer denne her rytme:
#    1 2 3 4 5 6 7 8 |...
# HH * * * * * * * *  ...
# SD         *        ...
# BD *       *        ...
# HH: High hat, SD: snare drum, BD: Bass drum
#
# Vi deler det hele op i 1/8-dele, som er den hurtigste node, nemlig HH
if 0 == 1
  16.times do
    # 1: HH + BD
    sample :drum_cymbal_closed, amp: 0.5
    sample :drum_bass_hard, finish: 0.15, rate: 0.7
    sleep 0.25
    # 2: HH
    sample :drum_cymbal_closed, amp: 0.5
    sleep 0.25
    # 3:
    sample :drum_cymbal_closed, amp: 0.5
    sleep 0.25
    # 4:
    sample :drum_cymbal_closed, amp: 0.5
    sleep 0.25
    # 5:
    sample :drum_cymbal_closed, amp: 0.5
    sample :drum_snare_hard, amp: 0.6
    sample :drum_bass_hard, finish: 0.15, rate: 0.7
    sleep 0.25
    # 6:
    sample :drum_cymbal_closed, amp: 0.5
    sleep 0.25
    # 7:
    sample :drum_cymbal_closed, amp: 0.5
    sleep 0.25
    # 8:
    sample :drum_cymbal_closed, amp: 0.5
    sleep 0.25
  end
  
  # Det er jo ikke s� sv�rt.  Skriv skemaet ned p� rytmen
  # og kod bare derudaf.  Det er rigtig fint hvis vi kun vil
  # spille den samme rytme hele vejen igennem stykket.
  # Vi kan selvf�lgelig lave mange flere af de her og spille dem
  # p� forskellige tidspunkter, men m�ske er der flere m�der?
end


# Nummer 11.
#  Tromme-spor med flere l�kker
#
#  Vi laver en tr�d til hvert instrument, og vil
# programmere den samme rytme som i 10.
#
# I stedet for at dele skemaet op i 1/8-dele og time alle
# instrumenterne sammen, s� tager vi os bare af et enkelt af gangen.
# High-hat spiller 16 gange, SD 2 gange, BD 4 gange.
# S� t�ller vi pauserne og ganger med den hurtugste node: 0.25
if 0 == 1
  in_thread do
    16.times do
      in_thread do
        16.times do  # Pr�v 32
          sample :drum_cymbal_closed, amp: 0.5
          sleep 0.25 # Pr�v 0.125
        end
      end
      in_thread do
        2.times do
          sleep 0.25 * 4 # Man ville jo nok bare skrive 1, ikke...
          sample :drum_snare_hard, amp: 0.6
          sleep 0.25 * 4
        end
      end
      4.times do
        sample :drum_bass_hard, finish: 0.15, rate: 0.7
        sleep 0.25 * 4
      end
    end
    # Koden fylder nogenlunde det samme som �velse 10.  Men hvis nu
    # vi skulle spille 1/16-dele, s� ville det her blive meget kortere:
    # Vi fordobler bare l�kken med HH og halverer sleep, og vi er f�rdige.
    # Pr�v det b�de med koden fra �velse 10, og denne her, og se forskellen.
    # L�kker er gode!
  end
  # Ok, det virker da meget godt.  3 lykker, det er da ok.
  # Men det er sv�rt at se hvordan slagene kommer i rytmen nu :-(
  # Kan vi lave noget, der b�de er rimelig kort, og som bedre viser rytmen
  # som kode?
end

# Nummer 12.
#  Trommespor som arrays
#
# Hvis vi bruger et array til at udtrykke rytmen, kan vi opstille
# den ligesom skemaet fra �velse 10.
#
if 0 == 1
  hh = [1,1,1,1,1,1,1,1]
  sd = [0,0,0,0,1,0,0,0]
  bd = [1,0,0,0,1,0,0,0]
  16.times do
    8.times do |idx|
      print hh.tick, sd.tick, bd.tick
      sample :drum_cymbal_closed, amp: 0.5 if hh[idx] == 1
      sample :drum_snare_hard, amp: 0.6 if sd[idx] == 1
      sample :drum_bass_hard, finish: 0.15, rate: 0.7 if bd[idx] == 1
      sleep 0.25
    end
  end
  # Koden er MEGET kortere nu, og vi kan oven i k�bet �ndre rytmen
  # rigtig simpelt.  Pr�v lige at g�re det, b�de her, og i de andre �velser.
  # Hvad er nu nemmest?
  #
  # Ulempen er, at hvis vi nu vil spille f.eks. HH dobbelt s� hurtigt,
  # skal l�kken skrives p� en lidt anden m�de.  Pr�v lige at g�re det.
  # Det er noget med in_thread og gentage HH-array dobbelt s� mange gange som nu.
  # Lidt tilbage til �velse 11, bare med et array.
  
  # Okay, indtil videre er rytmen bare den samme og samme.  Ret kedeligt. Der er
  # altid variation i musik, ellers er det ikke sp�ndende at h�re p�.
  # Hvordan g�r vi s� det?
end

# Nummer 13.
#   Trommespor med variation - med 2-dimensionelle arrays!!
#
# Variation betyder at vi skal spille flere forskellige skemaer for
# b�de HH, SD og BD.  Vi ved hvordan vi laver et 1-dimensionelt array, s�
# hvis vi nu bruger array som v�rdier i et array, har vi et 2-d array:
# arr2d = [ [1,2,3], [3,4,5] ]
# Vi finder v�rdier i et 2-d array: arr2d[0][1] == 2 er sandt.
#
# Lad os pr�ve det nu p� vores rytme.
if 1 == 1
  hh = [
    [1,1,1,1,1,1,1,1],
    [1,0,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1],
    [1,1,1,0,1,1,0,0],
  ]
  sd = [
    [0,0,0,0,1,0,0,0],
    [0,1,0,0,0,1,0,0],
    [0,0,1,0,1,1,0,0],
    [1,0,0,0,1,0,1,1],
  ]
  bd = [
    [1,0,0,0,1,0,0,0],
    [1,0,1,0,1,0,1,0],
    [0,1,0,0,0,1,0,0],
    [1,1,0,0,1,1,1,1],
  ]
  
  # Vi spiller samme antal takter som alle de andre, men nu er
  # der en masse variation.  Vi spiller variationerne efter hinanden
  # s� det er altid de samme ting vi h�rer.
  4.times do |variation|
    8.times do |idx|
      sample :drum_cymbal_closed, amp: 0.5 if hh[variation][idx] == 1
      sample :drum_snare_hard, amp: 0.6 if sd[variation][idx] == 1
      sample :drum_bass_hard, finish: 0.15, rate: 0.7 if bd[variation][idx] == 1
      sleep 0.25
    end
  end
  
  # Hvad nu hvis vi bruger tilf�ldige tal til at afg�re hvilken variation vi
  # spiller?  Det kan g�res s� alt er tilf�ldigt, eller hvis f.eks. SD og BD
  # h�rer sammen, kan vi bruge det samme tilf�ldige tal.
  4.times do
    variation = rrand_i(0,3) # l�ngden af vores array
    8.times do |idx|
      sample :drum_cymbal_closed, amp: 0.5 if hh[variation][idx] == 1
      sample :drum_snare_hard, amp: 0.6 if sd[variation][idx] == 1
      sample :drum_bass_hard, finish: 0.15, rate: 0.7 if bd[variation][idx] == 1
      sleep 0.25
    end
  end
  
  # Denne her udgave varierer alle tre instrumenter uafh�ngigt
  4.times do
    8.times do |idx|
      variation = rrand_i(0,3) # l�ngden af vores array
      sample :drum_cymbal_closed, amp: 0.5 if hh[variation][idx] == 1
      variation = rrand_i(0,3) # l�ngden af vores array
      sample :drum_snare_hard, amp: 0.6 if sd[variation][idx] == 1
      variation = rrand_i(0,3) # l�ngden af vores array
      sample :drum_bass_hard, finish: 0.15, rate: 0.7 if bd[variation][idx] == 1
      sleep 0.25
    end
  end
end
