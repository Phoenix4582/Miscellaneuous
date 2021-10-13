from time import time
from inspect import getsource

def timer(func):
    def ff(*args, **kwargs):
        before = time()
        rv = func(*args, **kwargs)
        after = time()
        print("Time elapsed", after - before)
        return rv
    return ff

def describer(func):
    def ff(*args, **kwargs):
        print("------------Begin------------")
        print("Original code:")
        print(getsource(func))
        print("Variable names:")
        print(func.__code__.co_varnames)
        rv = func(*args, **kwargs)
        print("------------End------------")
        return rv
    return ff

def repeater(n):
    def wrapper(func):
        def ff(*args, **kwargs):
            for i in range(n):
                print("Running", i+1, "time(s)")
                rv = func(*args, **kwargs)
            return rv
        return ff
    return wrapper
# @timer
# def add(x, y = 10):
#     return x+y
#
# @timer
# def sub(x, y = 10):
#     return x-y


@repeater(5)
def add(x, y = 10):
    return x+y

@repeater(5)
def sub(x, y = 10):
    return x-y

if __name__ == '__main__':
    print("add(20)", add(20))
    print("sub(20)", sub(20))
