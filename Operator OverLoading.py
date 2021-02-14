"""
a = 5
b = 6
# + calls add(), - calls sub(), * calls mul() method. These are called magic methods.

print(a+b)  #behind the scenes below is getting called.
## integer is a class, and it has so many methods.

print(int.__add__(a,b))
## operator remains the same but type of operators that we pass is changes.
"""

class Student:

    def __init__(self,m1, m2):
        self.m1 = m1
        self.m2 = m2

    ## like above method there are many other method, we can try them out.

    def __add__(self, other):
        m1 = self.m1 + other.m1
        m2 = self.m2 + other.m2
        ## once you got above two values. create one more object.
        s3 = Student(m1, m2)
        return s3

    def __gt__(self, other):
        r1 = self.m1 + self.m2
        r2 = other.m1 + other.m2

        if r1 > r2:
            return True
        else:
            return False

    def __str__(self):
        return '{} {}'.format(self.m1, self.m2)
        ## if we just use return self.m1, self.m2 and try to print s1, it will give error, as it is expecting string.

s1 = Student(59, 69)
s2 = Student(60, 65)

s3 = s1 + s2  #we need to know if + sign supported for the class.
## We can not do operation between student 1 and student 2 becoz we have not defined it.
## behind the scenes it will call the add methods, it is not defined for this class.

# s3 = s1 + s2 --> Behind the scenes it gets converted to
# Student.__add__(s1, s2)

print(s3.m1)
print(s3.m2)

if s1 > s2:
    print("s1 wins")
else:
    print("s2 wins")

a = 9
print(a)
print(a.__str__()) # behind the scenes it calling str

print(s1)
print(s1.__str__())
#<__main__.Student object at 0x01640FF0> Student object at that address.
## we can define our own str definition that will return

