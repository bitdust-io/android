# BitDust for Android


Tested on Ubuntu 18.04 Desktop and Mac OS Mojave (still failed).


#### Ubuntu dependencies

        sudo apt-get update
        sudo apt-get upgrade

        sudo apt-get install git gcc make perl
        sudo apt-get install python3-pip openjdk-8-jdk autoconf libtool python3-venv
        sudo apt-get install zlib1g-dev libffi-dev
        sudo apt-get install python-zopeinterface python-twisted
        sudo apt-get install libusb-1.0-0-dev libudev-dev
        sudo apt-get install protobuf-compiler

        sudo pip3 install cython


#### MacOS dependencies

        brew install git gcc make
        sudo /usr/local/bin/python3 -m pip install Cython
        export PATH="$PATH:/Library/Frameworks/Python.framework/Versions/3.7/bin"
        sudo installer -pkg /Library/Developer/CommandLineTools/Packages/macOS_SDK_headers_for_macOS_10.14.pkg -target /
        # still issues with zlib in python 3.7


#### Install buildozer

        make install_buildozer


#### Clone BitDust sources

        make clone


#### Make sure to start from clean state

        make clean


#### Build APK

        make


## Connect and run on Android device

Enable "Developer Mode" on your Android device: https://developer.android.com/studio/debug/dev-options

Open another terminal window and run this to be able to catch Python logs from your Android:

        adb logcat | grep python


Now connect your device with USB cable and install APK file you just created:

        adb install -r bin/bitdust-1.0.1-armeabi-v7a-debug.apk


On your device find "BitDust" application and start it. You will see a lot of output in another console window and will be to monitor running application.

