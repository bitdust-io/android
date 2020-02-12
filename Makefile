#
# Makefile
#
# Copyright (C) 2008-2018 Veselin Penev  https://bitdust.io
#
# This file (Makefile) is part of BitDust Software.
#
# BitDust is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BitDust Software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BitDust Software.  If not, see <http://www.gnu.org/licenses/>.
#
# Please contact us if you have any questions at bitdust.io@gmail.com


# This Makefile requires the following commands to be available:
# * python
# * virtualenv
# * git
# * pip3
# * adb
#

.DEFAULT_GOAL := build

.PHONY: build


install_dependencies_ubuntu:
	@sudo apt-get update; sudo apt-get upgrade
	@sudo apt-get install python3-pip openjdk-8-jdk python3-venv unzip git gcc make perl pkg-config autoconf libtool protobuf-compiler llvm zlib1g-dev libffi-dev libusb-1.0-0-dev libudev-dev python-zopeinterface python-twisted
	@sudo pip3 install cython

install_dependencies_macos:
	@brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer autoconf automake libtool
	@ln -s /usr/local/bin/glibtoolize /usr/local/bin/libtoolize

install_buildozer_ubuntu:
	@rm -rf buildozer/
	@git clone https://github.com/kivy/buildozer
	@cd buildozer/; python3 setup.py build; sudo pip3 install -e .; cd ..;

install_buildozer_macos:
	@rm -rf buildozer/
	@git clone https://github.com/kivy/buildozer
	@python3 -m virtualenv venv
	@cd buildozer/; ../venv/bin/python setup.py build; ../venv/bin/pip install -e .; cd ..;

install_p4a:
	@rm -rf python-for-android/
	@git clone --single-branch --branch develop https://github.com/kivy/python-for-android.git
	@cp -r -v etc/AndroidManifest.tmpl.xml ./python-for-android/pythonforandroid/bootstraps/sdl2/build/templates/
	@mkdir -p ./python-for-android/pythonforandroid/bootstraps/sdl2/build/src/main/res/xml/
	@cp -r -v etc/res/xml/network_security_config.xml ./python-for-android/pythonforandroid/bootstraps/sdl2/build/src/main/res/xml/
	@cp -r etc/PythonActivity.java ./python-for-android/pythonforandroid/bootstraps/sdl2/build/src/main/java/org/kivy/android/

update_engine_repo:
	@cd ../bitdust; git fetch --all; git reset --hard origin/master; cd ../bitdust.android;

update_ui_repo:
	@cd ../bitdust.ui; git fetch --all; git reset --hard origin/gh-pages; cd ../bitdust.android;

clean:
	@rm -rf .build_incremental
	@rm -rf .release_incremental
	@rm -rf .buildozer

rewrite_dist_files:
	@cp -r -v etc/PythonActivity.java ./.buildozer/android/platform/build-arm64-v8a/dists/bitdust1__arm64-v8a/src/main/java/org/kivy/android/
	@cp -r -v etc/AndroidManifest.tmpl.xml ./python-for-android/pythonforandroid/bootstraps/sdl2/build/templates/

.build_incremental:
	@python3 -c "import os, re; s = re.sub('(requirements = .+?python3)','# \g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('# requirements = incremental,kivy','requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@VIRTUAL_ENV=1 ./venv/bin/buildozer -v android debug
	@python3 -c "import os, re; s = re.sub('# (requirements = .+?python3)','\g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('requirements = incremental,kivy','# requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@echo '1' > .build_incremental

build: .build_incremental rewrite_dist_files
	@VIRTUAL_ENV=1 ./venv/bin/buildozer -v android debug

.release_incremental:
	@python3 -c "import os, re; s = re.sub('(requirements = .+?python3)','# \g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('# requirements = incremental,kivy','requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@VIRTUAL_ENV=1 ./venv/bin/buildozer -v android release | grep -v "Listing " | grep -v "Compiling " | grep -v "# Copy " | grep -v "# Create directory "
	@python3 -c "import os, re; s = re.sub('# (requirements = .+?python3)','\g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('requirements = incremental,kivy','# requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@echo '1' > .release_incremental

release: .release_incremental rewrite_dist_files
	@rm -rfv ./bin/*.apk
	@VIRTUAL_ENV=1 ./venv/bin/buildozer -v android release | grep -v "Listing " | grep -v "Compiling " | grep -v "# Copy " | grep -v "# Create directory "
	@mv ./bin/bitdust*.apk ./bin/BitDustAndroid_unsigned.apk

download_apk:
	@rm -rfv bin/*.apk
	@scp android.build:bitdust.android/bin/BitDustAndroid.apk bin/.
	@ls -la bin/

test_apk:
	@adb install -r bin/BitDustAndroid.apk

log_adb:
	@adb logcat | grep -v extracting | grep -v "Checking pattern" | grep -v "Library loading" | grep -v "Loading library" | grep -v "AppleWebKit/537.36 (KHTML, like Gecko)" | grep -v "I Bitdustnode:   " | grep -v "I Bitdustnode: DEBUG:jnius.reflect:" | grep -e python -e Bitdustnode -e "E AndroidRuntime" -e "F DEBUG" -e "PythonActivity:" -e "WebViewConsole"

log_main:
	@adb shell tail -f /storage/emulated/0/.bitdust/logs/android.log

log_states:
	@adb shell tail -f /storage/emulated/0/.bitdust/logs/automats.log

shell:
	@adb shell "cd /storage/emulated/0/.bitdust/; ls -la; sh;"

cat_main_log:
	@adb shell cat /storage/emulated/0/.bitdust/logs/android.log

cat_automat_log:
	@adb shell cat /storage/emulated/0/.bitdust/logs/automats.log
