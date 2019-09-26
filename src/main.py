#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

__version__ = '0.4'

import os
import sys
import time
import platform

import kivy
kivy.require('1.9.1')  # replace with your current kivy version !
# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


from kivy.app import App
from kivy.uix.label import Label


class AndroidServerApp(App):
    
    def build(self):
        print('AndroidServerApp.build')
        self.label = Label(text="server started\n")
        return self.label

    def on_start(self):
        # /data/user/0/org.kivy.bitdust/files/app/
        print('AndroidServerApp.on_start %s' % list(platform.uname()))

        sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'bitdust'))

        print('\n'.join(sys.path))

        # from main.bpmain import main
        # ret = main(executable_path='.', start_reactor=False)

        from twisted.web import server, resource
        from twisted.internet import reactor
        
        class Simple(resource.Resource):
            isLeaf = True
            def render_GET(self, request):
                return "<html>Hello, world!</html>"
        
        site = server.Site(Simple())
        reactor.listenTCP(8080, site)
        # reactor.run()

    def do_quit(self):
        print("AndroidServerApp.do_quit")
        # Kivy
        AndroidServerApp.get_running_app().stop()
        # Extinction de tout
        os._exit(0)


if __name__ == "__main__":
    AndroidServerApp().run()
    print('AndroidServerApp FINISHED')
