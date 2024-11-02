import RPi.GPIO as GPIO
import time
import subprocess

config = {
    23: "balle.AVI",
    24: "papillon.mp4",
    25: "pipou.mp4",
    8: "poisson.mp4"
}

GPIO.setmode(GPIO.BCM)

def play_video(pin):
    subprocess.run(["pkill", "mpv"])
    path = "/home/jo/samba/trucs/" + config[pin]
    subprocess.Popen([
        "mpv",
        "--fullscreen",
        "--no-osd-bar",
        "--no-border",
        "--input-ipc-server=/tmp/mpv-socket",
        path
    ])

for pin in config:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=play_video, bouncetime=200)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    subprocess.run(["pkill", "mpv"])
