# Lyde 1
#  synth og sample
#
# Synth er en syntetisk lyd, som de synthesizere laver.  De består
# af sinus, sawtak, firkant og støj.
#
# Tutorial i SonicPi og her: https://guides.codingpirates.dk/lectures/10
#
# Online keyboard og trommemaskine:
#  Trommemaskine: https://drumbit.app/
#  Synthesizer  : https://www.webaudiomodules.org/wamsynths/obxd
#  Klaver       : https://virtualpiano.net/
#  Klaver mv.   : https://www.musicca.com/piano
#
# Også nyttigt:
#  https://sonic-pi.mehackit.org/exercises/en/09-keys-chords-and-scales/01-piano.html
#
# Øvelserne skal tastes ind selv for at få træning i keyboard og
# gøre det nemmere at huske de forskellige kommandoer.
# Og så skal man uhske at ændre alle tal til noget andet og se hvad der sker!

################################################################################


# Nummer 1:
# Udtryk tonen som et tal eller som en nodeværdi:
#  60 61 62 63 64 65 66 67 68 69 70 71
#   C C#  D D#  E  F F#  G G#  A A#  B
#
# Ret if-sætningen så sammenligningen bliver sand, så spiller lydene
if 0 == 1
  sleep_time = 1
  play 60
  sleep sleep_time
  play :C
  sleep sleep_time
  play 61
  sleep sleep_time
  play :Cs
  sleep sleep_time
  play 62
  sleep sleep_time
  play :D
  sleep sleep_time
  play 63
  sleep sleep_time
  play :Ds
  sleep sleep_time
  play 64
  sleep sleep_time
  play :E
  sleep sleep_time
  play 65
  sleep sleep_time
  play :F
  sleep sleep_time
  play 66
  sleep sleep_time
  play :Fs
  sleep sleep_time
  play 67
  sleep sleep_time
  play :G
  sleep sleep_time
  play 68
  sleep sleep_time
  play :Gs
  sleep sleep_time
  play 69
  sleep sleep_time
  play :A
  sleep sleep_time
  play 70
  sleep sleep_time
  play :As
  sleep sleep_time
  play 71
  sleep sleep_time
  play :B
  sleep sleep_time
end

# Nummer 2.
#  Nu kender vi tonerne.  Vi kan også spille alle muilge lyde ind i mellem.
#  Lad os også afprøve at sætte de her tal tilfældigt på forskellig måde.
#  rrand_i(<fra>, <til>) giver et heltal
#  rrand(<fra>, <til>) giver et decimaltal
#
#  Prøv denne her:
if 0 == 1
  # Gentag 16 gange:
  16.times do
    # Spil tonen "60" + et tilfældigt decimaltal mellem 0 og 3.14:
    play 60 + rrand(0.0, 3.14)
    sleep 0.5
  end
  16.times do
    # Spil tonen "60" + et tilfældigt heltal mellem 60 og 71:
    play rrand_i(60, 71)
    sleep 0.5
  end
end

# Nummer 3.
#  Kan vi skrive tonerne i en melodi lidt mere kompakt?
#  Svaret er "arrays" (eller lister)
#
#  Vi bruger også
#   use_synth <lyd> - som giver os forskellige lyde at bruge
#   use_bpm <antal slag per minut> - som sætter en hastighed for musikken.
#      Det smarte er, at "sleep 1" er et taktslag, og så kan vi justere
#      hvor mange takeslag per sekund vi vil have med use_bpm
#   :<node><oktav>, såsom :C4 - tallet bag noden angiver hvilken oktav
#      på et instrument vi bruger.  Det svarer til at lægge 12 til hvis vi
#      bruger tallene.  :C = :C4 = 60, og :C5 = 72, :C3 = 48 osv.
#      Det betyder heller ikke noget om vi bruger store eller små bogstaver
#      I musik bruger man dog altid store bogstaver.
#   :r (:rest) - Her spiller vi ikke noget i et slag.  Det er altså en pause.
#
# Prøv denne her:
if 0 == 1
  use_synth :piano
  use_bpm 100
  melodi = [:C, :C, :C, :D, :E, :E, :E, :r, :D, :D4, :D4, :E4, :C4, :r, :C4, :r]
  play_pattern melodi
  # Kan vi spille den en oktav højere?
  melodi = [:C5, :C5, :C5, :D5, :E5, :E5, :E5, :r, :D5, :D5, :D5, :E5, :C5, :r, :C5, :r]
  play_pattern melodi
  # ... og to oktaver lavere?
  melodi = [:C2, :c2, :C2, :d2, :E2, :e2, :E2, :r, :d2, :D2, :d2, :E2, :c2, :r, :C2, :r]
  play_pattern melodi
  use_synth :beep
