# For at komme i gang

Installer VSCode herfra:
    https://code.visualstudio.com/download

Installer VSCode udvidelse:
    PlatformIO

Nu skal VSCode lukkes.

Installer driver til vores AZdelivery ESP32 Wroom 32 C4 board:
    https://www.silabs.com/documents/public/software/CP210x_Universal_Windows_Driver.zip

Start VSCode igen.
Åbn PLatformIO (det ligner en myre i venstre side)
Vælg "Platforms" -> "Embedded" tab os søg efter "ESP32" 
Vælg "Expressif 32" og installer miljøet.
Vores ESP32 board hedder "AZ-Delivery ESP-32 Dev Kit C V4" og har ID "az-delivery-devkit-v4"

Det tager noget tid at installere.

# Første projekt
Det første projekt går ud på at sikre vores værktøj er sat op rigigt.  Vi skal "kompilere" (eller "bygge") et program der ikke gør noget.

I PlatformIO vælg "Home" og herfra "New Project".
Det nye projekt skal have et navn. Brug et navn UDEN mellemrum.  Brug _ i stedet for.  Som board vælger du "AZ-Delivery ESP32 Dev Kit C V4".  Framework skal være espidf.  Og til sidst skal Location være en sti på din computer som heller IKKE har mellemrum i sig.

Når du trykker "Finish"-knappen går der igen noget tid mens alle filer til esdidf-bibliotekerne hentes fra Internettet.

Når det hele er klart har du et projekt med forskellige mapper:
mit_projekt

    -> include/
       lib/
       src/
           main.c
           CMakeLists.txt
       test/
       platformio.ini

I ```src``` findes ```main.c```.  Hvis du åbner den kan du se det program der bygges.  Det gør ikke noget, og det er helt fint.

Du vil også finde en "platformio.ini" fil.  Åbn den og indsæt en linje med følgende:

    monitor_speed = 115200

Nu tester vi at alt fungerer.

Nederst i VSCode-vinduet er der en række ikoner: et flueben, en pil, en skraldespand, en kolbe, et stik.

Tryk på fluebenet og se programmet kompilere ("compile" på engelsk).
Det skulle meget gerne gå uden problemer.  Det tager noget tid første gang.

Hvis ESP32-boardet ikke er tilskuttet PCen skal det gøres nu.

Tryk så på "->" knappen.  Programmet skal gerne uploades til vores ESP32 board.

Hvis det går godt, er vi klar til at skrive det første program!


