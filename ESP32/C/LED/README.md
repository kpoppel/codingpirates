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

# Det første program

Vores første program skal tænde og slukke for en LED på vores board.
Find en LED og en modstand, 220 Ohm f.eks.  Modstanden skal til for at begrænse den strøm der kan gå i LEDen, så den ikke går i stykker ("brænder af").

Sæt modstanden på GND og i en tom række på protoboardet.  Sæt LED på "2"/GPIO2 og den samme række som modstanden.  Se billedet af boardet. 

LEDs skal vende rigtigt, da det er en "diode".  Sådan en vil kun sende strøm i én retning.  En LED har et langt ben og et kort ben. Det lange ben er "+" og det korte er "-".  Strømmen løber fra "+" til "-", så det lange ben skal altså være på GPIO2 og det korte sammen med modstanden.

Så skal programmet skrives. Lige nu ser det ud sådan her:

    void app_main(void) {}

Så det gør ikke meget.  Vi vil gerne styre LEDen med vores nye program.  Så her er det ny program så:

    // prg_1_LED_blink.c
    //------------------
    // Include driver for gpio to control pin
    #include <driver/gpio.h>
    // Include FreeRTOS for delay
    #include <freertos/FreeRTOS.h>
    #include <freertos/task.h>

    #define LED_PIN 2 // LED connected to GPIO2

    void app_main() {
        // Configure pin
        gpio_reset_pin(LED_PIN);
        gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);

        // Main loop
        while(true) {
            // Turn OFF LED
            gpio_set_level(LED_PIN, 0);
            // 500 ms delay
            vTaskDelay(500 / portTICK_PERIOD_MS);

            Turn ON LED
            gpio_set_level(LED_PIN, 1);
            // 500 ms delay
            vTaskDelay(500 / portTICK_PERIOD_MS);
        }
    }


# Registrering af knaptryk

Vi skal bruge en knap eller to til at styre funktioner med.  Med to knapper kan vi måske lave et menusystem.

Det første forsøg er bare at koble knappen på en GPIO og så se hvad der sker.
Forbind den lille kontakt med to ben til GPIO06 på det ene ben og GND på det andet.

Programmet skal nu tænde for LED når knappen trykkes, og slukke når den slippes.
Det betyder at GPIO skal sættes op som "pull up" og som "input".  "pull up" betyder at vores MCU board sørger for at en lille modstand mellem GPIO-pin og forsyningen (3V3) aktiveres, så GPIO er "1" når der ikke sker noget.

        // prg_2_LED_knap.c
        //------------------
        // Include driver for gpio to control pin
        #include <driver/gpio.h>
        // Include FreeRTOS for delay
        #include <freertos/FreeRTOS.h>
        #include <freertos/task.h>

        #define LED_PIN 2    // LED connected to GPIO2
        #define LED_BUTTON 6 // Button connected to GPIO6

        void app_main() {
            // Configure pin
            gpio_reset_pin(LED_PIN);
            gpio_set_direction(LED_PIN, GPIO_MODE_OUTPUT);

            // Configure pin (full configuration)
            gpio_config_t io_conf;
            io_conf.intr_type = GPIO_INTR_DISABLE;
            io_conf.mode = GPIO_MODE_INPUT;
            io_conf.pin_bit_mask = (1ULL << BUTTON_PIN);
            io_conf.pull_down_en = 0;
            io_conf.pull_up_en = 1;
            gpio_config(&io_conf);

            // Main loop
            while(true) {
                // Turn OFF LED
                gpio_set_level(LED_PIN, 0);
                // 500 ms delay
                vTaskDelay(500 / portTICK_PERIOD_MS);

                Turn ON LED
                gpio_set_level(LED_PIN, 1);
                // 500 ms delay
                vTaskDelay(500 / portTICK_PERIOD_MS);
            }
        }




https://github.com/craftmetrics/esp32-button
gpio_set_direction(GPIO_NUM_33, GPIO_MODE_INPUT);
https://esp32tutorials.com/esp32-push-button-esp-idf-digital-input/
HW debounce: https://www.youtube.com/watch?v=FOMI2J-y1Rc

