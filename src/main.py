# coding: utf8
__version__ = '0.2'

#------------------------------------------------------------------------------

import kivy
kivy.require('1.9.1')  # replace with your current kivy version !

#------------------------------------------------------------------------------

from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock

from jnius import PythonJavaClass, java_method, autoclass

from android.permissions import request_permissions, Permission
from android.runnable import run_on_ui_thread 

#------------------------------------------------------------------------------

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

#------------------------------------------------------------------------------

RootApp = None

#------------------------------------------------------------------------------

class BitDustUI(Widget):
    def __init__(self, **kwargs):
        super(BitDustUI, self).__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)

    @run_on_ui_thread
    def create_webview(self, *args, **kwargs):
        print('BitDustUI.create_webview')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        activity = autoclass('org.renpy.android.PythonActivity').mActivity
        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setUseWideViewPort(True) # enables viewport html meta tags
        settings.setLoadWithOverviewMode(True) # uses viewport
        settings.setSupportZoom(True) # enables zoom
        settings.setBuiltInZoomControls(True) # enables zoom controls
        wvc = WebViewClient()
        webview.setWebViewClient(wvc)
        activity.setContentView(webview)
        webview.loadUrl('https://bitdust.io')

#------------------------------------------------------------------------------

class BitDustApp(App):

    def build(self):
        print('BitDustApp.build')
        global RootApp
        RootApp = self
        self.icon = 'bitdust.png'
        self.service = None
        self.root = Builder.load_string(KV)
        self.ui = BitDustUI()
        self.root.add_widget(self.ui)
        return self.root

    def on_start(self):
        self.request_app_permissions()

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

    def request_app_permissions(self):
        ret = request_permissions([
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])
        print('BitDustApp.request_app_permissions : %r' % ret)

#------------------------------------------------------------------------------

if __name__ == '__main__':
    BitDustApp().run()
