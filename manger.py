from utils import read_file_line_by_line, logger, Worker
import time
import ast

IP_ADDRESSES = [('127.0.0.1', 2020)]
gen = read_file_line_by_line('mew.txt', 'cp1251')
# gen = read_file_line_by_line('aaaa.txt')

workers = [Worker(address=addr, name='worker_' + str(i)) for i, addr in enumerate(IP_ADDRESSES)]

solution_list = []
result = []
i = 0
t1 = time.time()
while True:
    solution = next(gen)
    if solution == 'stop':
        print('end read', i)
        break
    if solution.find('установил:') == -1 or solution.find('постановил:') == -1:
        continue
    solution_parse = solution.split('установил:')[1]
    solution_parse = solution_parse.split('постановил:')[0]
    solution_list.append(solution_parse)
    i += 1
    if i % 10 == 0:
        message = str(solution_list)
        print(i)
        solution_list = []
        while message:
            time.sleep(0.5)
            for worker in workers:
                if False == worker.working:
                    print('new ', i)
                    if worker.result != '':
                        result.append(ast.literal_eval(worker.result))
                        [print(res) for res in result]
                    worker.start(message)
                    message = ''

[print(res) for res in result]
t2 = time.time()
logger.info('time of work: ' + str(t2 - t1))
print(t2 - t1)
