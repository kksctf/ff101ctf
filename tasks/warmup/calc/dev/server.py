#!/usr/bin/env python3

import random
import asyncio

flag = b"ptctf{i_h0p3_y0u_h4v3_us3d_3v4l_1n_s0lv3}\n"


class ProblemGenerator():

    def __init__(self, _size):
        assert(_size > 0)
        self.size = _size
        self.answer = 0
        self.problem = b''

        possible_ops = ['+', '-', '/', '*']
        result_example = ""

        for _ in range(self.size):
            result_example += hex(random.randint(1, 50))
            result_example += random.choice(possible_ops)

        result_example += hex(random.randint(1, 50))

        self.answer = eval(result_example)
        self.problem = result_example.encode("latin-1") + b"\n"
        


async def handle_client(reader, writer):
    
    # print(reader._transport.get_extra_info('peername'), o.problem, o.answer)
    problems_solved = 0
    deadline = 500
    flag_exit = False

    while True:
        o = ProblemGenerator(problems_solved + 1)
        writer.write(o.problem)
        await writer.drain()
        answer = await reader.read(1024)
        answer = answer.decode('latin-1').strip()
        if answer == '':
            answer = '0.00'
        else:
            answer = float(answer)

        if answer == o.answer:
            problems_solved += 1
            resp = "YES {} more\n".format(deadline-problems_solved).encode("latin-1")
            if problems_solved == deadline:
                resp += flag
                flag_exit = True
            writer.write(resp)
            await writer.drain()
        else:
            writer.write("NO, CORRECT IS {} \n".format(o.answer).encode("latin-1"))
            await writer.drain()
            flag_exit = True
        
        if flag_exit:
            break

        await asyncio.sleep(0.01)

    writer.close()
    await writer.wait_closed()
    return 

async def init():
    sock = await asyncio.start_server(handle_client, '0.0.0.0', 1337)

    async with sock:
        await sock.serve_forever()

if __name__ == "__main__":
    asyncio.run(init())
