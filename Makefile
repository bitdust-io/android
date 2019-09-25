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
#

.DEFAULT_GOAL := build

.PHONY: build


install_buildozer:
	@rm -rf buildozer/
	@git clone https://github.com/kivy/buildozer
	@cd buildozer/; python3 setup.py build; sudo pip3 install -e .; cd ..

clean:
	@rm -rf .buildozer

clone_dev:
	@rm -rf src/bitdust/
	@git clone https://github.com/bitdust-io/devel.git ./src/bitdust/

clone:
	@rm -rf src/bitdust/
	@git clone https://github.com/bitdust-io/public.git ./src/bitdust/

pull:
	@cd ./src/bitdust/
	@git pull origin master
	@cd ..

clone_p4a:
	@rm -rf python-for-android/
	@git clone -b v2019.08.09 --single-branch https://github.com/kivy/python-for-android.git python-for-android/

recipes_fix:
	cp -R -f -v recipes/* ./python-for-android/pythonforandroid/recipes/.

build:
	@buildozer -v android debug

