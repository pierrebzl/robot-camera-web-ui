# ROBOT

## Synopsis

This software provide an interface to control a specific pipe robot.

## Requirements

 * Raspberry Pi (only tested on pi 3)
 * Raspberry Pi camera plugged and enable :
   * `sudo raspi-config`
   * Select : "6 Enable Camera" > "Yes" > "Ok"
 * Python 3.x: `sudo apt-get update && sudo apt-get install python3 python3-systemd python3-pip`
 * virtualenv-3.x: `sudo apt-get install python-virtualenv`
 * Avahi-daemon to ensure Bonjour support and assign the .local Domain to Your Raspberry Pi:`sudo apt-get install avahi-daemon`

## Physical setup

## Installation: development environment

  * `sudo pip3 install virtualenv`
  * `git clone https://github.com/pierrebzl/robot-penetrator.git`
  * `cd robot-penetrator`
  * Create a virtualenv: `virtualenv --python=/usr/bin/python3 venv`
  * Activate the virtualenv: `. venv/bin/activate`
  * Install deps `pip install -r requirements.txt`
  * Start application: `python3 main.py`
  * Check logs on the console and with `sudo journalctl -f`

## Installation: production setup

  * `sudo apt-get install python3.5 python3-pip git`
  * `sudo pip3 install virtualenv`
  * `git clone https://github.com/pierrebzl/robot-penetrator.git`
  * `cd robot-penetrator`
  * Create a virtualenv: `virtualenv --python=/usr/bin/python3 venv`
  * Activate the virtualenv: `. venv/bin/activate`
  * Install deps `pip install -r requirements.txt`
  * Check configuration file to ensure PIN are OK : `sudo nano conf/default.py`
  * Make sure paths are OK in `deploy/systemd/robot.service`
  * Install systemd service `sudo cp deploy/systemd/robot.service /etc/systemd/system/robot.service`
  * Enable robot on boot `sudo systemctl enable robot.service`
  * Start robot now `sudo systemctl start robot.service`
  * Get the status with `sudo systemctl status robot.service`

## Usage

Connect to raspberypi.local:8080 from local network or to [LOCAL_PI]:8080
