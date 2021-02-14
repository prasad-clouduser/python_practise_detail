## oops two type of variable
## instance varibles.
## class variables or static varibles.

class Car:
    wheels = 4
    ## out side init it becomes class variable.

    def __init__(self):
        ## instance variables. become instance variable

        self.mil = 10
        self.com = "BMW"

# wheels is common for all objects, so we can also use class name
# namespace is an area where you create and store object/variable.

# 1) class namespace --> Where you store all class variables.
# 2) object/instance namespace --> Where you can store all instance variables.

c1 = Car()
c2 = Car()

c1.mil = 8
Car.wheels = 5  # this wheel is shared among all objects.

print(c1.com, c1.mil, c1.wheels)
print(c2.com, c2.mil, c2.wheels)
