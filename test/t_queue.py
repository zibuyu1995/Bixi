# coding: utf-8

import asyncio

queue = asyncio.Queue()


async def main():
    for i in range(10):
        print(i)
        await queue.put(i)
    while queue.qsize():
        d = await queue.get()
        print(d)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
