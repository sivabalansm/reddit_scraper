import multiprocessing
from time import sleep

def work(tasks):
    while True:
        print("Worker waiting for jobs...")
        print(tasks.get())
        sleep(1)


def main():
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    queue3 = multiprocessing.Queue()
    p = multiprocessing.Process(target = work, args = (queue1,))
    p = multiprocessing.Process(target = work, args = (queue2,))
    p = multiprocessing.Process(target = work, args = (queue3,))



    
