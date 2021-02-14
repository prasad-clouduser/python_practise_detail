## Python does not support abstract classes. But support with a module.

# 1) What is abstract class
# 2) Why do we need it?

from abc import ABC, abstractmethod

class Computer(ABC): # has become subclass of ABC
    @abstractmethod # you are talking to compiler about it that this method abstract method.
    def process(self):
        pass #just declare no body. # which has declaration and no body called abstract method.

class Laptop(Computer):
    #pass
    #it is compulsion for you define that method. otherwise this class is an abstract class.

    def process(self):
        print("It is running.")

class Whiteboard(Computer):   ## there is no compulsion to have method called process. if there is no computer in brackets
    ## but if we have computer in brackets, it becomes compulsion for whiteboard to have process.
    def write(self):
        print("It is writing")

class Programmer:

    def work(self,com):  # com can be anything, desktoop, mobile, or whiteboard.
        print("Solving Bugs")
        com.process()

#com = Computer()

com1 = Laptop()
com2 = Whiteboard()
prog1 = Programmer()
prog1.work(com2) # execute now, it throws error.

#com1.process()

## execute now, it will throw. if we create a object for abstract class. you wont be able to do it.

# we created a class and that class is implementing all the methods. if you
# failed to implement all the abstract methods, you will get an error.
# abstract class has at least one abstract method.

## it is design aspect. it is not that you cannot write the code without abstract classes
## but sometimes it also depends upon the way you design your applications and the way
## you design classes.

## you can abstract classes, so that other classes will have some signature. or some
## restriction which method they define.

## example when you design APIs, you can create an API and if someone wants to use your API
## and they have all methods defined.




