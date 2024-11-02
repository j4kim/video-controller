import RPi.GPIO as GPIO
import time
import subprocess
import socket
import json

config = {
    23: "balle.AVI",
    24: "papillon.mp4",
    25: "pipou.mp4",
    8: "poisson.mp4"
}

mpv_socket = "/tmp/mpv-socket"

videos_dir = "/home/jo/samba/trucs/"

GPIO.setmode(GPIO.BCM)

def get_path(pin):
    return videos_dir + config[pin]

def run_mpv():
    return subprocess.Popen([
        "mpv",
        "--fullscreen",
        "--no-osd-bar",
        "--no-border",
        f"--input-ipc-server={mpv_socket}",
        "--idle"
    ])

def send_mpv_command(command):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.connect(mpv_socket)
        sock.sendall(json.dumps(command).encode("utf-8") + b"\n")

def loadfile(pin):
    send_mpv_command({"command": ["loadfile", get_path(pin), "replace"] })
for pin in config:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=loadfile, bouncetime=200)

mpv = run_mpv()

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    mpv.terminate()
