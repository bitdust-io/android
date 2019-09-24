# BitDust for Android

Tested on clean Ubuntu 18.04 Desktop.


## Install debian packages

        sudo apt-get update
        sudo apt-get upgrade

        sudo apt-get install git gcc make perl
        sudo apt-get install python3-pip openjdk-8-jdk autoconf libtool python3-venv
        sudo apt-get install zlib1g-dev libffi-dev
        sudo apt-get install python-zopeinterface python-twisted
        sudo apt-get install libusb-1.0-0-dev libudev-dev
        sudo apt-get install protobuf-compiler


## Install cython

        sudo pip3 install cython


## Install buildozer

        git clone https://github.com/kivy/buildozer
        cd buildozer/
        python setup.py build
        sudo pip3 install -e .
        cd ..


## Prepare project files

        mkdir android
        cd android
        cp ../buildozer.spec .


# Manual patches

        nano .buildozer/android/platform/python-for-android/pythonforandroid/recipes/twisted/__init__.py
        # comment out line:
        # patches = ['incremental.patch']


## Build APK

        buildozer -v android debug deploy run


## Connect and run on Android device

Enable "Developer Mode" on your Android device: https://developer.android.com/studio/debug/dev-options

Open another terminal window and run this to be able to catch Python logs from your Android:

        adb logcat | grep python


Now connect your device with USB cable and install APK file you just created:

        adb install -r bin/bitdust-1.0.1-armeabi-v7a-debug.apk


On your device find "BitDust" application and start it. You will see a lot of output in another console window and will be to monitor running application.

