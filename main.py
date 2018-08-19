from utils import read_file_line_by_line, Solution, logger
from rules import CODEX, COURT, COD
import time

gen = read_file_line_by_line('mew.txt', 'cp1251')
#gen = read_file_line_by_line('aaaa.txt')
solution_list = []
i = 0
while True:
    solution = next(gen)
    if solution == 'stop':
        print('end read')
        break
    if solution.find('установил:') == -1 or solution.find('постановил:') == -1:
        continue
    solution_parse = solution.split('установил:')[1]
    solution_parse = solution_parse.split('постановил:')[0]
    solution_list.append(Solution(text=solution_parse, RULES=[CODEX], name='sol_'+str(i)))
    i+=1

t1 = time.time()
[(sol.start()) for sol in solution_list]
logger.info('all thread starts')
[(sol.join()) for sol in solution_list]
t2 = time.time()
logger.info('time of work: ' + str(t2 - t1))
print(t2-t1)
logger.info('all thread ends')
[sol.show_log() for sol in solution_list]
[sol.show() for sol in solution_list]