end

# Nummer 4.
#  Lad os tilføje en akkord.  En akkord er bare nogle tomer der spilles
#  på samme tid.  Så er der akkorder der lyder godt sammen, og derfor
#  går man på musikskole.  Her leger vi bare med det vi synes lyder fedt.

if 0 == 1
  # Tre måder at lave den samme akkord på:
  #
  # Bare spil tonerne på samme tid:
  play :C
  play :E
  play :G
  sleep 1
  # Brug en kommando til at spille en liste:
  play_chord [:C, :E, :G]
  sleep 1
  # Spil akkorden ved at bruge musik-notation for akkorder:
  play chord(:C, :major)
  sleep 1
  play_chord chord(:C, :major)
  sleep 1
  # play chord() og play_chord cord() gør det samme.  Bare brug den korte form.
end

# Nummer 5.
#  Lad os sætte melodi og akkorder sammen.
#  Hvad hvis vi bruger arrays til det formål?
#
#  Vi lærer også noget omkring "sekventiel" og "parallel" afspilning.
#  in_thread - en funtion der starter not, og fortsætter til næste linje
#     med det samme.
if 0 == 1
  use_bpm 100
  melodi = [:C, :C, :C, :D, :E, :E, :E, :r,
            :D, :D, :D, :E, :C, :r, :C, :r]
  akkord = [chord(:C3, :major), :r, :r, :r, chord(:C3, :major), :r, :r, :r,
            chord(:G3, :major), :r, :r, :r, chord(:C3, :major), :r, :r, :r]
  play_pattern melodi
  play_pattern akkord
  
  # Ok et problem her.  Melodien spiller først, og så spiller akkorderne.
  # Programmet kører jo en linje af gangen, så hvodan får vi det til at
  # vide vi vil spille noget samtidig?
  # Svaret er "in_thread".  Funktionen starter alt det der er mellem do-end
  # som en sekvens.  Men den fortsætter ogsåmed det samme til næste linje,
  # så nu kan vi spille de to play_pattern samtidig.
  #
  # Et andet tip:  Vi kan skifte instrument per linje.  Prøv nogle forskellige.
  in_thread do
    use_synth :fm
    play_pattern melodi
  end
  use_synth :prophet
  play_pattern akkord
  
  # Nu har vi den første linje af "Lille Peter Edderkop", med akkorder og
  # forskellige instrumenter.
end

# Nummer 6.
#  Tuning af synths.
#  Kan vi lave en lyd kortere længere, kraftigere og svagere mens den spiller?
#  Ja det er kan vi godt.  Det hedder ADSR : Attack, Decay, Sustain, Release
#
#  Attack : Hvor hurtigt og hvor kraftigt starter lyden
#  Decay  : Hvor lang tid og til hvilket niveau falder lydens attack af
#  Sustain: Hvor lang tid spiller lyden efter Decay
#  Release: Hvor lang tid fader lyden væk
#
#  Vi bruger også:
#   <.choose> - lister kan fungere på forskellige måder. <liste>.choose vælger et tilfældigt
#           element i en liste.  Prøv også med ".pick", ".ring"
#   <.pick(<tal>)>  - Vælg et tilfældigt antal elementer.  Elementet kan vælges flere gange.
#   <.tick> - Vælger elementerne i en liste i rækkefølge.
#
# Prøv noget forskelligt - gå amok!
if 0 == 1
  # Prøv forskellige synths
  use_synth :beep
  
  # Denne her lyd spiller i 1 + 1 + 1 + 3 = 6 slag.
  play 60, attack: 1, attack_level: 2, decay: 1, decay_level: 2, sustain: 1, sustain_level: 2, release: 3
  sleep 6
  
  # Dene her lyd spiller i 0.1 + 0.1 + 0.1 + 0.3 = 0.6 slag.
  play 60, attack: 0.1, attack_level: 1, decay: 0.1, decay_level: 0.4, sustain: 0.1, sustain_level: 5, release: 0.3
  sleep 1
  
  # Lad os spille nogle tilfældige toner.
  32.times do
    # Prøv at ændre værdierne og se hvad der sker.  Prøv at sætte nogle til 0, eller noget småt eller stort!
    a = rrand(0, 0.1) # 0
    d = rrand(0, 0.3) # 0
    s = rrand(0, 0.5)
    r = rrand(0, 0.3) # 0.1
    tone = chord(:E3, :major).choose # .pick(2), .tick, .choose
    play tone, attack: a, attack_level: 1, decay: d, decay_level: 1, sustain: s, sustain_level: 1, release: r
    sleep a+d+s+r
  end
  
  # Og hvad med denne her:
  use_synth :saw
  32.times do
    n = (ring :c1, :c2, :c3).tick
    play n, release: 0.125
    sleep 0.125
  end
  
