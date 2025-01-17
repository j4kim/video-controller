import RPi.GPIO as GPIO
import time
import subprocess
import socket
import json
import config
import os

mpv_socket = os.path.expanduser("~/.mpv-socket")

reading = -1

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
    print("> send", command)
    sock.sendall(json.dumps(command).encode("utf-8") + b"\n")

def loadfile(pin):
    global reading
    if pin == reading:
        send_mpv_command({"command": ["stop"] })
    else:
        send_mpv_command({"command": ["loadfile", get_path(pin), "replace"] })
        reading = pin

mpv = run_mpv()

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

tries = 0

while True:
    time.sleep(0.4)
    tries += 1
    try:
        sock.connect(mpv_socket)
        print("connected")
        break
    except ConnectionRefusedError:
        if tries > 10:
            print("failed connecting to socket")
            break

GPIO.setmode(GPIO.BCM)

for pin in config.videos:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=loadfile, bouncetime=200)

try:
    while True:
        data = sock.recv(1024)
        if data:
            message = data.decode("utf-8")
            print("< received", message)
            if '{"event":"idle"}' in message:
                reading = -1
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
    mpv.terminate()
    sock.close()
