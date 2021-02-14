"""
#iterator

nums = [7, 8, 9, 5]

it = iter(nums)
print(it.__next__())
print(it.__next__())

print(next(it))
"""

#iter will give you the object.
# next will give you the next value.

class TopTen:

    def __init__(self):
        self.num = 1

    def __iter__(self):
        return self

    def __next__(self):

        if self.num <= 10:
            val = self.num
            self.num += 1
            return val
        else:
            raise StopIteration

values = TopTen()
print(next(values)) ## it will fetch one only once.

for i in values: ## one will not be repeated again
    print(i)



