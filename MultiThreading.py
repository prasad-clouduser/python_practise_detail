## most interesting and useful topic.
## We can break down one task into Multiple processes.
## and each process can be broken down in to a thread.

from time import sleep
from threading import *

class Hello(Thread): ## you have to make them subclass of Thread.
    def run(self):  # why do we go for run method, becoz inside we have a method call run in the thread class.
        for i in range(5):
            print("Hello")
            sleep(1)

class Hi(Thread):
    def run(self):
        for i in range(5):
            print("Hi")
            sleep(1)


t1 = Hello()
t2 = Hi()

#t1.run() # instead of run use t1.start, internally it will call start method.
t1.start()
sleep(0.2) ## gap between them. so taht they will not go in collision.
t2.start()  ## if we execute now, they are still executing simultaneosly.

t1.join() ## ask main method to wait till t1 to comes back.
t2.join() ## ask main method to wait till t2 to comes back. then it will execute bye


print("Bye")  # t1 is busy printing hello, t2 is busy printing hi. Main is doing nothing.

## by default every execution have one thread.
## even if you are not creating a thread by yourself, we have one thread ie Main thread.

## by default we have main thread, it will execute all the statements.
## by the time you say Run and Run, it will create two threads t1 and t2
## t1 will print hello five times and t2 will print hi five times.

## after executing 500 num, this system is so fast that it is excuting them
## at the same time. There is a collision. There is concept called scheduler
## that will allocate specific time to execute, We are expecting it will execute
## one hello at that time. but it is very smart




