python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python controller.py

sudo mount -t cifs //192.168.1.120/SSD ~/samba -o username=osmc,password=osmc,uid=1000,gid=1000,file_mode=0777,dir_mode=0777

