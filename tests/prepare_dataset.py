import asyncio
import os
import sys
import time
from queue import Queue, Empty

script = os.path.join(os.path.dirname(sys.argv[0]), "prepare_video.sh")

scale = int(sys.argv[1])
root_orig = sys.argv[2]
root_desc = os.path.join(root_orig, '')[0:-1] + "_x%d" % scale
if len(sys.argv) >= 4:
    root_desc += sys.argv[3]
enc_opts = []
if len(sys.argv) >= 5:
    enc_opts = sys.argv[4:]

tasks = []
for name in os.listdir(root_orig):
    path_orig = os.path.join(root_orig, name)

    path_desc = os.path.join(root_desc, name + '.ivf')
    tasks.append([script, path_orig, path_desc, str(scale), *enc_opts])

task_queue = Queue(len(tasks))
for task in tasks:
    task_queue.put(task)


async def runner(i):

    async def task_wrapper(i, task):
        proc = await asyncio.create_subprocess_exec(
            *task,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        async def print_std(prefix, f):
            async for line in f:
                print(f"{time.strftime('%Y-%m-%d %X', time.localtime())} {prefix} | {line.strip().decode('utf8')}")
        await asyncio.gather(
            print_std(f"{i} stdout", proc.stdout),
            print_std(f"{i} stderr", proc.stderr)
        )
        return await proc.wait()

    failed_tasks = []
    while True:
        try:
            task = task_queue.get_nowait()
            return_code = await task_wrapper(i, task)
            if return_code != 0:
                failed_tasks.append(task)
            task_queue.task_done()
        except Empty:
            return failed_tasks

runners = []
for i in range(16):
    runners.append(runner(i))


async def main():
    failed_task_list = await asyncio.gather(*runners)
    failed_tasks = []
    for fts in failed_task_list:
        failed_tasks.extend(fts)
    for task in failed_tasks:
        print("failed:", task)

asyncio.run(main())
