import asyncio
import logging
import socket
from multiprocessing.dummy import Process
import time

logging.basicConfig(
    format=u' %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.DEBUG,
    filename='manager.log')
logger = logging


@asyncio.coroutine
def read_file_line_by_line(file_name, code='utf-8'):
    with open(file_name, 'r', encoding=code) as f:
        while True:
            line = ''
            for l in f:
                if '------------------------------------------------------------------' in l:
                    break
                line += l
            if line == '' or line == '\n':
                break
            line = line.lower().replace(',', '')
            yield line
        logger.info('file read end now')
        yield 'stop'


class Worker(object):
    def __init__(self, address, name):
        self.__address = address
        self.__socket = socket.socket()
        self.__name = name
        self.__working = False
        self.__process = None
        self.__result = ''

    @property
    def working(self):
        return self.__working

    @property
    def result(self):
        return self.__result

    def __connect__(self):
        self.__socket.connect(self.__address)

    def __send__(self, message):
        message = message.encode()
        self.__socket.send(message)

    def join(self):
        self.__process.join()

    def __recv__(self):
        text = b''
        while True:
            data = self.__socket.recv(8192)
            if not data:
                break
            text += data
            if len(data) < 8192:
                break
        text = text.decode()
        return text

    def __work__(self, message):
        t1 = time.time()
        self.__socket = socket.socket()
        self.__connect__()
        self.__send__(message)
        self.__result = self.__recv__()
        t2 = time.time()
        self.__socket.close()
        #logger.debug(self.__result)
        logger.debug(self.__name + ' end work at ' + str(t2-t1))
        self.__working = False

    def start(self, message):
        self.__result = ''
        self.__working = True
        self.__process = Process(target=self.__work__, args=(message,), name=self.__name + '_thread')
        self.__process.start()
