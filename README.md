magicOS
=======

MagicOS  is an operating system based on ubuntu for mining cryptocurrencies

The code found here can be used to build a magicOS image ready to burn in a USB stick.

You must download the file magicOSfiles.tar.gz

NOTE: You may be asked for a sudo password during the building process

wget -c http://magicpool.org/downloads/magicOSfiles.tar.gz
./build.sh
sudo dd if=magicOS.img of=/dev/sdX
sudo sync
