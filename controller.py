import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def button_callback(pin):
    print(pin)

for pin in [23, 24]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback, bouncetime=200)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
