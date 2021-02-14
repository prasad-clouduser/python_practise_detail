## Method OverLoading.

## method Overloading. --> in java. having same two methods in a class. We cannot
## do the same thing

## inheritance. have the same method in two different classes with same parameters. that is called method overriding

class Student:

    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2

    #def sum(self, a, b, c): of we pass two arg, it will throw error. in java we create separate method with three arg
    ## this does not support in python, we are just doing some tricks

    def sum(self, a=None, b=None, c=None):
        s=0
        if a!= None and b!= None and c != None:
           s = a + b + c
        elif a!= None and b!= None:
           s = a + b
        else:
           s = a
        return s

s1 = Student(58, 69)
print(s1.sum(5,9,6))


