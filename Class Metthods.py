
## introduction to classes

class Computer:

    def __init__(self, cpu, ram):
        ## like contructor in java.
        self.cpu = cpu
        self.ram = ram
        ## no compusion to have same name

    def config(self):
        print("Config is: ", self.cpu,self.ram)
        ## you are passing the self because you can use it to fetch the values

com1 = Computer('i5', 16)   ##computer is our class
com2 = Computer('Ryzen 3', 8)

com1.config()
# the moment you call computer, it brackets you pass object as first parameter
#it gets passed automatically, First one object, second variables,
com2.config()







