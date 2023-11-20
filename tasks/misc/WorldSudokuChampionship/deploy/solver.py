import re
import time
from pwn import remote
from sudoku import Sudoku

round_regex = re.compile(r"ROUND \d+\n")

r = remote('127.0.0.1', 2806)
r.recv()
for i in range(250):
    data = (r.recvuntil(b'>>> \n')).decode("utf-8")

    board_data_start = round_regex.search(data).end()
    board_data = data[board_data_start + 1:-6]
    board = board_data.split("\n")

    formatted = []
    for line in board:
        formatted.append([int(x) if x != "*" else None for x in line])

    s = Sudoku(3, 3, board=formatted)
    formatted_ans = ""
    for line in s.solve().board:
        formatted_ans += "".join([str(x) for x in line])
        formatted_ans += "\n"
    r.send(formatted_ans.encode())

#  gettin' flaaag
time.sleep(5)
data = (r.recvall()).decode("utf-8")
print(data)
