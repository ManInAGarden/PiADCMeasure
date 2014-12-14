# -*- coding: utf-8 *-*
class Fifo:
    def __init__(self):
        self.first=()

    def push(self,data):
        node = [data,()]
        if self.first:
            self.last[1] = node
        else:
            self.first = node

        self.last = node
        
    def pop(self,n=-1):
        node = self.first
        self.first=node[1]
        return node[0]

if __name__ == "__main__":
    f = Fifo()
    f.push(10)
    f.push(29)
    print (f.pop(), f.pop())
