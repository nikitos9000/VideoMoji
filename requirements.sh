#!/usr/bin/env bash

# linux

sudo apt-get install portaudio
sudo apt-get install cmake libboost-dev

# Mac OS X

brew install lua
brew install portaudio

# Common

git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps;
./install.sh

. /Users/nsmetanin/torch/install/bin/torch-activate

for NAME in dpnn nn optim optnet csvigo cutorch cunn fblualib torchx tds; do
    luarocks install ${NAME};
done
