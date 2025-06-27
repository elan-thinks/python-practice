class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def traverseNode(head):
    currentNode = head
    while currentNode:
        print(currentNode.data, end=(" -> "))
        currentNode = currentNode.next
    print("null")

def deleteNode(node , nodeToDelete):
    if node.data == nodeToDelete:
        return node.next
    currentNode = node
    lastNode = currentNode
    while currentNode:
        if currentNode.data == nodeToDelete:
            lastNode.next = currentNode.next
        elif currentNode.data is None:
            print("value note found !")

        lastNode = currentNode
        currentNode = currentNode.next
    return node

nodel1 = Node(7)
nodel2 = Node(11)
nodel3 = Node(3)
nodel4 = Node(2)
nodel5 = Node(9)

nodel1.next = nodel2
nodel2.next = nodel3
nodel3.next = nodel4
nodel4.next = nodel5

nodel1 = deleteNode(nodel1, nodel1.data)
traverseNode(nodel1)
