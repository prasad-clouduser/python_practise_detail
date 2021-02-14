## three types of error
# compile time error: Error at compile time errors syntax erros.
## logical error: 2+3 = 4 not correct output logical error
## run time error, dividing 6/0 not possible so run time error.

a = 5
b = 2

try:
    print("resource Open")
    print(a/b)
    k = int(input("Enter a number: "))
    print(k)
except ZeroDivisionError as e:
    print("Hey, You can not divide a number by zero: ",e)
except ValueError as e:
    print("Invalid input")
except Exception as e: ## like a general doctor
    print("Hey, You cannot divide a number by zero", e)

finally:
    print("resource Closed")



