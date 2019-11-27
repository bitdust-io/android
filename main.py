from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.core.window import Window

from android.permissions import request_permissions, Permission

from webviewengine import WebviewEngine  


SERVICE_NAME = u'{packagename}.Service{servicename}'.format(
    packagename=u'org.bitdust_io.bitdust',
    servicename=u'Bitdustnode'
)


class browserApp(App):
  
    webviewEngine = None

    #address box 
    address_bar = ObjectProperty(None)
    
    #can Go Back
    can_go_back = BooleanProperty(False)

    #can go forward 
    can_go_forward = BooleanProperty(False)


    def __init__(self,**kwargs):

        super(browserApp,self).__init__(**kwargs)
        
        Clock.schedule_once(self._on_init_complete)


    #When the constructor has finished proccessing 
    def _on_init_complete(self,*args):

        #address bar 
        # self.address_bar = self.ids.address_bar

        # self.top_right_nav = self.ids.top_right_nav 

        #lets check if webview object has been instantiated already
        if(self.webviewEngine is not None):
            return True 
        
        # webview_pos_y = self.ids.browser_toolbar.height

        # contentWin = self.ids.content_window

        # contentWinHeight = Window.height - (webview_pos_y + app_config.bottom_toolbar_height)
         
        # print('----!!___WInDOW WIDTH-------', Window.width) 

        #init webview engine 
        self.webviewEngine = WebviewEngine(
                                # posX=0,
                                # posY=webview_pos_y,
                                # width=Window.width,
                                # height=contentWinHeight
                                )
        
        #Add webview engine class as a widget
        # contentWin.add_widget(self.webviewEngine)
        Window.add_widget(self.webviewEngine)

        #Listen to events 
        # self.webviewEngine.bind(on_page_started=self.proccess_on_page_start)
        
        #On on_page_commit_visible
        self.webviewEngine.bind(on_page_commit_visible=self.proccess_on_page_commit_visible)

        # self.webviewEngine.bind(on_should_override_url_loading=self.on_should_override_url_loading)



    #proccess back button 
    def proccess_go_back(self):
        
        #if page can go back, then go back 
        if(self.can_go_back == True):
            self.webviewEngine.goBack()

    #Proccess Go Back 
    def proccess_go_forward(self):

        #if can go forward, then go 
        if(self.can_go_forward == True):
            self.webviewEngine.goForward()
    

#     #enable disable back and forward button
#     def proccess_on_page_start(self,*args,**kwargs):
#         
#         #change the url to the new url 
#         new_url = kwargs.get('url')
# 
#         if(new_url is not None):
#             self.update_address_bar_url(new_url)


    #proccess on Page Commit visible 
    def proccess_on_page_commit_visible(self,*args,**kwargs):

        #if the webview can go back, update the button
        self.can_go_back = self.webviewEngine.canGoBack()

        #check if it can go forward 
        self.can_go_forward = self.webviewEngine.canGoForward()



#     #should_override_url_loading
#     def on_should_override_url_loading(self,*args,**kwargs):
# 
#         #change the url to the new url 
#         new_url = kwargs.get('url')


    def on_start(self):
        print('BitDustApp.on_start')
        self.request_app_permissions()

    def on_pause(self):
        print('BitDustApp.on_pause')
        return True

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
        print('BitDustApp.request_app_permissions')
        ret = request_permissions([
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ])
        print('BitDustApp.request_app_permissions : %r' % ret)


if __name__ == '__main__':
    browserApp().run()

