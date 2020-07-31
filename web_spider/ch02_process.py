import os, time, random
from multiprocessing import Process


# 子进程启动时要执行的函数
def proc_run(name):
    time.sleep(random.random() * 3)
    print('Child Process {0}({1}) is running...'.format(name, os.getpid()))  

    
def main():
    print('Parent Process({}) is creating and starting Child Processes...'.format(os.getpid()))
    for i in range(5):
        p = Process(target=proc_run, args=(str(i),))
        print('Child Process is starting...')
        p.start()
        # 等待所有子进程结束
        p.join()
    print('All Processes Done.')

if __name__ == '__main__':
    main()