import os
import json

from twisted.internet import reactor

# import logging
# logging.basicConfig(level=logging.DEBUG)

# from twisted.internet.defer import setDebugging
# setDebugging(True)

# from twisted.python.log import startLogging
# startLogging(sys.stdout)

from jnius import autoclass  # @UnresolvedImport


def set_auto_restart_service(restart=True):
    print('set_auto_restart_service restart=%r' % restart)
    service = autoclass('org.kivy.android.PythonService').mService
    service.setAutoRestartService(restart)


def set_foreground():
    print('set_foreground')
    channel_id = 'org.bitdust_io.bitdust.Bitdustnode'
    Context = autoclass(u'android.content.Context')
    Intent = autoclass(u'android.content.Intent')
    PendingIntent = autoclass(u'android.app.PendingIntent')
    AndroidString = autoclass(u'java.lang.String')
    NotificationBuilder = autoclass(u'android.app.Notification$Builder')
    NotificationManager = autoclass(u'android.app.NotificationManager')
    NotificationChannel = autoclass(u'android.app.NotificationChannel')
    notification_channel = NotificationChannel(channel_id, AndroidString('BitDust Channel'.encode('utf-8')), NotificationManager.IMPORTANCE_HIGH)
    Notification = autoclass(u'android.app.Notification')
    service = autoclass('org.kivy.android.PythonService').mService
    PythonActivity = autoclass(u'org.kivy.android.PythonActivity')
    notification_service = service.getSystemService(Context.NOTIFICATION_SERVICE)
    notification_service.createNotificationChannel(notification_channel)
    app_context = service.getApplication().getApplicationContext()
    notification_builder = NotificationBuilder(app_context, channel_id)
    title = AndroidString("BitDust".encode('utf-8'))
    message = AndroidString("Application is running in background".encode('utf-8'))
    notification_intent = Intent(app_context, PythonActivity)
    notification_intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_SINGLE_TOP | Intent.FLAG_ACTIVITY_NEW_TASK)
    notification_intent.setAction(Intent.ACTION_MAIN)
    notification_intent.addCategory(Intent.CATEGORY_LAUNCHER)
    intent = PendingIntent.getActivity(service, 0, notification_intent, 0)
    notification_builder.setContentTitle(title)
    notification_builder.setContentText(message)
    notification_builder.setContentIntent(intent)
    notification_builder.setOngoing(True)
    notification_builder.setPriority(NotificationManager.IMPORTANCE_MIN)
    Drawable = autoclass(u"{}.R$drawable".format(service.getPackageName()))
    icon = getattr(Drawable, 'icon')
    notification_builder.setSmallIcon(icon)
    notification_builder.setAutoCancel(True)
    notification_builder.setCategory(Notification.CATEGORY_SERVICE)
    new_notification = notification_builder.getNotification()
    service.startForeground(1, new_notification)
    print('set_foreground DONE : %r' % service)


def start_bitdust():
    executable_path = os.getcwd()
    print('start_bitdust executable_path=%r' % executable_path)
    try:
        os.chdir('bitdust')
    except:
        pass
    print('executable_path after : %r' % os.getcwd())
    from main.bpmain import main
    reactor.callLater(0.01, main, executable_path, start_reactor=False)  # @UndefinedVariable
    return True


def run_service():
    argument = os.environ.get('PYTHON_SERVICE_ARGUMENT', 'null')
    argument = json.loads(argument) if argument else None
    argument = {} if argument is None else argument
    print('argument %r' % argument)

    if argument.get('stop_service'):
        print('service to be stopped')
        return

    try:
        set_foreground()

        # set_auto_restart_service(True)

        reactor.callWhenRunning(start_bitdust)  # @UndefinedVariable
        reactor.run()  # @UndefinedVariable

        print('Twisted reactor stopped')

        # set_auto_restart_service(False)
    except Exception as exc:
        print('Exception in run_service() : %r' % exc)

        # avoid auto-restart loop
        # set_auto_restart_service(False)


if __name__ == '__main__':
    run_service()
    print('EXIT')
