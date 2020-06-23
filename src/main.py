import os

from kivy.app import App  # @UnresolvedImport
from kivy.clock import Clock  # @UnresolvedImport
from kivy.properties import BooleanProperty  # @UnresolvedImport
from kivy.core.window import Window  # @UnresolvedImport

from jnius import autoclass  # @UnresolvedImport

from android.permissions import request_permissions, Permission  # @UnresolvedImport

from webviewengine import WebviewEngine

import encodings.idna

PACKAGE_NAME = 'org.bitdust_io.bitdust1'

SERVICE_NAME = '{packagename}.Service{servicename}'.format(
    packagename=PACKAGE_NAME,
    servicename='Bitdustnode'
)

# SERVICE_STARTED_MARKER_FILENAME = f'/data/user/0/{PACKAGE_NAME}/local_web_server'

APP_STARTUP_PERMISSIONS = [
    Permission.INTERNET,
    Permission.READ_EXTERNAL_STORAGE,
    Permission.WRITE_EXTERNAL_STORAGE,
    Permission.FOREGROUND_SERVICE,
]


# PythonActivity = autoclass('org.kivy.android.PythonActivity')
PythonActivity = autoclass('org.bitdust_io.bitdust1.BitDustActivity')


class BitDustApp(App):

    webviewEngine = None
    can_go_back = BooleanProperty(False)
    can_go_forward = BooleanProperty(False)

    def __init__(self,**kwargs):
        self.service = None
        super(BitDustApp,self).__init__(**kwargs)
        Clock.schedule_once(self._on_init_complete)

    def _on_init_complete(self,*args):
        if(self.webviewEngine is not None):
            print('BitDustApp._on_init_complete already engine started')
            return 
        print('BitDustApp._on_init_complete starting WebviewEngine')
#         if os.path.isfile(SERVICE_STARTED_MARKER_FILENAME):
#             os.remove(SERVICE_STARTED_MARKER_FILENAME)
#             print('BitDustApp._on_init_complete file erased:', SERVICE_STARTED_MARKER_FILENAME)
        if not self.webviewEngine:
            print('BitDustApp._on_init_complete   new WebviewEngine window to be created')
            self.webviewEngine = WebviewEngine()
            Window.add_widget(self.webviewEngine)
        else:
            print('BitDustApp._on_init_complete   WebviewEngine window already exist')
        # self.webviewEngine.bind(on_page_started=self.proccess_on_page_start)
        # self.webviewEngine.bind(on_page_commit_visible=self.proccess_on_page_commit_visible)

    def build(self):
        ret = super(BitDustApp, self).build()
        print('BitDustApp.build return %r' % ret)
        return ret

#     def proccess_go_back(self):
#         print('BitDustApp.proccess_go_back')
#         if(self.can_go_back == True):
#             self.webviewEngine.goBack()

#     def proccess_go_forward(self):
#         print('BitDustApp.proccess_go_forward')
#         if(self.can_go_forward == True):
#             self.webviewEngine.goForward()

#     def proccess_on_page_start(self, *args, **kwargs):
#         print('BitDustApp.proccess_on_page_start %r %r' % (args, kwargs))

#     def proccess_on_page_commit_visible(self, *args, **kwargs):
#         print('BitDustApp.proccess_on_page_commit_visible %r %r' % (args, kwargs))
#         self.can_go_back = self.webviewEngine.canGoBack()
#         self.can_go_forward = self.webviewEngine.canGoForward()

    def on_start(self):
        print('BitDustApp.on_start')
        # self.request_app_permissions()
        # self.create_notification_channel()
        self.start_service()

    def on_stop(self):
        print('BitDustApp.on_stop')

    def on_pause(self):
        print('BitDustApp.on_pause')
        # if self.webviewEngine:
        #     if self.webviewEngine._webview_obj:
        #         self.webviewEngine._webview_obj.loadUrl(f'file:///data/user/0/{PACKAGE_NAME}/files/app/www/img/logo-pictogram-white.61b08a81.png')
        return True

    def on_resume(self):
        print('BitDustApp.on_resume')
        # self.start_service()
        # if self.webviewEngine:
        #     if self.webviewEngine._webview_obj:
        #         self.webviewEngine._webview_obj.loadUrl(f'file:///data/user/0/{PACKAGE_NAME}/files/app/www/index.html')

    def start_service(self, finishing=False):
        print('BitDustApp.start_service finishing=%r' % finishing)
        service = autoclass(SERVICE_NAME)
        mActivity = PythonActivity.mActivity
        argument = ''
        if finishing:
            argument = '{"stop_service": 1}'
        print('BitDustApp.start_service: %r' % type(service))
        service.start(mActivity, argument)
        print('BitDustApp.start_service OK')
        if finishing:
            self.service = None
            print('BitDustApp.start_service expect to be STOPPED now')
        else:
            self.service = service
            print('BitDustApp.start_service STARTED : %r' % self.service)

    def stop_service(self):
        print('BitDustApp.stop_service %r' % self.service)
        service = autoclass(SERVICE_NAME)
        service.stop(PythonActivity.mActivity)
        self.start_service(finishing=True)
        print('BitDustApp.stop_service STOPPED')

    def request_app_permissions(self, list_permissions=[]):
        global APP_STARTUP_PERMISSIONS
        print('BitDustApp.request_app_permissions')
        ret = request_permissions(list_permissions or APP_STARTUP_PERMISSIONS)
        print('BitDustApp.request_app_permissions : %r' % ret)

    def create_notification_channel(self):
        """
        Not used.
        """
        print('BitDustApp.create_notification_channel')
        channel_id = f'{PACKAGE_NAME}.Bitdustnode'
        AndroidString = autoclass(u'java.lang.String')
        Context = autoclass(u'android.content.Context')
        NotificationManager = autoclass(u'android.app.NotificationManager')
        NotificationChannel = autoclass(u'android.app.NotificationChannel')
        notification_channel = NotificationChannel(channel_id, AndroidString('BitDust Channel'.encode('utf-8')), NotificationManager.IMPORTANCE_HIGH)
        notification_service = PythonActivity.mActivity.getSystemService(Context.NOTIFICATION_SERVICE)
        new_channel = notification_service.createNotificationChannel(notification_channel)
        print('BitDustApp.create_notification_channel new_channel=%r' % new_channel)


if __name__ == '__main__':
    BitDustApp().run()
