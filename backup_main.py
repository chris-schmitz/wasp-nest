import board
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogOut, AnalogIn
import touchio
import time
import neopixel
import random
import adafruit_hcsr04

touch = touchio.TouchIn(board.D1)
ultrasonic = adafruit_hcsr04.HCSR04(trigger_pin=board.D3, echo_pin=board.D4)

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


rainbow_last_checked = 0
rainbow_interval = 0.0005
rainbow_index = 0
rainbow_current_cell = 0


def rainbow(now):
    global rainbow_index
    global rainbow_current_cell
    global rainbow_last_checked
    if now - rainbow_last_checked > rainbow_interval:
        rainbow_last_checked = now

        # for p in range(NUMPIXELS):
        idx = int((rainbow_current_cell * 256 / NUMPIXELS) + rainbow_index)
        neopixels[rainbow_current_cell] = wheel(idx & 255)
        neopixels.show()

        rainbow_current_cell += 1
        if rainbow_current_cell > NUMPIXELS - 1:
            rainbow_current_cell = 0
            rainbow_index = (rainbow_index + 1) % 256  # run from 0 to 255


brightness = 0.1


def cycle_brightness():
    brightness += 0.1
    if brightness > 1.0:
        brightness = 0.1
    neopixel.brightness = brightness


changed = set()


def get_random_pixel(changed_pixels):
    pixel = None
    while pixel is None:
        pixel = random.randint(0, NUMPIXELS - 1)
        if pixel not in changed_pixels:
            return pixel
        else:
            return None
            print("skip")


slow_replace_color = (255, 0, 255)
slow_replace_last_checked = 0
slow_replace_interval = 0.3


def slow_replace(now):
    global changed
    global slow_replace_last_checked
    global slow_replace_interval
    global slow_replace_color
    if now - slow_replace_last_checked > slow_replace_interval:
        slow_replace_last_checked = now

        if len(changed) < NUMPIXELS - 1:

            pixel = get_random_pixel(changed)
            if pixel is not None:
                changed.add(pixel)
                neopixels[pixel] = slow_replace_color
                neopixels.show()
        else:
            changed.clear()
            i = (random.randint(0, 255) + 1) % 256  # run from 0 to 255
            slow_replace_color = wheel(i & 255)


current_pattern = "SLOW_REPLACE"
pattern_debounce_time = 1.0
pattern_debounce_last_check = 0


def cycle_pattern(now):
    # global neopixels
    global current_pattern
    global pattern_debounce_time
    global pattern_debounce_last_check
    if now - pattern_debounce_last_check > pattern_debounce_time:
        neopixels.fill((0, 0, 0))
        neopixels.show()
        print("cycle pattern...")
        pattern_debounce_last_check = now
        if current_pattern == "RAINBOW":
            current_pattern = "SLOW_REPLACE"
        else:
            current_pattern = "RAINBOW"
        print("new pattern: ", current_pattern)


# current_pattern = 'RAINBOW'

base_interval_last_checked = 0
base_interval = 0.0005
while True:
    now = time.monotonic()
    if now - base_interval_last_checked > base_interval:

        if touch.value:
            cycle_pattern(now)

        base_interval_last_checked = now
        if current_pattern == "SLOW_REPLACE":
            slow_replace(now)
        elif current_pattern == "RAINBOW":
            rainbow(now)
        # try:
        #     print(ultrasonic.distance)
        # except RuntimeError:
        #     pass

        # if (touch.value):
        #   cycle_brightness()
