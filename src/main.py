from __future__ import absolute_import
import os

import kivy
kivy.require('1.10.1')  # replace with your current kivy version !
# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


from kivy.app import App
from kivy.uix.label import Label


def start_bitdust():
    executable_path = os.getcwd()
    try:
        os.chdir(os.path.dirname(__file__))
    except:
        pass
    from main.bpmain import main
    main(executable_path=executable_path, start_reactor=False)


class TwistedServerApp(App):

    label = None

    def build(self):
        start_bitdust()
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
    TwistedServerApp().run()
