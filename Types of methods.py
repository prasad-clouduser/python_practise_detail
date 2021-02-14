
## types of methods.

# 1) instance methods.
# 2) Class Methods.
# 3) Static methods.

# in variable class variable and static variables are same
# in methods class methods and static methods are different.

## in instance itself we have two differnt types of methods

# 1) Accessor Methods.  if we want to fetch just the values of instance variables.
# 2) Mutator Methods. if we want to modify the values.

# how about static method, if you want a method that is nothing to do with instance and class methods.
class Student:

    school = "Telusko"

    def __init__(self, m1, m2, m3):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3

    def avg(self):
        return (self.m1 + self.m2 + self.m3)/3

    def get_m1(self):  # not compulsion to have that get key word
        return self.m1

    def set_m1(self, value): ## it wil change the values that is why we say mutators
        self.m1 = value

    # you want to work with class variables you can use class method.
    @classmethod  # if you want to use info as class method.
    def getSchool(cls):  # if you work with instance you work with self keyword, if you want to work with class var you use class
        return cls.school

    ## if you dnt want to relate this to a class, keep it blank,
    ## if you dnt want to relate this to any object, keep it blank
    @staticmethod
    def info():
        print("This is Student Class.... in abc module")
        ## this can be used to perform any operations which
        ## has something to do with other class objects.
        ## or for operations like finding factorial of a number
        ## if you want to do anything extra with the class. 


s1 = Student(34, 47, 32)
s2 = Student(89, 32, 12)

print(s1.avg())
print(s2.avg())

print(Student.getSchool())
Student.info()

