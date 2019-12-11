import time

from kivy.uix.widget import Widget  # @UnresolvedImport
from runnable import run_on_ui_thread  # @UnresolvedImport
from kivy.event import EventDispatcher  # @UnresolvedImport
from jnius import autoclass  # @UnresolvedImport
from webviewclient import WebviewClient

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
View = autoclass('android.view.View')


class WebviewEngine(Widget, EventDispatcher): 

    is_visible = True

    _webview_obj = None

    _webview_events = [
        'on_page_started',
        'on_page_finished',
        'on_received_error',
        'on_page_commit_visible',
        'on_should_override_url_loading',
    ]

    def __init__(self, **kwargs):       
        self.webviewWidth = kwargs.get('width') if 'width' in kwargs else LayoutParams.MATCH_PARENT
        self.webviewPosX = kwargs.get('posX') if 'posX' in kwargs else 0
        self.webviewPosY = kwargs.get('posY') if 'posY' in kwargs else 0
        self.webviewHeight = kwargs.get('height') if 'height' in kwargs else LayoutParams.MATCH_PARENT
        self._register_events()
        super(WebviewEngine, self).__init__(**kwargs)
        time.sleep(0.5)
        # Clock.schedule_once(self.create_webview, 0)
        self.create_webview()

    def dispatch_event(self, event_name, **kwargs):
        self.dispatch(event_name, **kwargs)
        print('WebviewEngine.dispatch_event %s' % event_name)

    def _event_default_handler(self, **kwargs):
        print('WebviewEngine._event_default_handler %r' % kwargs)

    def _register_events(self):
        print('WebviewEngine._register_events')
        events = self._webview_events
        for event_name in events:
            setattr(self, event_name, self._event_default_handler)
            self.register_event_type(event_name)

    def __getattr__(self, method_name):
        print('WebviewEngine.__getattr__ %r' % method_name)
        if method_name == 'f2':
            return None
        if method_name in ['_context',]:
            return None
        if hasattr(self._webview_obj,method_name):
            call_method = lambda *x: getattr(self._webview_obj,method_name)(*x) 
            return call_method
        else:
            raise Exception("Method %s not define" % method_name)

    @run_on_ui_thread
    def create_webview(self, *args):
        print('WebviewEngine.create_webview', args)
        if(self._webview_obj):
            print('WebviewEngine.create_webview _webview_obj already exist: %r' % self._webview_obj)
            return True
        webview = WebView(activity)
        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setAllowContentAccess(True)
        settings.setAllowFileAccessFromFileURLs(True)
        settings.setAllowUniversalAccessFromFileURLs(True)
        settings.setUseWideViewPort(True)
        settings.setLoadWithOverviewMode(True)
        settings.setSupportZoom(True)
        settings.setBuiltInZoomControls(False)
        webviewClient = WebviewClient(self)
        webview.setWebViewClient(webviewClient)
        webview.setX(self.webviewPosX)
        webview.setY(self.webviewPosY)
        activity.addContentView(webview, LayoutParams(self.webviewWidth,self.webviewHeight))
        self._webview_obj = webview
        print('WebviewEngine.create_webview is loading BitDust UI')
        self._webview_obj.loadUrl('file:///data/user/0/org.bitdust_io.bitdust/files/app/www/index.html')

    @run_on_ui_thread 
    def hide(self):
        print('WebviewEngine.hide _webview_obj=%r is_visible=%r' % (self._webview_obj, self.is_visible))
        if self._webview_obj is None and self.is_visible == False:
            return False
        self._webview_obj.setVisibility(View.GONE)
