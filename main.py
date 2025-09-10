# Trinket IO demo
# Welcome to CircuitPython 3.1.1 :)

import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import touchio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import adafruit_dotstar as dotstar
import time
import neopixel
import random

# One pixel connected internally!
# dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)


# Capacitive touch on D3
touch = touchio.TouchIn(board.D3)

# NeoPixel strip (of 16 LEDs) connected on D4
NUMPIXELS = 12
neopixels = neopixel.NeoPixel(board.D2, NUMPIXELS, brightness=0.8, auto_write=False)


######################### HELPERS ##############################


# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0:
        return (0, 0, 0)
    if pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (int(pos * 3), int(255 - (pos * 3)), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - pos * 3), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))


######################### MAIN LOOP ##############################

# i = 0
# while True:
#     print("Loop", i)
#     #   dot[0] = wheel(i & 255)

#     # also make the neopixels swirl around
#     for p in range(NUMPIXELS):
#         idx = int((p * 256 / NUMPIXELS) + i)
#         neopixels[p] = wheel(idx & 255)
#     neopixels.show()

#     # use D3 as capacitive touch to turn on internal LED
#     if touch.value:
#         print("D3 touched!")
#     #   led.value = touch.value

#     i = (i + 1) % 256  # run from 0 to 255
#     time.sleep(0.01) # make bigger to slow down

changed = set()
def get_random_pixel():
    pixel = None
    while pixel is None:
        pixel = random.randint(0, NUMPIXELS - 1)
        if pixel not in changed:
            changed.add(pixel)
        else:
            print("skip")
    return pixel

brightness = 0.1

def cycle_brightness():
    brightness += 0.1
    if brightness > 1.0:
        brightness = 0.1
    neopixel.brightness = brightness


i = 0
while True:
    if (touch.value):
      cycle_brightness()
    changed.clear()
    i = (random.randint(0,255) + 1) % 256  # run from 0 to 255
    color = wheel(i & 255)
    while len(changed) < NUMPIXELS-1:
        print(len(changed))

        pixel = get_random_pixel()
        # print(color)

        neopixels[pixel] = color
        neopixels.show()
        time.sleep(0.2)

        # idx = int((pixel * 256 / NUMPIXELS) + i)
        # neopixels[pixel] = wheel(idx & 255)
        # neopixels.show()


