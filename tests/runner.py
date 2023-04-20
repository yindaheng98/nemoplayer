import asyncio
import argparse
import os
import time
from queue import Queue, Empty

parser = argparse.ArgumentParser()
parser.add_argument('--tasks', type=str, default='tasks.sh', help='Task list')
parser.add_argument('--devices', type=str, default=",".join(list(str(i) for i in range(1, 64))), help='Devices to use')
parser.add_argument('--preprocess', type=str, default="pwd", help='Some preprocess command here (e.g. set environment variables)')
args = parser.parse_args()
root = os.path.dirname(os.path.abspath(args.tasks))


def get_task_pool():
    task_pool = []
    with open(args.tasks, 'r', encoding='utf8') as f:
        line = f.readline().rstrip()
        while line:
            line = line.rstrip()
            if len(line) > 0:
                task_pool.append(line)
            line = f.readline()
    task_queue = Queue(len(task_pool))
    for task in task_pool:
        task_queue.put(task)
    return task_queue


async def print_std(prefix, f):
    async for line in f:
        print(f"{time.strftime('%Y-%m-%d %X', time.localtime())} {prefix} | {line.strip().decode('utf8')}")


async def task_wrapper(device_id, task, preprocess):
    cmd = f"cd {root} && {preprocess} && export DEVICE={device_id} && {task}"
    proc = await asyncio.create_subprocess_exec(
        'sh', '-c', cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    await asyncio.gather(
        print_std(f"{device_id} stdout", proc.stdout),
        print_std(f"{device_id} stderr", proc.stderr)
    )
    return await proc.wait()


failed_tasks = []


async def runner(device_id, task_queue: Queue, preprocess):
    while True:
        try:
            task = task_queue.get_nowait()
            return_code = await task_wrapper(device_id, task, preprocess)
            if return_code != 0:
                failed_tasks.append(task)
            task_queue.task_done()
        except Empty:
            return


async def main():
    task_queue = get_task_pool()
    runners = []
    device_list = []
    for device in args.devices.split(','):
        try:
            device_list.append(int(device))
        except Exception:
            pass
    print(device_list)
    for device_id in device_list:
        runners.append(runner(device_id, task_queue, args.preprocess))
    await asyncio.gather(*runners)
    for task in failed_tasks:
        print(f"failed | {task}")


if __name__ == "__main__":
    asyncio.run(main())
