import asyncio
from yargy import Parser
import random
import time
import logging
import re
from multiprocessing import Process, Pool
from multiprocessing.dummy import  Pool as ThPool, Process as Thread
import pathos.pools as pp

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
                line += l
            if line == '' or line == '\n':
                break
            line = line.lower().replace(',', '')
            yield line
        logger.info('file read end now')
        yield 'stop'


class Solution(object):
    def __init__(self, text, RULES, name):
        self.name = name
        self.text_to_parse = text
        self.links = []
        self.RULES = RULES
        self.thread_list = [Process(name=name + 'thread_' + str(_), target=self.find_all,
                                    args=(line, self.RULES, name + ' thread' + str(_)))
                            if self.match(line) else False
                            for (_, line) in enumerate(self.text_to_parse.split('\n'))]

    def find_all(self, text, GR, thread_name):
        """
        :param text: line of solution to analise
        :param GR: RULE
        :param thread_name: name of thread
        :return:
        """
        ans = []
        if text == '\n':
            return
        t1 = time.time()
        for gr in GR:
            for match in Parser(gr).findall(text):
                ans.append([_.value for _ in match.tokens])
        if ans:
            self.links.append(ans)
        t2 = time.time()
        logger.info(thread_name + ': ' + str(ans))
        logger.info('time of work current ' + thread_name + ': ' + str(t2 - t1))

    def start(self):
        [thread.start() if thread else False for thread in self.thread_list]

    def join(self):
        [thread.join() if thread else False for thread in self.thread_list]

    def show_log(self):
        [logger.debug(link) for link in self.links]

    def show(self):
        [print(link) for link in self.links]

    @staticmethod
    def match(text):
        pattern1 = r'(пункт|подпункт|част|раздел|подраздел|глав|стат|абзац)+(' \
                   r'а|у|и|ы|ой|ьей|ьёй|ью|ьям|ям|ье|ом|ам|ах|е|ов|ей|ьях|ях|ьи|ья|ь|)* '
        pattern2 = r'\b(ч|п|ст|пп)+(\.|\b)+'

        if re.search(pattern1, text) is not None or re.search(pattern2, text) is not None:
            return True
        else:
            return False


class My_pool(object):
    def __init__(self, list_of_solutions, count_of_threads):
        self.solutions = list_of_solutions
        list_of_threads = []
        for solution in self.solutions:
            list_of_threads = list_of_threads + solution.thread_list
        random.shuffle(list_of_threads)
        self.thread_list = list_of_threads
        self.max_count = count_of_threads

    def start(self):
        i = 0
        thread_stac = set()
        for thread in self.thread_list:
            if not thread:
                continue
            thread_stac.add(thread)
            thread.start()
            i += 1
            thread_to_kill = Process()
            while i >= self.max_count:
                for thread_ in thread_stac:
                    if not thread_.is_alive():
                        thread_to_kill = thread_
                        i -= 1
                        break
            print(thread_to_kill.name, len(thread_stac))
            thread_stac.discard(thread_to_kill)