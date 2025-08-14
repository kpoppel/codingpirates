import asyncio

"""
En klasse definerer et antal tasks, og constructor opretter dem.
Hovedprogrammet kører opgaverne.

Kilde: https://github.com/peterhinch/micropython-async/blob/master/v3/docs/TUTORIAL.md
"""
class MyTasks():
    def __init__(self):
        task = asyncio.create_task(self.task_1(1))
        task = asyncio.create_task(self.task_2(2))
        task = asyncio.create_task(self.task_3(3))

    def task_1(self, sleep):
        while True:
            print("1", end="")
            await asyncio.sleep(sleep)
            
    def task_2(self, sleep):
        while True:
            print("2", end="")
            await asyncio.sleep(sleep)

    def task_3(self, sleep):
        while True:
            print("3", end="")
            await asyncio.sleep(sleep)
            
    def run_forever(self):
        while True:
            await asyncio.sleep(10)
            
        
def set_global_exception():
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

async def main():
    set_global_exception() # Debug aid
    t = MyTasks()          # Constructor creates tasks
    await t.run_forever()  # Non-terminating method
    
try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()  # Clear retained state