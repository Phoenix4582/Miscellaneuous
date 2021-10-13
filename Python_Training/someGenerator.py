from time import sleep

# class Compute():
#     def __init__(self, n):
#         self.n = n
#
#     def run(self):
#         result = []
#         for i in range(self.n):
#             sleep(0.5)
#             result.append(i)
#
#         return result

class Compute():
    def __iter__(self):
        self.last = 0
        return self
    def __next__(self):
        result = self.last
        self.last += 1
        if self.last > 10:
            raise StopIteration()
        sleep(0.5)
        return result

if __name__ == '__main__':
    # K = Compute(10)
    # print(K.run())
    for val in Compute():
        print(val)
