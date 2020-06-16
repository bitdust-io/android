# BitDust for Android

This repo contains all required scripts and configs to build BitDust application for Android Platform.

We only target devices running the latest Android API 21 version at the moment.



## Prepare application folders

First you must clone BitDust Engine and BitDust UI repositories to your local machine next to the current repository folder.
BitDust Android APK bundle will include files from both sources:

    git clone https://github.com/bitdust-io/public.git bitdust
    git clone --single-branch --branch gh-pages --depth=1 https://github.com/bitdust-io/ui.git bitdust.ui


Now clone BitDust Android repository in same folder and create sym-links to other repositories:

    git clone https://github.com/bitdust-io/android.git bitdust.android
    cd bitdust.android/src/
    ln -s ../../bitdust bitdust
    ln -s ../../bitdust.ui www
    cd ..



## Install dependencies

#### Ubuntu 18.04 Desktop

	make install_dependencies_ubuntu



#### MacOS Mojave

(most probably not working at the moment)

	make install_dependencies_macos



#### Install Buildozer

	make install_buildozer



#### Install python-for-android

	make install_p4a



## Prepare keystore

To be able to publish BitDust on Google Play Market .APK file must be digitaly signed.

First create a keystore file:

	mkdir ~/keystores/
	keytool -genkey -v -keystore ~/keystores/bitdust.keystore -alias bitdust -keyalg RSA -keysize 4096 -validity 60000


Make sure you have backup copy of the `bitdust.keystore` file and the keystore password!

Now you need to get from Google Play Console "Encryption Key" which you will use to prepare `output.zip` file.

You need to do that only one time - the `output.zip` file must be uploaded back to Google.

This way Google will be able to verify the .APK file you built before publish it on the Play Market:

	java -jar pepk.jar --keystore=~/keystores/bitdust.keystore --alias=bitdust --encryptionkey=<Encryption Key> --include-cert --output=output.zip



## Make sure BitDust Engine and UI repositories are up to date

	make update_engine_repo
	make update_ui_repo



## Build APK image

#### Ubuntu 18.04 Desktop

	./release_ubuntu.sh 1.0.5



#### MacOS Mojave

	./release_macos.sh 1.0.5



## Connect and run on Android device

Enable "Developer Mode" on your Android device: https://developer.android.com/studio/debug/dev-options

Open another terminal window and run this to be able to catch Python logs from your Android:

    cd bitdust.android
    make logcat


Now connect your device with USB cable and install APK file you just created.

Switch back to previous terminal window and run:

    make test_apk


On your device find "BitDust" application and start it.

You will see a lot of output in another terminal window and will be able to monitor running application.


## Success!

Now you can upload file `bitdust.android/bin/BitDustAndroid.apk` to Google Play Console.
