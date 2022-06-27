#!/usr/bin/python

import board
import busio
import digitalio
import adafruit_ssd1306
import subprocess

from time import sleep
from PIL import Image, ImageDraw, ImageFont
from signal import pause
from gpiozero import Button

# Define display on/off button
button = Button(21)
# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)
# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5
# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)
# Clear display.
oled.fill(0)
oled.show()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)
font = ImageFont.truetype('/home/pi/fonts/PixelOperator.ttf', 16)

displayOnOff = True

def display_on_off():
    global displayOnOff
    displayOnOff = not displayOnOff

def display_func():
    while True:
        while displayOnOff:
            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
            # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = subprocess.check_output(cmd, shell = True )
            cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
            CPU = subprocess.check_output(cmd, shell = True )
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            MemUsage = subprocess.check_output(cmd, shell = True )
            cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
            Disk = subprocess.check_output(cmd, shell = True )
            cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
            temp = subprocess.check_output(cmd, shell = True )
            # Pi Stats Display
            draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=font, fill=255)
            draw.text((0, 16), str(CPU,'utf-8') + "%", font=font, fill=255)
            draw.text((80, 16), str(temp,'utf-8') , font=font, fill=255)
            draw.text((0, 32), str(MemUsage,'utf-8'), font=font, fill=255)
            draw.text((0, 48), str(Disk,'utf-8'), font=font, fill=255)        
            # Display image
            oled.image(image)
            oled.show()    
            sleep(1)
        else:
            # Clear display.
            oled.fill(0)
            oled.show()
            sleep(1)

try:
    button.when_pressed = display_on_off    
    display_func()
    pause()

finally:
    pass
