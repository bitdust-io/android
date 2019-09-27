# BitDust for Android


Tested on Ubuntu 18.04 Desktop.


#### Install dependencies

        sudo apt-get update
        sudo apt-get upgrade

        sudo apt-get install git gcc make perl pkg-config autoconf libtool protobuf-compiler
        sudo apt-get install python3-pip openjdk-8-jdk python3-venv
        sudo apt-get install zlib1g-dev libffi-dev libusb-1.0-0-dev libudev-dev
        sudo apt-get install python-zopeinterface python-twisted

        sudo pip3 install cython


#### Install buildozer

        make install_buildozer


#### Clone BitDust sources

        make clone


#### Make sure to start from clean state

        make clean


#### Build APK image

        make


## Connect and run on Android device

Enable "Developer Mode" on your Android device: https://developer.android.com/studio/debug/dev-options

Open another terminal window and run this to be able to catch Python logs from your Android:

        adb logcat | grep python


Now connect your device with USB cable and install APK file you just created:

        adb install -r bin/bitdust-1.0.1-armeabi-v7a-debug.apk


On your device find "BitDust" application and start it. You will see a lot of output in another console window and will be able to monitor running application.

Now you can open web browser on your Android and open `http://127.0.0.1:18000`.

Hello, world!
