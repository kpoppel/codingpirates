import asyncio
import random

"""
Programmet starter 3 tasks udover main som hver gør noget og venter en bestemt tid.
Mens hver task venter, kan andre dele af programmet køre.
"""
async def do_something(x, sleep):
    count = 0
    while True:
        count += 1
        print('Instance: {} count: {}'.format(x, count))
        await asyncio.sleep(sleep)

async def main():
    tasks = [None] * 3
    for x in range(3):
        sleep_s = random.randint(1,4)
        tasks[x] = asyncio.create_task(do_something(x, sleep_s))
    await asyncio.sleep(10)

asyncio.run(main())