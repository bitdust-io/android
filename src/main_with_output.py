import os
import sys
import time
import shlex
import subprocess
import threading

from kivy.base import runTouchApp, stopTouchApp
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.properties import (
    ObjectProperty, ListProperty, StringProperty, NumericProperty, Clock, partial
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

STDOUT_FILE = 'stdout'
STDERR_FILE = 'stderr'


Builder.load_string('''
<KivyConsole>:

    orientation: "vertical"
    # spacing: "2dp"
    # padding: root.width * .01, root.height * .01
    font_size: "8pt"

    console_input: console_input
    scroll_view: scroll_view

    ScrollView:
        id: scroll_view
        ConsoleInput:
            id: console_input
            multiline: True
            shell: root
            focus: True
            readonly: True
            size_hint: (1, None)
            font_name: root.font_name
            font_size: root.font_size
            foreground_color: root.foreground_color
            background_color: root.background_color
            height: max(self.parent.height, self.minimum_height)

    ButtonDeploy:
        id: "root_button_deploy_0"
        shell: root
        text: "Deploy"
        size_hint_y: None
        height: self.parent.height * 0.03
        # background_color: (0.0, 1.0, 0.0, 1.0)

    ButtonClone:
        id: "root_button_clone_0"
        shell: root
        text: "Clone"
        size_hint_y: None
        height: self.parent.height * 0.03
        # background_color: (0.0, 1.0, 0.0, 1.0)

    ButtonConfigure:
        id: "root_button_clone_0"
        shell: root
        text: "Configure"
        size_hint_y: None
        height: self.parent.height * 0.03
        # background_color: (0.0, 1.0, 0.0, 1.0)

    ButtonStart:
        id: "root_button_start_0"
        shell: root
        text: "Start"
        size_hint_y: None
        height: self.parent.height * 0.03
        background_color: (0.0, 1.0, 0.0, 1.0)

    ButtonStop:
        id: "root_button_stop_0"
        shell: root
        text: "Stop"
        size_hint_y: None
        height: self.parent.height * 0.03
        background_color: (1.0, 0.0, 0.0, 1.0)

    ButtonExit:
        id: "root_button_exit_0"
        shell: root
        text: "Exit"
        size_hint_y: None
        height: self.parent.height * 0.03
        # background_color: (1.0, 0.0, 0.0, 1.0)

''')

def threaded(fn):
    def wrapper(*args, **kwargs):
        th = threading.Thread(target=fn, args=args, kwargs=kwargs)
        th.start()
        return th
    return wrapper


class Shell(EventDispatcher):
    __events__ = ('on_output', 'on_complete', 'on_exit', )

    process = ObjectProperty(None)

    def wait_command(self, command, show_output=True, callback=None, *args):
        try:
            self.process = subprocess.Popen(
                command,
                stdout=open(STDOUT_FILE, 'wb'),
                stderr=open(STDERR_FILE, 'wb'),
                universal_newlines=True,
            )
        except Exception as exc:
            self.dispatch('on_output', ('ERROR in [' + command + '] result: ' + str(exc)))
        return self.process

    @threaded
    def fire_command(self, command, show_output=True, callback=None, *args):
        return self.wait_command(command, show_output=show_output, callback=callback, *args)

    @threaded
    def stop(self, *args):
        if self.process:
            self.process.kill()

    def _run_cmd(self, cmd, cb=None, *args):
        _posix = True
        if sys.platform[0] == 'w':
            _posix = False
        # self.text += '\n>>> ' + str(cmd) + '\n'
        self.dispatch('on_output', ('>>> ' + str(cmd)))
        commands = shlex.split(str(cmd), posix=_posix)
        prc = self.fire_command(commands, callback=cb)
        return prc


class ButtonDeploy(Button):
    """
    """

    shell = ObjectProperty(None)

    def on_release(self):
        self.shell._run_cmd('/bin/sh src/bitdust.sh -c deploy -i "%s"' % sys.argv[0])
        return Button.on_release(self)


class ButtonClone(Button):
    """
    """

    shell = ObjectProperty(None)

    def on_release(self):
        self.shell._run_cmd('/bin/sh src/bitdust.sh -c clone -i "%s"' % sys.argv[0])
        return Button.on_release(self)


class ButtonConfigure(Button):
    """
    """

    shell = ObjectProperty(None)

    def on_release(self):
        self.shell._run_cmd('/bin/sh bitdust.sh -c config -i "%s"' % sys.argv[0])
        return Button.on_release(self)


class ButtonStart(Button):
    """
    """

    shell = ObjectProperty(None)

    def on_release(self):
        self.shell._run_cmd('/bin/sh bitdust.sh -c start -i "%s"' % sys.argv[0])
        return Button.on_release(self)


class ButtonStop(Button):
    """
    """

    shell = ObjectProperty(None)

    def on_release(self):
        self.shell._run_cmd('/bin/sh bitdust.sh -c stop -i "%s"' % sys.argv[0])


class ButtonExit(Button):
    """
    """

    shell = ObjectProperty(None)

    def on_release(self):
        stopTouchApp()


class ConsoleInput(TextInput):
    '''Displays Output and sends input to Shell. Emits 'on_ready_to_input'
       when it is ready to get input from user.
    '''

    shell = ObjectProperty(None)
    '''Instance of KivyConsole(parent) widget
    '''

    def __init__(self, **kwargs):
        super(ConsoleInput, self).__init__(**kwargs)
        self.lines = 0
        self._init_console()
        Clock.schedule_once(self._init_output)
        Clock.schedule_once(self._print_header)

    def _print_header(self, *args):
        out_fd = open('stdout', 'a')
        out_fd.write('Argv: ' + str(sys.argv) + '\n')
        out_fd.write('Argv[0] exist: ' + str(os.path.exists(os.path.abspath(sys.argv[0]))) + '\n')
        out_fd.write('Executable: ' + os.path.abspath(sys.executable) + '\n')
        out_fd.write('Is exist: ' + str(os.path.exists(os.path.abspath(sys.executable))) + '\n')
        # out_fd.write('Python Path: \n' + ('\n'.join(sys.path)))
        out_fd.write('executable: ' + str(os.path.abspath(sys.executable)) + '\n')
        # out_fd.write('list: ' + str(os.listdir(os.path.abspath(sys.executable))) + '\n')
        out_fd.close()

    def _init_console(self, *args):
        '''Create initial values for the prompt and shows it
        '''
        self.cur_dir = os.getcwd()
        self._hostname = 'kivy'
        try:
            if hasattr(os, 'uname'):
                self._hostname = os.uname()[1]
            else:
                self._hostname = os.environ.get('COMPUTERNAME', 'kivy')
        except Exception:
            pass
        self._username = os.environ.get('USER', '')
        if not self._username:
            self._username = os.environ.get('USERNAME', 'designer')

    def _init_output(self, *args):
        thread_read_stdout = threading.Thread(target=self.read_stdout)
        thread_read_stdout.daemon = True  # kill thread on app close
        thread_read_stdout.start()
        thread_read_stderr = threading.Thread(target=self.read_stderr)
        thread_read_stderr.daemon = True  # kill thread on app close
        thread_read_stderr.start()
        # self.shell._run_cmd('echo "%s" >> stdout' % sys.executable)
        # self.shell._run_cmd('echo "%s" >> stdout' % sys.argv[0])

    def read_stdout(self):
        try:
            out_fd = open(STDOUT_FILE, 'wb')
            out_fd.write(b'')
            out_fd.close()
        except:
            import traceback
            traceback.print_exc()
            self.shell.dispatch('on_output', 'Not able to erase "%s"' % STDOUT_FILE)
            return
        with open(STDOUT_FILE, 'r') as infile:
            while 1:
                where = infile.tell()
                line = infile.readline()
                if not line:
                    time.sleep(0.5)
                    infile.seek(where)
                else:
                    if self.shell:
                        self.shell.dispatch('on_output', line)

    def read_stderr(self):
        try:
            err_fd = open(STDERR_FILE, 'wb')
            err_fd.write(b'')
            err_fd.close()
        except:
            self.shell.dispatch('on_output', 'Not able to erase "%s"' % STDERR_FILE)
            return
        with open(STDERR_FILE, 'r') as infile:
            while 1:
                where = infile.tell()
                line = infile.readline()
                if not line:
                    time.sleep(0.5)
                    infile.seek(where)
                else:
                    if self.shell:
                        self.shell.dispatch('on_output', 'STDERR:' + line)

    def on_output(self, output):
        for ln in output.splitlines():
            try:
                if self.lines > 100:
                    self.lines = 0
                    self.text = ''
                self.lines += 1
                if ln:
                    try:
                        self.text += ((ln[:250].replace('\n', ' ') + '\n') or '\n')
                    except AttributeError:
                        pass
                else:
                    self.text += '\n'
            except:
                import traceback
                print(traceback.format_exc())
                self.text += 'ERROR:\n'
                for l in traceback.format_exc().splitlines():
                    self.text += '%r\n' % l

    def on_complete(self, command, returncode, output):
        pass


class KivyConsole(BoxLayout, Shell):

    console_input = ObjectProperty(None)
    '''Instance of ConsoleInput
       :data:`console_input` is an :class:`~kivy.properties.ObjectProperty`
    '''

    scroll_view = ObjectProperty(None)
    '''Instance of :class:`~kivy.uix.scrollview.ScrollView`
       :data:`scroll_view` is an :class:`~kivy.properties.ObjectProperty`
    '''

    foreground_color = ListProperty((1, 1, 1, 1))
    '''This defines the color of the text in the console
    :data:`foreground_color` is an :class:`~kivy.properties.ListProperty`,
    Default to '(.5, .5, .5, .93)'
    '''

    background_color = ListProperty((0, 0, 0, 1))
    '''This defines the color of the text in the console
    :data:`foreground_color` is an :class:`~kivy.properties.ListProperty`,
    Default to '(0, 0, 0, 1)'''

    font_name = StringProperty('data/fonts/droid-sans-mono.ttf')
    '''Indicates the font Style used in the console
    :data:`font` is a :class:`~kivy.properties.StringProperty`,
    Default to 'DroidSansMono'
    '''

    font_size = NumericProperty(14)
    '''Indicates the size of the font used for the console
    :data:`font_size` is a :class:`~kivy.properties.NumericProperty`,
    Default to '9'
    '''

    def __init__(self, **kwargs):
        super(KivyConsole, self).__init__(**kwargs)

    def on_output(self, output):
        '''Event handler to send output data
        '''
        self.console_input.on_output(output)
        self.scroll_view.scroll_y = 0

    def on_complete(self, command, returncode, output):
        '''Event handler to send output data
        '''
#         stopTouchApp()

    def on_exit(self, output):
        """
        """


if __name__ == '__main__':
    runTouchApp(KivyConsole())
