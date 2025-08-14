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
