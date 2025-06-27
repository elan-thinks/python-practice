class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

def traversAndPrint(head):
    currentNode = head
    while  currentNode:
        print(currentNode.data , end=" -> ")
        currentNode = currentNode.next
    print("null")

nodel1 = Node(7)
nodel2 = Node(11)
nodel3 = Node(3)
nodel4 = Node(2)
nodel5 = Node(9)

nodel1.next = nodel2
nodel2.next = nodel3
nodel3.next = nodel4
nodel4.next = nodel5

traversAndPrint(nodel1)



