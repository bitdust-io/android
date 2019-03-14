from __future__ import absolute_import

__version__ = '0.1'

import os
import sys
import time

import kivy
kivy.require('1.10.1')  # replace with your current kivy version !
# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


from kivy.app import App
from kivy.uix.label import Label


class BitDustService(App):

    def build(self):
        print('LAUNCHING BitDustService')
        self.start_service()

    def start_service(self):
        self.service = None

        if sys.platform == 'android' or sys.platform == 'linux3':
            from android import AndroidService
            service = AndroidService('BitDustServerApp', 'running')  
            # this will launch what is in the folder service/main.py as a service
            service.start('BitDustServerApp service started')
            self.service = service

        else:
            executable_path = os.getcwd()
            try:
                os.chdir('./src/bitdust')
            except:
                pass
            from bitdust.main.bpmain import main
            main(executable_path='./src/bitdust', start_reactor=False)

    def stop_service(self):
        if self.service:
            self.service.stop()
            self.service = None

    def on_stop(self):  # TODO: does not work! We need to close the service on leaving!
        self.stop_service()


class TwistedServerApp(App):

    label = None

    def build(self):
        self.label = Label(text="server started\n")
        return self.label

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.label.text = "received:  {}\n".format(msg)

        if msg == "ping":
            msg = "Pong"
        if msg == "plop":
            msg = "Kivy Rocks!!!"
        self.label.text += "responded: {}\n".format(msg)
        return msg.encode('utf-8')


if __name__ == '__main__':
    bitdust_server = BitDustService()
    bitdust_server.build()
    #bitdust_server.run()
    time.sleep(0.1)
    bitdust_server.stop_service()  # workaround because service might still be running on exit
    time.sleep(0.5)
    bitdust_server.start_service()
    time.sleep(0.1)

    TwistedServerApp().run()
