
##1) constructor in inheritance
##2) Method resolution order (MRO)

# subclass can access all the features of super class, but vice versa is not possible.

## if we create object of B, first it will try to call the method of its own,
#if it is not there, it will go for A.

"""
class A:

    def __init__(self):
        print("In A Init")

    def feature1(self):
        print("feature 1 is working")

    def feature2(self):
        print("Feature 2 is working")

class B(A):
    # what if if we have own constructor, priority goes to this first.
    # what if we want to call the init method of A as well, there is a
    # special function that we can use, ie super()
    ## by using super, you can access all features of class A. Now we are calling
    ## the init method of A.

    def __init__(self):
        super().__init__()
        print("In B Init")

    def feature1(self):
        print("feature 1 is working")

    def feature4(self):
        print("Feature 4 is working")

a1 = B()  # even if we have object of class B, it will call the constructor of A.
# since we don't have any init method in B, it is going to class A to call its init method.

## conclustion: when you create object of Sub class it will call init of Sub
## class first if you have call super then it will first call init of super class
##then call init of Sub class.

"""
class A:

    def __init__(self):
        print("In A Init")

    def feature1(self):
        print("feature 1-A is working")

    def feature2(self):
        print("Feature 2 is working")

class B:

    def __init__(self):
        print("In B Init")

    def feature1(self):
        print("feature 1-B is working")

    def feature2(self):
        print("Feature 4 is working")

class C(A,B):

    def __init__(self):
        super().__init__()
        print("in C Init")

    def feat(self):
        super().feature2()  ## you can also use super method to call other methods as well.

a1 = C()
a1.feature1() ## it follows the MRO rules. left to right.
a1.feat()
## we have a concept of MRO, when we have multiple inheritance, it will always
## starts from left to right. which means the moment you say init, it will call iself first
## it will prefer the left one first.

## it will also work in the same way for methods. it wil go from left to right




