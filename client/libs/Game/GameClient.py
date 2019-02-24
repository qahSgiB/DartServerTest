import socket
import time

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
    def __init__(self, address, port, outputEnabled=False, baseDataLength=1024, baseDataLengthMaxMultiplayerDigits=3):
        self.address = address
        self.port = port
        self.id = None

        self.outputEnabled = outputEnabled

        self.baseDataLength = baseDataLength
        self.baseDataLengthMaxMultiplayerDigits = baseDataLengthMaxMultiplayerDigits

        self.socket = socket.socket()

    def output(self, text):
        if self.outputEnabled:
            print(text)

    def begin(self):
        self.socket.connect((self.address, self.port))

        self.output('Connected')

        message = self.communicate('beginCommunication', {})

        self.id = message['id']

        self.output('Begin | id:{id}'.format(id=self.id))

        return message

    def end(self):
        endCommunicationMessage = self.communicate('endCommunication', {})

        self.output('Disconnected')

        self.socket.close()

    @JSONEncoding.decodeDecorator
    def recieveData(self):

        data = b''

        while data == b'':
            data = self.socket.recv(self.baseDataLength)

        data = str(data.decode('utf-8'))

        dataMult = int(data[0:self.baseDataLengthMaxMultiplayerDigits])
        data = data[self.baseDataLengthMaxMultiplayerDigits:]

        for i in range(dataMult-1):
            time.sleep(0.005)

            newData = self.socket.recv(self.baseDataLength)
            newData = str(newData.decode('utf-8'))
            data += newData

        return data

    @JSONEncoding.encodeDecoratorX(True)
    def sendData(self, message):
        message += '_'
        data = message.encode('utf-8')

        self.socket.sendall(data)

    def communicate(self, title, sendData):
        sendMessage = {
            'title': title,
            'data': sendData,
        }

        self.sendData(sendMessage)
        message = self.recieveData()

        return message
