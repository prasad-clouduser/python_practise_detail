
## Inheritance.
## 1) Single
## 2) MultiLevel
### 3) Multiple

class A:

    def feature1(self):
        print("feature 1 is working")

    def feature2(self):
        print("Feature 2 is working")

## if you want to use features of A class.

"""
class B(A):  # B is a child class of A

    def feature3(self):
        print("feature 3 is working")

    def feature4(self):
        print("Feature 4 is working")
"""
#Suppose consider A as separate class and B as a separate class.
# and c want to access to feature of both A and B. This is called multiple inheritance

class B:  # B is a child class of A

    def feature3(self):
        print("feature 3 is working")

    def feature4(self):
        print("Feature 4 is working")

class C(A,B):

    def feature5(self):
        print("Feature 5 is working")


a1 = A()

a1.feature1()
a1.feature2()

b1 = B()
b1.feature3()

c1 = C()
c1.feature3()