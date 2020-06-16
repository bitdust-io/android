from kivy.uix.widget import Widget  # @UnresolvedImport
from kivy.event import EventDispatcher  # @UnresolvedImport

from runnable import run_on_ui_thread  # @UnresolvedImport

from jnius import autoclass  # @UnresolvedImport

LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
View = autoclass('android.view.View')
Uri = autoclass('android.net.Uri')
Array = autoclass('java.lang.reflect.Array')

# PythonActivity = autoclass('org.kivy.android.PythonActivity')
PythonActivity = autoclass('org.bitdust_io.bitdust1.BitDustActivity')


PACKAGE_NAME = 'org.bitdust_io.bitdust1'

# SERVICE_STARTED_MARKER_FILENAME = f'/data/user/0/{PACKAGE_NAME}/local_web_server'


class WebviewEngine(Widget, EventDispatcher): 

    is_visible = True

    _webview_obj = None

    def __init__(self, **kwargs):       
        super(WebviewEngine, self).__init__(**kwargs)
        # Clock.schedule_once(self.create_webview, 0)
        self.create_webview()

    def __getattr__(self, method_name):
        print('WebviewEngine.__getattr__ %r' % method_name)
        if method_name == 'f2':
            return None
        if method_name in ['_context',]:
            return None
        if hasattr(self._webview_obj, method_name):
            try:
                call_method = lambda *x: getattr(self._webview_obj, method_name)(*x) 
                return call_method
            except Exception as exc:
                print('WebviewEngine.__getattr__ error :', exc)
                raise exc
        else:
            raise Exception("Method %s not define" % method_name)

    @run_on_ui_thread
    def create_webview(self, *args):
        print('WebviewEngine.create_webview', args, PythonActivity.mActivity, PythonActivity)
        if(self._webview_obj):
            print('WebviewEngine.create_webview _webview_obj already exist: %r' % self._webview_obj)
            return True
        PythonActivity.mActivity.createWebView()
        self._webview_obj = PythonActivity.mActivity.webView
        # self._webview_obj.loadUrl(f'file:///data/user/0/{PACKAGE_NAME}/files/app/www/index.html')
