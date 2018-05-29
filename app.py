import asyncio


###-----------Example 1-----------###

# async def foo():
#     print('Running in the foo')
#     await asyncio.sleep(0)
#     print('Explicit context switch to foo again')

# async def bar():
#     print('Explicit context to bar')
#     await asyncio.sleep(0)
#     print('Implicit context switch back to bar')

# ioloop = asyncio.get_event_loop()
# tasks = [ioloop.create_task(foo()), ioloop.create_task(bar())]
# wait_tasks = asyncio.wait(tasks)
# ioloop.run_until_complete(wait_tasks)
# ioloop.close()


###-------------Example 2---------------##

#import time

# start = time.time()

# def tic():
#     return 'at %1.1f seconds' % (time.time()-start)

# async def gr1():
#     # Busy waits for a second, but we don't want to stick around...
#     print('gr1 started work: {}'.format(tic()))
#     await asyncio.sleep(2)
#     print('gr1 ended work: {}'.format(tic()))

# async def gr2():
#     # Busy waits for a second, but we don't want to stick around...
#     print('gr2 started work: {}'.format(tic()))
#     await asyncio.sleep(2)
#     print('gr2 Ended work: {}'.format(tic()))

# async def gr3():
#     print("Let's do some stuff while the coroutines are blocked, {}".format(tic()))
#     await asyncio.sleep(1)
#     print("Done!")

# ioloop = asyncio.get_event_loop()
# tasks = [
#     ioloop.create_task(gr1()),
#     ioloop.create_task(gr2()),
#     ioloop.create_task(gr3())
# ]
# ioloop.run_until_complete(asyncio.wait(tasks))
# ioloop.close()


###-----------------Example 3------------------###

import random
from time import sleep


def task(pid):
    """Synchronous non-deterministic task.

    """

    sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)

async def task_coro(pid):
    """Coroutine non-deterministic task
    """

    await asyncio.sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)

def synchronous():
    for i in range(1, 10):
        task(i)

async def asynchronous():
    tasks = [asyncio.ensure_future(task_coro(i)) for i in range(1,10)]
    await asyncio.wait(tasks)

print('Synchronous:')
synchronous()

ioloop = asyncio.get_event_loop()
print('Asynchronous')
ioloop.run_until_complete(asynchronous())
ioloop.close()
