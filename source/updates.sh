#!/bin/sh

# macOS Requirements:
# A 64-bit Intel CPU or Apple Silicon CPU
# macOS Big Sur (11) (or higher)
# Comman Line Tools (CLT) for Xcode (from xcode-select --install or https://developer.apple.com/download/all/) or Xcode
# The Bourne-again shell for installation (i.e. bash)


# run homebrew and python updates
brew update && brew upgrade
python3 -m ensurepip --upgrade
pip3 install --upgrade PyQt5
pip3 install --upgrade twilio
python3 --version
pip3 --version
twilio --version
echo('FINISHED ALL UPDATES.')
