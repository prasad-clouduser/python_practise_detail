## files.

f = open("MyData", 'r')
print(f.readline(), end='') ## print only first line
print(f.readline()) ## fetch the second line, pointer will move to second line. After fetching

## second line pointer will move to the third line.
## print will give you a new line and also in the file content there is a newline after every line.

f1 = open('abc', 'w')
f1.write("Something")

for data in f:
    print(data)
    f1.write(data)






