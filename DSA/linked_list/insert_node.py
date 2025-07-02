class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


def traverseNode(head):
    currentNode = head
    while currentNode:
        print(currentNode.data, end=" -> ")
        currentNode = currentNode.next
    print("null")


def insertNode(head, newNode, pos):
    prevNode = None
    count = 1
    currentNode = head
    if pos <= 1 or head is None:
        newNode.next = head
        return newNode

    while currentNode and count < pos:
        prevNode = currentNode
        currentNode = currentNode.next
        count += 1

    prevNode.next = newNode
    newNode.next = currentNode
    return head


node1 = Node(7)
node2 = Node(11)
node3 = Node(3)
node4 = Node(2)
node5 = Node(9)
node6 = Node(6)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5

node1 = insertNode(node1, node6, 3)
traverseNode(node1)
print(node5.next)
