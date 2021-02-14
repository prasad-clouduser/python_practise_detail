pos = -1

def search(list, n):
    i = 0
    while i < len(list):
        if list[i] == n:
            globals()['pos'] = i
            return True
        i = i+1
    return False

list  = [5, 8, 4, 6, 9, 2]
n = 6

if search(list, n):
    print("Found at", pos)
else:
    print("Not Found")


