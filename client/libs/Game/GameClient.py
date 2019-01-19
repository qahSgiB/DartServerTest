import socket

from libs.DataStructures.LinkedList import LinkedList
from libs.Encoding import JSONEncoding



class SocketXList():
    def __init__(self):
        self.list_ = LinkedList()

    def getIndex(self, id):
        return self.list_.findIndex(lambda item: item.id == id)

    def add(self, item):
        self.list_.add(item)

class GameClient():
    def __init__(self, address, port, outputEnabled=False):
        self.address = address
        self.port = port
        self.id = None

        self.outputEnabled = outputEnabled

        self.socket = socket.socket()

    def output(self, text):
        if self.outputEnabled:
            print(text)

    def begin(self, responseDataLength=1024):
        self.socket.connect((self.address, self.port))

        self.output('Connected')

        message = self.communicate('beginCommunication', None, responseDataLength)

        self.id = message['id']

        self.output('Begin | id:{id}'.format(id=self.id))

        return message

    def end(self):
        self.output('Disconnected')

        endCommunicationMessag = self.communicate('endCommunication', {})

        self.socket.close()

    @JSONEncoding.decodeDecorator
    def recieveData(self, dataLength=1024):
        data = b''

        while data == b'':
            data = self.socket.recv(1024)

        return str(data.decode('utf-8'))

    @JSONEncoding.encodeDecoratorX(True)
    def sendData(self, message):
        data = message.encode('utf-8')

        self.socket.sendall(data)

    def communicate(self, title, sendData, responseDataLength=1024):
        sendMessage = {
            'title': title,
            'data': sendData,
        }

        self.sendData(sendMessage)
        message = self.recieveData(responseDataLength)

        return message
