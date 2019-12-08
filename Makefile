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
# * buildozer
# * pip3
# * adb
#

.DEFAULT_GOAL := build

.PHONY: build


install_buildozer:
	@rm -rf buildozer/
	@git clone https://github.com/kivy/buildozer
	@cd buildozer/; python3 setup.py build; sudo pip3 install -e .; cd ..;

clean:
	@rm -rf .build_incremental
	@rm -rf .release_incremental
	@rm -rf .buildozer


.build_incremental:
	@python3 -c "import os, re; s = re.sub('(requirements = .+?python3)','# \g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('# requirements = incremental,kivy','requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@buildozer -v android debug
	@python3 -c "import os, re; s = re.sub('# (requirements = .+?python3)','\g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('requirements = incremental,kivy','# requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@echo '1' > .build_incremental

build: .build_incremental
	@buildozer -v android debug

.release_incremental:
	@python3 -c "import os, re; s = re.sub('(requirements = .+?python3)','# \g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('# requirements = incremental,kivy','requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@buildozer -v android release
	@python3 -c "import os, re; s = re.sub('# (requirements = .+?python3)','\g<1>',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@python3 -c "import os, re; s = re.sub('requirements = incremental,kivy','# requirements = incremental,kivy',open('buildozer.spec','r').read()); open('buildozer.spec','w').write(s);"
	@echo '1' > .release_incremental

release: .release_incremental
	@rm -v ./bin/*.apk
	@buildozer -v android release
	@mv ./bin/bitdust__*.apk ./bin/BitDustAndroid_unsigned.apk
	@jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore /home/bitdust/keystores/bitdust.keystore bin/BitDustAndroid_unsigned.apk bitdust
	@~/.buildozer/android/platform/android-sdk/build-tools/29.0.2/zipalign -v 4 ./bin/BitDustAndroid_unsigned.apk  ./bin/BitDustAndroid.apk

logcat:
	@adb logcat | grep -v extracting | grep -v "Checking pattern" | grep -e python -e Bitdustnode -e "E AndroidRuntime"
