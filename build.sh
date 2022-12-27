#!/usr/bin/env bash
# exit on error
set -o errexit

# this is a build script that will install chromedriver
# while still working with the native Python environment on render






## Adding trusting keys to apt for repositories
#wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#
## Adding Google Chrome to the repositories
#sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#
## Updating apt to see and install Google Chrome
#apt-get -y update
#
## Magic happens
#apt-get install -y google-chrome-stable
#
## Installing Unzip
#apt-get install -yqq unzip
#
## Download the Chrome Driver
#wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#apt-get -y update
#apt-get install -y google-chrome-stable
#
## Install chromedriver
#apt-get install -yqq unzip
#wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
#unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/





# STORAGE_DIR=/opt/render/project/.render
#
# if [[ ! -d $STORAGE_DIR/chrome ]]; then
#   echo "...Downloading Chrome"
#   mkdir -p $STORAGE_DIR/chrome
#   cd $STORAGE_DIR/chrome
#   wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#   dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
#   rm ./google-chrome-stable_current_amd64.deb
#   cd $HOME/project/src # Make sure we return to where we were
# else
#   echo "...Using Chrome from cache"
# fi

# be sure to add Chromes location to the PATH as part of your Start Command
# export PATH="${PATH}:/opt/render/project/.render/chrome/opt/google/chrome/"






CHROMEDRIVER_PATH=/usr/local/bin/chromedriver

if [[ ! -d $CHROMEDRIVER_PATH ]]; then

    # Download chromedriver
    echo "...Downloading Chromedriver..."
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
    apt-get -y update
    apt-get install -y google-chrome-stable

    # Install chromedriver
    echo "...Installing Chromedriver..."
    apt-get install -yqq unzip
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

else
  echo "...Using Chrome from cache"
fi


echo "...Build Script Completed!"