# Mind Your Decisions - "69 Is A Nice Number"
# - 69**2 and 69**3 has all ten digits exactly once.
# https://www.youtube.com/watch?v=H4YjOD65Ur0
# - his code didn't look correct to me
# - he used an AI and changed it a little

# Problem Statement
# For 48 <= n <= 98, compute n^2 and n^3 and test if
# {digits(n^2),digits(n^3)} = {0,1,2,3,4,5,6,7,8,9}

# the code he finally ran
def find_numbers1():
    numbers = []
    x = range(48, 99, 1)
    for n in x:
        square = n ** 2
        cube = n ** 3
        digits = set(str(square) + str(cube))
        if len(digits) == 10:
            numbers.append(n)
    return numbers

assert find_numbers1() == [69]

# let's try a wider range...

def find_numbers2(a, b):
    for n in range(a, b):
        square = n ** 2
        cube = n ** 3
        digits = set(str(square) + str(cube))
        if len(digits) == 10:
            yield n

# - his function is correct, since the problem statement requires
#   between 48 and 98
# - but it's not correctly determining there are ten *unique* digits
# - when all the digits are there but there are dupes, `set` strips the dupes
#   and he tests the population of the set

wrong_result = list(find_numbers2(0, 200))
assert wrong_result == [69, 128], f'{result=}'

# the problem statements says {0..9}, so I think this change is justified

def is_nice(n):
    digits = ''.join(map(str, (n ** p for p in [2, 3])))
    return len(digits) == len(set(digits)) == 10

def find_numbers3(a, b):
    yield from filter(is_nice, range(a, b))

# and an even larger range

correct_result = list(find_numbers3(0, 100000))
assert correct_result == [69], f'{correct_result=}'
