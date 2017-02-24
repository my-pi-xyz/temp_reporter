#!/usr/bin/env python

########################################################################
# Filename    : TempReporter.py
# Description : Displays temperature and humidity on an LCD.
# auther      : www,my-pi.xyz
# modification: 2017/02/27
########################################################################

import Adafruit_DHT
import LCD1602

from time import sleep
from gpiozero import LED, Button

# -----------------------------------------------------------------------
# Module level variables
button_control = Button(18)
report_in_fahrenheit = False


# -----------------------------------------------------------------------
# Button handling
def button_pressed():
    global report_in_fahrenheit
    report_in_fahrenheit = not report_in_fahrenheit


# -----------------------------------------------------------------------
# Support routines
def to_fahrenheit(celsius):
    return 1.8 * celsius + 32


# -----------------------------------------------------------------------
# Program setup
def setup():
    button_control.when_pressed = button_pressed

    LCD1602.init(0x27, 1)
    LCD1602.write(0, 0, "...starting...")
    sleep(1)


# -----------------------------------------------------------------------
# Program clean up
def destroy():
    LCD1602.clear()


# -----------------------------------------------------------------------
# Program main loop
def loop():
    global report_in_fahrenheit

    max_temperature = 0
    min_temperature = 0
    max_humidity = 0
    min_humidity = 0

    next_display = 1  # Show current values

    while True:
        # Take reading
        current_humidity, current_temperature = Adafruit_DHT.read_retry(11, 4)

        # Record min/max stats
        if current_temperature > max_temperature:
            max_temperature = current_temperature
        if min_temperature < current_temperature:
            min_temperature = current_temperature

        if current_humidity > max_humidity:
            max_humidity = current_humidity
        if min_humidity < current_humidity:
            min_humidity = current_humidity

        # Prepare the display
        line_1 = ''
        line_2 = ''

        if next_display == 1:  # Show current values
            if report_in_fahrenheit:
                line_1 = 'Cur Temp : {0:0.1f}F'.format(to_fahrenheit(current_temperature))
            else:
                line_1 = 'Cur Temp : {0:0.1f}C'.format(current_temperature)
            line_2 = 'Cur Hum  : {0:0.1f}%'.format(current_humidity)

            next_display = 2  # Show max values

        elif next_display == 2:  # Show max values
            if report_in_fahrenheit:
                line_1 = 'Max Temp : {0:0.1f}F'.format(to_fahrenheit(max_temperature))
            else:
                line_1 = 'Max Temp : {0:0.1f}C'.format(max_temperature)
            line_2 = 'Max Hum  : {0:0.1f}%'.format(max_humidity)

            next_display = 3  # Show min values

        elif next_display == 3:  # Show min values
            if report_in_fahrenheit:
                line_1 = 'Min Temp : {0:0.1f}F'.format(to_fahrenheit(min_temperature))
            else:
                line_1 = 'Min Temp :  {0:0.1f}C'.format(min_temperature)
            line_2 = 'Min Hum  : {0:0.1f}%'.format(min_humidity)

            next_display = 1  # Show current values

        # Let the dog see the rabbit
        LCD1602.write(0, 0, line_1)
        LCD1602.write(0, 1, line_2)

        sleep(1)


# -----------------------------------------------------------------------
# Program Start
if __name__ == '__main__':
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        # When 'Ctrl+C' is pressed we need to clean up and exit.
        destroy()
