
## introduction to classes

class Computer:

    ## Attributes.
    ## methods.  Behaviours

    def config(self):
        print("i5, 18GB RAM 1 TB")


a = '8'
x = 9
print(type(a))  ## str is in built class
comp1 = Computer() ## computer is our class\
comp2 = Computer()
print(type(comp1))
print(type(x)) ## int is inbuilt class.

Computer.config(comp1) ## if we want to use to method we have to use computer.
Computer.config(comp2)
## we have to call with object name.


## we have another way of calling

comp1.config() # object itself to call function
comp2.config()
## behind the scenes config take comp1 as argument and it will pass that in self.





