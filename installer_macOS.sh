#!/bin/sh

# macOS Requirements:
# A 64-bit Intel CPU or Apple Silicon CPU
# macOS Big Sur (11) (or higher)
# Comman Line Tools (CLT) for Xcode (from xcode-select --install or https://developer.apple.com/download/all/) or Xcode
# The Bourne-again shell for installation (i.e. bash)


# installs all dependencies
xcode-select --install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew update
#curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
#python3 get-pip.py
python3 -m ensurepip --upgrade

# check to make sure both python3 and pip3 are installed
echo "\nVersions:"
python3 --version
pip3 --version
echo "\n\n"
read -p "Do you see a version printed above for python3 and pip3 (will say 'Python 3.10.9' or higher followed by 'pip 22.3.1' or higher)? (y/n)" yn
case $yn in
	[yY] ) echo "great, continuing...";
		break;;
	[nN] ) echo "contact e.bst@pm.me - installation aborted";
		exit;;
	* ) echo "invalid response";
		exit 1;;
esac

pip3 install PyQt5
pip3 install twilio
pip3 install pyinstaller
brew tap twilio/brew && brew install twilio
twilio login

# install and move the program to the correct directories
cd source
# check main program name
pyinstaller main.py --name BUZZER --onefile
mv formatting dist
chmod +x check_logs.sh && mv check_logs.sh dist
mv assets dist
mv contacts.csv dist
mv data.tsv dist # check on this one
rm -rf __pycache__ client_connect.py mms.py sms.py main.py
echo "\n\n\n\n.........................................................................................\n#########################################################################################\nInstallation Finished. Open the Application and read the manual to get started messaging.\n#########################################################################################\n.........................................................................................\n"

# create desktop shortcut or application
