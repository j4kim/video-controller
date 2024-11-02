# Video controller

A python script to run videos using MPV.
The played video is changed via buttons wired to GPIO ports on a Raspberry Pi.
MPV messages to change the video are handled by a socket.

## Install

	python3 -m venv venv

	source venv/bin/activate

	pip install -r requirements.txt

	cp config.py.example config.py

## Run

	python controller.py

## Run as a service

	sudo nano /etc/systemd/system/video-controller.service
	
The service is copied to [video-controller.service](video-controller.service)

Reload after change in the service:

	sudo systemctl daemon-reload
	
Restart service:

	sudo systemctl restart video-controller.service
	
Enable/disable service:

	sudo systemctl enable video-controller.service
