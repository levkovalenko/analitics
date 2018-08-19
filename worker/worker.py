from worker_utils import Solution, logger
from worker_rule import CODEX
import time
import socket
import ast

worker_sock = socket.socket()
worker_sock.bind(('127.0.0.1', 2020))
worker_sock.listen(1)


def recvire(conn):
    text = b''
    while True:
        data = conn.recv(1024)
        if not data:
            break
        text += data
        if len(data) < 1024:
            break
    text = text.decode()
    return text


def work(conn):
    solutions = recvire(conn)
    solution_list = [Solution(text=sol, RULES=[CODEX], name='sol_' + str(i))
                     for i, sol in enumerate(ast.literal_eval(solutions))]
    t1 = time.time()

    [(sol.start()) for sol in solution_list]
    logger.info('all thread starts')
    [(sol.join()) for sol in solution_list]

    t2 = time.time()
    logger.info('time of work: ' + str(t2 - t1))
    print(t2 - t1)

    logger.info('all thread ends')

    [sol.show_log() for sol in solution_list]
    [sol.show() for sol in solution_list]
    links = str([sol.get_links() for sol in solution_list]).encode()
    conn.send(links)
    conn.close()


while True:
    connection, address = worker_sock.accept()
    print(address)
    work(connection)







