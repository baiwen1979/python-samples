from multiprocessing import Pool
import os, time, random

def run_task(name):
    print('Task {0} (pid = {1}) is running ...'.format(name, os.getpid()))
    # 休眠随机秒数，以模拟不同任务的处理时延
    time.sleep(random.random() * 3)
    print('Task {} Done.'.format(name))
    
print("Parent Process({}) is requesting Child Processes for running Task... "
      .format(os.getpid()))

def main():
    # 创建3个进程的进程池
    pool = Pool(processes=3)
    for i in range(5):  #5个任务请求
        pool.apply_async(run_task, args=(i,))

    print("Waiting for all Child Processes in Pool Done.")
    # 关闭进程池,停止接受任务请求
    pool.close()
    # 同步进程池中的子进程
    pool.join()

    print('All Processes Done.')
    
if __name__ == '__main__':
    main()