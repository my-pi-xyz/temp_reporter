# temp_reporter
Reports current temp and hum on an LCD

![Alt text](TempReporter.png?raw=true)

The LCD used was taken from the Freenove starter kit and it had the LCM1602 chip already in place.  The code used to drive the LCD is from their kit.

To use this code you will need to install Adafruit_Python_DHT

You can use these steps to install the required library:

    git clone https://github.com/adafruit/Adafruit_Python_DHT.git

    cd Adafruit_Python_DHT

    sudo apt-get install build-essential python-dev (optional)

    sudo python setup.py install

