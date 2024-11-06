import RPi.GPIO as GPIO
import time
import config

GPIO.setmode(GPIO.BCM)

def printpin(pin):
    print(pin, config.videos[pin])

for pin in config.videos:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=printpin, bouncetime=200)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
