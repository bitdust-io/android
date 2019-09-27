# coding: utf8
__version__ = '0.2'

import kivy
kivy.require('1.9.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform

from jnius import autoclass


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.bitdust_io.bitdust',
    servicename=u'Bitdustnode'
)


KV = '''
BoxLayout:
    BoxLayout:
        size_hint_y: None
        height: '50sp'
        Button:
            text: 'start service'
            on_press: app.start_service()
        Button:
            text: 'stop service'
            on_press: app.stop_service()
'''


class BitDustApp(App):

    def build(self):
        print('BitDustApp.build')
        self.service = None
        self.root = Builder.load_string(KV)
        return self.root

    def on_resume(self):
        print('BitDustApp.on_resume')
        if self.service:
            self.start_service()

    def start_service(self, finishing=False):
        print('BitDustApp.start_service finishing=%r' % finishing)
        service = autoclass(SERVICE_NAME)
        mActivity = autoclass(u'org.kivy.android.PythonActivity').mActivity
        argument = ''
        if finishing:
            argument = '{"stop_service": 1}'
        service.start(mActivity, argument)
        if finishing:
            self.service = None
            print('BitDustApp.start_service expect to be STOPPED now')
        else:
            self.service = service
            print('BitDustApp.start_service STARTED : %r' % self.service)

    def stop_service(self):
        print('BitDustApp.stop_service %r' % self.service)
        service = autoclass(SERVICE_NAME)
        mActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        service.stop(mActivity)
        self.start_service(finishing=True)
        print('BitDustApp.stop_service STOPPED')


if __name__ == '__main__':
    BitDustApp().run()
