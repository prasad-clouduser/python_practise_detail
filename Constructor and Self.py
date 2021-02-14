## Talk about constructor and self.
## init is actually a constructor

class Computer:

    def __init__(self):
        self.name = "Navin"
        self.age = 28

    # def update(self):
    #   self.age = 30

    def compare(self, other):  #also pass c2, c1 become self and c2 becomes other

        if self.age == other.age:
            return True
        else:
            return False

c1 = Computer()
c1.age = 30
c2 = Computer()

#c1.name = "Raasi" ## change value
#c1.age = 12

if c1.compare(c2):
    print("They are same")
else:
    print("They are different")


#c1.update()
# when you calling with C1 your self will be assigned to C1
print(c1.name)
print(c2.name)

## everytime you create an object it wil take two different spaces.
## size of the object depends upon the number of variables we have.
## Who is responsible to assign and calculate the memory, constructor is responsible.


## inside of your system we have special memory you have heap memory and inside
##this heap memory you will get all the objects

## example this object takes some space in your heap memory and every space have
##some address,  We can use id function to print the address of the c1