end

# Nummer 7.
# Nu hvor vi ved hvordan ADSR virker, og kan forme en lyd som vi vil have den, kan vi måske
# få vores melodi til at spille lidt bedre?
#
# Se også i hjælpen under "Synths", hvilke andre paramtere der kan leges med.
# :fm har f.eks. "divisor" og "depth" som ser spændende ud.

if 0 == 1
  use_bpm 100
  melodi = [:C, :C, :C, :D, :E, :E, :E, :r,
            :D, :D, :D, :E, :C, :r, :C, :r]
  akkord = [chord(:C3, :major), :r, :r, :r, chord(:C3, :major), :r, :r, :r,
            chord(:G3, :major), :r, :r, :r, chord(:C3, :major), :r, :r, :r]
  
  in_thread do
    use_synth :fm
    play_pattern melodi, release: 0, amp: 1, divisor: 0.1, depth: 3
  end
  use_synth :square
  play_pattern akkord, sustain: 1.5, release: 0.5
end


# Nummer 8.
#  Nok med synth.  Tid til samples.
# Ligesom <play>, har vi en <sample> kommando.
# Samples kan afspilles forlæns, baglæns, hurtigere, langsommere, og også ændres med ADSR.
# Man kan også klippe i dem og afspille dele af dem.
if 0 == 1
  in_thread do
    16.times do
      sample :guit_em9, rate: rrand(-1, 1), pan: rrand_i(-1, 1)
    end
  end
  in_thread do
    16.times do
      density [1, 1, 1, 1, 1].choose do
        sample :bd_mehackit, rate: 1.3
        sleep 1
      end
    end
  end
  sleep 20
end

# Nummer 9.
#   Effekter.
#
# Der er et ton af effekter.  Prøv dem alle sammen.
#    with_fx <effekt>, <parametre> do ... end
# er opskriften.  Man kan lave lige så mange effekter som computeren kan klare.
# Slå effekterne op i "Fx", og de dem alle.  Med effekter kan vi lave endnu flere
# lyde på både samples og synths.
#
# Du skulle gerne kunne læse koden nu, og finde rundt i hjælpen til samles, synths og
# kommandoer.
#
# Prøv forskellige synths af, forskellige samples og effekter.
if 1 == 1
  16.times do
    with_fx :ping_pong do
      with_fx :reverb, room: 0.9 do
        with_fx :slicer do
          sample :bd_gas
          sleep 0.75
          sample :bd_gas
          sleep 0.25
          sample :sn_generic, finish: 0.12
          sleep 0.75
        end
        use_synth :pretty_bell
        play 60+rrand(-0.2, 0.2), release: 0.25/3, amp: rrand(0.5, 1)
        sleep 0.25/3
        play 62+rrand(-0.2, 0.2), release: 0.25/3, amp: rrand(0.5, 1)
        sleep 0.25/3
        play 66+rrand(-0.2, 0.2), release: 0.25/3, amp: rrand(0.5, 1)
        sleep 0.25/3
      end
    end
  end
end
