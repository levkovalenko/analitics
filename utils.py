import asyncio
from yargy import Parser
from threading import Thread
import time
import logging
from multiprocessing import Process, Pool

logging.basicConfig(
    format=u' %(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.DEBUG,
    filename='tmp.log')
logger = logging


@asyncio.coroutine
def read_file_line_by_line(file_name, code='utf-8'):
    with open(file_name, 'r', encoding=code) as f:
        while True:
            line = ''
            for l in f:
                if '------------------------------------------------------------------' in l:
                    break
                line+=l
            print('a')
            print(line)
            if line == '' or line == '\n':
                break
            line = line.lower().replace(',', '')
            yield line
        logger.info('file read end now')
        yield 'stop'


class Solution(object):
    def __init__(self, text, RULES):
        self.text_to_parse = text
        self.links = []
        self.RULES = RULES
        self.thread_list = [Process(name='thread'+str(_), target=self.find_all,
                                   args=(line, self.RULES, 'thread'+str(_)))
                            for (_, line) in enumerate(self.text_to_parse.split('\n'))]

    def find_all(self, text, GR, thread_name):
        ans = []
        if text == '\n': return
        t1 =time.time()
        for gr in GR:
            for match in Parser(gr).findall(text):
                ans.append([_.value for _ in match.tokens])
        if ans != []:
            self.links.append(ans)
        t2 = time.time()
        logger.info(thread_name + ': ' + str(ans))
        logger.info('time of work current ' + thread_name + ': ' + str(t2 - t1))

    def start(self):
        [thread.start() for thread in self.thread_list]

    def join(self):
        [thread.join() for thread in self.thread_list]

    def show(self):
        [print(link) for link in self.links]