# led-animations

## Installation

Setup SD card by downloading latest Rasbian OS from (https://www.raspberrypi.org/downloads/raspbian/)[raspberrypi.org]
Flash with (https://etcher.io/)[Etcher]
Boot and log in with default credentials `pi` and `raspberry`.

Use `sudo raspi-config` to enter the config and edit at least the following:
```
Change default password
Localization
 keyboard
 wifi country
 timezone
Interfaces
 SSH
Advanced
 expand
Networking
 hostname
 wifi
```

Then `reboot`. Find Raspberry's IP by using `ifconfig` or `nmap -sP 192.168.1.*` and use SSH to login.

`ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no pi@192.168.1.220`

Update packages
```
sudo apt-get update
sudo apt-get upgrade
```

Install required packages
```
sudo apt-get install scons python-pip git python-dev swig libglib2.0-dev
sudo pip install numpy bluepy
```

Install Neopixel
```
git clone https://github.com/jgarff/rpi_ws281x.git
cd rpi_ws281x/
sudo scons
cd python/
sudo python ./setup.py build
sudo python ./setup.py install
export PYTHONPATH=".:build/lib.linux-armv7l-2.7"
```

Ready to use
`git clone https://github.com/EinariTuukkanen/led-animations.git`
