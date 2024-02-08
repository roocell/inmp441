# inmp441
I2S MEMS Microphone for Raspberry Pi

# install
Starting with bullseye on Raspberry Pi Zero W.<BR>
Follow instructions here: https://makersportal.com/blog/recording-stereo-audio-on-a-raspberry-pi<BR>
Abbreviated below.<BR>
The adafruit installer script (i2smic.py) creates the audio device driver.<BR>
```
sudo apt-get -y update
sudo apt-get -y upgrade
sudo reboot
sudo apt install python3-pip
sudo apt-get install idle3
sudo pip3 install --upgrade adafruit-python-shell
sudo wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
sudo python3 i2smic.py
sudo apt-get -y install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sudo pip3 install pyaudio matplotlib scipy
sudo apt-get install libopenblas-dev
```

# dump audio to find hw index
sudo python dumpaudio.py
sudo python mictest.py

# test wav file
generates wave files in data directory.<BR>
export wav file off pi and listen to it.
