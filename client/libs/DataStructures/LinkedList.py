class Node():
    def __init__(self, value):
        self.value = value
        self.next = None
        self.previous = None

    def proceedNext(self, func, ifNone, *args, **params):
        return func(self.value, lambda *largs, **lparams: self.next.proceedNext(func, ifNone, *largs, **lparams) if self.next != None else ifNone, *args, **params)

    def proceedPrevious(self, func, ifNone, *args, **params):
        return func(self.value, lambda *largs, **lparams: self.previous.proceedPrevious(func, ifNone, *largs, **lparams) if self.previous != None else ifNone, *args, **params)


class LinkedList():
    def __init__(self):
        self.beginNode = None
        self.endNode = None

    def isEmptyXDecoratorCreator(ifEmpty):
        def isEmptyXDecorator(func):
            def newFunc(self, *args, **params):
                if self.beginNode == None:
                    return ifEmpty
                else:
                    return func(self, *args, **params)

            return newFunc

        return isEmptyXDecorator


    def add(self, value):
        if self.getLength() == 0:
            self.beginNode = Node(value)
            self.endNode = self.beginNode
        else:
            self.endNode.next = Node(value)
            endNodeH = self.endNode
            self.endNode = self.endNode.next
            self.endNode.previous = endNodeH

    def addToBegin(self, value):
        if self.getLength() == 0:
            self.beginNode = Node(value)
            self.endNode = self.beginNode
        else:
            beginNodeH = self.beginNode
            self.beginNode = Node(value)
            self.beginNode.next = beginNodeH
            self.beginNode.next.previous = self.beginNode

    def get(self, getIndex):
        if getIndex < self.getLength():
            def nodeFunc(value, proceedNext, index):
                if index == getIndex:
                    return value
                else:
                    return proceedNext(index+1)

            return self.beginNode.proceedNext(nodeFunc, LinkedList(), 0)

    def pop(self, index):
        if index < self.getLength():
            if self.getLength() == 1:
                beginNodeH = self.beginNode
                self.beginNode = None
                self.endNode = None

                return beginNodeH.value
            else:
                if index == 0:
                    beginNodeH = self.beginNode
                    self.beginNode = self.beginNode.next
                    self.beginNode.previous = None

                    return beginNodeH.value
                elif index == self.getLength()-1:
                    endNodeH = self.endNode
                    self.endNode = self.endNode.previous
                    self.endNode.next = None

                    return endNodeH.value
                else:
                    tempNode = self.beginNode
                    for i in range(index):
                        tempNode = tempNode.next

                    tempNode.previous.next = tempNode.next
                    tempNode.next.previous = tempNode.previous

                    return tempNode.value

    @isEmptyXDecoratorCreator([])
    def find(self, condition):
        def nodeFunc(value, proceedNext):
            result = proceedNext()
            if condition(value):
                result.addToBegin(value)

            return result

        return self.beginNode.proceedNext(nodeFunc, LinkedList()).toList()

    @isEmptyXDecoratorCreator([])
    def findIndex(self, condition):
        def nodeFunc(value, proceedNext, index):
            result = proceedNext(index+1)

            if condition(value):
                result.addToBegin(index)

            return result

        return self.beginNode.proceedNext(nodeFunc, LinkedList(), 0).toList()

    @isEmptyXDecoratorCreator([])
    def toList(self):
        def nodeFunc(value, proceedNext):
            l = [value]
            l.extend(proceedNext())
            return l

        return self.beginNode.proceedNext(nodeFunc, [])

    @isEmptyXDecoratorCreator(0)
    def getLength(self):
        def nodeFunc(value, proceedNext):
            return 1+proceedNext()

        return self.beginNode.proceedNext(nodeFunc, 0)



def test():
    # l = LinkedList()
    # l.add({'id': 5, 'value': 'A'})
    # l.add({'id': 4, 'value': 'B'})
    # l.add({'id': 8, 'value': 'C'})
    # l.add({'id': 3, 'value': 'D'})
    # l.add({'id': 1, 'value': 'F'})
    #
    # print(l.find(lambda value: value['id']%2 == 0).toList())
    #
    # indexes = l.findIndex(lambda value: value['id']%2 == 0)
    # print(indexes)
    # for index in indexes:
    #     print(l.get(index))

     # l = LinkedList()
     # l.add({'id': 5, 'value': 'A'})
     # l.add({'id': 4, 'value': 'B'})
     # l.add({'id': 8, 'value': 'C'})
     # l.add({'id': 3, 'value': 'D'})
     # l.add({'id': 1, 'value': 'F'})
     #
     # print(l.get(2))

    pass




if __name__ == '__main__':
    test()
