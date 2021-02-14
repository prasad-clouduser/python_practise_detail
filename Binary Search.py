
# Better way of searching. All the values have to be sorted.

# first you need to specify the lower and upper bound.
# then you need to mid value. Mid index = (Lower + Upper)/2

# value to search is smaller or bigger than mid value.
# if the search value is smaller, change your upper bound.
# and then mid becomes new upper bound.

# value to search is higher than the mid value
# then change the lower bound. mid becomes newer lower bound.

pos = -1

def search(list, n):

    l = 0
    u = len(list) - 1

    while l <= u:
        mid = (l + u) // 2 ## // gives the integer division

        if list[mid] == n:
            globals()['pos'] = mid
            return True
        else:
            if list[mid] < n:
                l = mid+1
            else:
                u = mid-1


list = [4, 7, 8, 12, 45, 99]
n = 15

if search(list, n):
    print("Found at: ", pos+1 )
else:
    print("Not Found. ")



