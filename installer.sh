#!/bin/bash

clear

echo "Updating System"
sudo apt-get update  && sudo apt-get upgrade

echo "Installing dependencies"
sudo apt install -y libsdl2-dev make gcc git python3 python3-pip python3-venv

echo "Creating and activating python virtual environment"
python3 -m venv env
source env/bin/activate

echo "Installing python packages and deactivating virtual environment"
pip install psutil evdev pyudev

echo "Cloning minivmac"
git clone https://github.com/minivmac/minivmac

echo "Cloning Minivmac Disk Helper"
git clone https://github.com/ngsenecal/Minivmac-Disk-Helper

echo "Replacing Sony floppy disk driver"
cp ./Minivmac-Disk-Helper/helper_files/SONYEMDV.c ./minivmac/src

echo "Setting build settings"

echo "Building minivmac"
./minivmac/build_linux64.sh

echo "Copying over helper.py and launch script"
cp ./Minivmac-Disk-Helper/helper_files/helper.py ./minivmac
cp ./Minivmac-Disk-Helper/helper_files/start.sh .
sudo chmod +x start.sh

echo "Done! Launch minivmac with the disk manager via start.sh"
