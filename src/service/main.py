print('LALALALO')

# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


from twisted.internet import reactor
from twisted.internet import protocol

import sys


class BitDustServerApp():

    def build(self):
        executable_path = os.getcwd()
        try:
            os.chdir('./src/bitdust')
        except:
            pass
        from bitdust.main.bpmain import main
        main(executable_path='./src/bitdust', start_reactor=False)

    def handle_message(self, msg):
        #self.label.text = "received:  %s\n" % msg

        print('LALALALU')
        print(msg)
        if msg == "ping":
            msg = "pong"
        if msg == "plop":
            msg = "kivy rocks"
        #self.label.text += "responded: %s\n" % msg
        return msg


def run_server():
    serverapp = BitDustServerApp()
    serverapp.build()

if __name__ == '__main__':
    run_server()
