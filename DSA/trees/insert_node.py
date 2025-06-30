class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def traverseTree(root: TreeNode):
    if root is None:
        return root

    print(root.data)
    traverseTree(root.left)
    traverseTree(root.right)

# def inserNode(node):
    

root = TreeNode(1)
nodeA = TreeNode(2)
nodeB = TreeNode(5)

nodeC = TreeNode(3)
nodeD = TreeNode(4)
nodeE = TreeNode(6)
nodeF = TreeNode(7)
nodeG = TreeNode(8)

root.left = nodeA
root.right = nodeB

nodeA.left = nodeC
nodeA.right = nodeD

nodeB.left = nodeE
nodeB.right = nodeF

nodeF.left = nodeG

traverseTree(root)

newNode = TreeNode(10)
# insertNode(newNode)

