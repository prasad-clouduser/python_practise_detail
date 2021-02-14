## major concept.   Poly _--> Many, Morph --> form

## used in below
## 1) Loose Coupling
## 2) Dependency Injection.
##3) interfaces.

## four ways of implementing polymorphism

##1) Duck Typing
##2) Operator Overloading.
##3) Method Overloading.
## 4) Method Overriding.

## Duck typing, if it is walking like a duck, squacking like a duck
## swimming like a duck, that is duck. if behaviour of birdies that matches
## with a duck, then that is duck.

class PyCharm:

    def execute(self):
        print("Compilling")
        print("Running")

class MyEditor:

    def execute(self):
        print("Spell check")
        print("Convention Check")
        print("Compilling")
        print("Running")

class Laptop:
    ## I want to execute the code, to compile and execute we need to pass IDE
    def code(self, ide):
        ide.execute()
        #ide is something that we are trying to execute that is not there in the call, so we can define class.

## when we run the code, as we are not calling anything, it will not display anything
## at this moment.
## Let me call code, by creating the object called laptop

ide = MyEditor() ## type of ide here is pycharm, yes you can do that.

lap1 = Laptop()
lap1.code(ide)


