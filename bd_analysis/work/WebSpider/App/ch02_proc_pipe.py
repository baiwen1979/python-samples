import multiprocessing as mp
import os, time, random

def proc_send(pipe, urls):
    for url in urls:
        print('Process({0}) send: {1}'.format(os.getpid(), url))
        pipe.send(url)
        time.sleep(random.random())
    pipe.send('exit')
        
def proc_recv(pipe):
    while True:
        message = pipe.recv()
        if message == 'exit':
            break
        print('Process({0}) recv: {1}'.format(os.getpid(), message))
        time.sleep(random.random())

def main():
    pipe_send, pipe_recv = mp.Pipe()
    
    urls = [('http://www.' + str(i) * 3  + '.com') for i in range(10)]
    p1 = mp.Process(target=proc_send, args=(pipe_send, urls))
    p2 = mp.Process(target=proc_recv, args=(pipe_recv,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
    
if __name__ == '__main__':
    main()