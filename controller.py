import RPi.GPIO as GPIO
import time
import subprocess
import socket
import json
import config
import os

mpv_socket = os.path.expanduser("~/.mpv-socket")

def get_path(pin):
    return config.videos_dir + config.videos[pin]

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

mpv = run_mpv()

GPIO.setmode(GPIO.BCM)

for pin in config.videos:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=loadfile, bouncetime=200)

try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    mpv.terminate()
