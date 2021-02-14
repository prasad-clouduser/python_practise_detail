# Generator give you iterators

# function cannot give you the iterators, it has to be something special
## so we ahve to convert this function into generator.
"""
def topten():

    yield 1  ## special keyword which make the function as generator
    yield 2  ## it is generator which will give you the iterator.
    yield 3
    yield 4

values = topten()  ## it will return the iterator

print(values.__next__())
print(values.__next__())

for i in values:
    print(i)
"""

def topten():

    n = 1
    while n <= 10:
        sq = n*n
        yield sq  ## it is always same as function but return will terminate the function but this will not.
        n += 1

values = topten()

for i in values: ## loop will ask you for the next value each time.
    print(i)


## suppose you are fetching 100 records from the database.
# may be yu want to print all. May be you want to process something
## from those records.
## when you say you want to fetcch all the 1000 records
## all the thousand records will be loaded into memory.
## may be you want to wrok with one at a time. 


