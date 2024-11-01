import RPi.GPIO as GPIO
import time
import subprocess

config = {
    23: "IWITW variante.mp4",
    24: "Jasmina.AVI",
    25: "La Quizza.AVI",
    8: "ouais ouais c'est la vie v2.mov"
}

def getpath(pin):
    return "/home/jo/samba/trucs/" + config[24]

GPIO.setmode(GPIO.BCM)

vlc = subprocess.Popen([
    "vlc", "--fullscreen", "--no-video-title-show",
    "--no-video-deco", "--no-embedded-video",
    "--no-video-title-show", "--rc-fake-tty",
    "--rc-unix", "/tmp/vlc.sock",
    getpath(23)
])

def change_video(pin):
    with open("/tmp/vlc.sock", "w") as vlc_socket:
        vlc_socket.write(f"add {getpath(pin)}\n")

for pin in config:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=change_video, bouncetime=200)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    vlc.terminate()
