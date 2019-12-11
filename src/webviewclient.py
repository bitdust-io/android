from jnius import autoclass, PythonJavaClass, java_method  # @UnresolvedImport

CustomJavaWebviewClient = autoclass('com.razzbee.WebviewEngine.CustomWebviewClient')


def WebviewClient(WebviewEngineObj):
    print('WebviewClient %r' % WebviewEngineObj)
    WebviewClientCoreClass = WebviewClientCore(WebviewEngineObj)
    WebviewClientResults = CustomJavaWebviewClient(WebviewClientCoreClass)
    return WebviewClientResults


class WebviewClientCore(PythonJavaClass):

    __javacontext__ = 'app'

    __javainterfaces__ = ['com.razzbee.WebviewEngine.CustomWebviewClientInterface']

    def __init__(self, webview_engine_obj):
        print('WebviewClientCore.__init__ %r' % webview_engine_obj)
        super(WebviewClientCore, self).__init__()
        self._webviewEngine = webview_engine_obj

    @java_method('(Landroid/webkit/WebView;Ljava/lang/String;)Z')
    def shouldOverrideUrlLoading(self, view, url):
        print('WebviewClientCore.shouldOverrideUrlLoading')
        self._webviewEngine.dispatch_event('on_should_override_url_loading', webview=view, url=url)

    @java_method('(Landroid/webkit/WebView;Ljava/lang/String;Landroid/graphics/Bitmap;)V')
    def onPageStarted(self, view, url, favicon):
        print('WebviewClientCore.onPageStarted')
        self._webviewEngine.dispatch_event('on_page_started', webview=view, url=url, favicon=favicon)

    @java_method('(Landroid/webkit/WebView;Ljava/lang/String;)V')
    def onPageFinished(self, view, url):
        print('WebviewClientCore.onPageFinished')
        self._webviewEngine.dispatch_event('on_page_finished', webview=view, url=url)

    @java_method('(Landroid/webkit/WebView;Ljava/lang/String;)V')
    def onPageCommitVisible(self, view, url):
        print('WebviewClientCore.onPageCommitVisible')
        self._webviewEngine.dispatch_event('on_page_commit_visible', webview=view, url=url)

    @java_method('(Landroid/webkit/WebView;Ljava/lang/Integer;Ljava/lang/String;Ljava/lang/String;)V')
    def onReceivedError(self, view, errorCode, description, failingUrl):
        print('WebviewClientCore.onReceivedError %r %r %r %r' % (view, errorCode, description, failingUrl))
        self._webviewEngine.dispatch_event('on_received_error', webview=view, error_code=errorCode, description=description, failing_url=failingUrl)
