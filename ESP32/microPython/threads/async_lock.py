import asyncio
from asyncio import Lock
import random

"""
Hvis flere tasks skal bruge samme resourcer, f.eks. en databuffer, er det en god idé at
sørge for at to tasks ikke læser og skriver i resourcen på "samme tid".  Der er reelt ikke
noget der er "samme tid", men der er ingen garanti for at task_1 altid kører før task_2 f.eks.

Eksemplet viser en task, der skal bruge den delte resource, frigiver den og laver så noget andet, der tager variabel tid.
Når programmet kører kan vi se, at tasks køres i forskellige rækkefølge, men at der hele tiden kun er én der kan bruge
den delte resource.
"""

# Den delte resource
shared_res = 0

# For at bruge lock, sæt til True
# For ikke at bruge lock, sæt til False
# Bemærk resultaterne!
use_lock = False #True

async def task(i, lock):
    global shared_res
    while 1:
        if use_lock:
            await lock.acquire()
            print(f"lock {i} - var={shared_res} -> ", end="")
        shared_res += 1#i*100^i
        await asyncio.sleep(0.1)
        if use_lock:
            lock.release()
        print(f"free {i} var={shared_res}")
        await asyncio.sleep(random.randint(1,3)*0.5)

async def main():
    lock = Lock()  # The Lock instance
    tasks = [None] * 4  # For CPython compaibility must store a reference see Note
    for n in range(1, 4):
        tasks[n - 1] = asyncio.create_task(task(n, lock))
    await asyncio.sleep(10) # Run for 10s

if use_lock:
    print("Bruger lock.  Den delte resource opfører sig pænt.")
else:
    print("Bruger IKKE lock.  Den delte resource opfører sig kaotisk.")
    
asyncio.run(main())