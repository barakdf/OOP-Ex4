# A simple implementation of Priority Queue
# using Queue.
from Node import *
import heapq


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def add(self, data: Node):
        self.queue.append(data)

    # for popping an element based on Priority
    def pop(self):
        try:
            min = 0
            for i in range(len(self.queue)):

                if self.queue[i] < self.queue[min]:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except IndexError:
            print()
            exit()






if __name__ == '__main__':
    myQueue = PriorityQueue()
    myQueue.add(12)
    myQueue.add(1)
    myQueue.add(14)
    myQueue.add(7)
    print(myQueue)
    while not myQueue.isEmpty():
        print(myQueue.pop())
