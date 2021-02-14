

## explanation about Inner class.

class Student:

    def __init__(self, name, rollno):
        self.name = name
        self.rollno = rollno
        self.lap = self.Laptop() # in the constructor you can define.

    def show(self):
        print(self.name, self.rollno)
        self.lap.show()
    ## suppose you also want to student lab info

    class Laptop: ## object of this class should be in side the outer class

        def __init__(self):
            self.brand = 'HP'
            self.cpu = 'i5'
            self.ram = 8

        def show(self):
            print(self.brand, self.cpu, self.ram)

s1 = Student('Navin', 2)
s2 = Student('Jenny', 3)

print(s1.name, s1.rollno)

s1.show()

## this student object.lap
## if you want to use the inner class.

print(s1.lap.brand)

## for every object you wil get different laptop object.

lap1 = s1.lap
lap2 = s2.lap

#print(id(lap1))
#print(id(lap2))

# you can create object of inner class inside the outer class or
# you can create object of inner class outside the outer class provided
# you use outer class name to call it.

#lap1 = Student.Laptop() ## laptop belongs to student class.







