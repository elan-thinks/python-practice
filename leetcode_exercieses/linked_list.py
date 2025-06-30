# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        newNodeL1 = l1
        newNodeL2 = l2
        sumNode = l1
        reminder=[0]

        while newNodeL1 or newNodeL2:
            # print (newNodeL2)
            if  newNodeL1 is None :
               sumNode.val = 0 + newNodeL2.val + reminder[0]
            elif newNodeL2 is None:
               sumNode.val = newNodeL1.val + 0 + reminder[0]
            # print(reminder[0])
            else:
                sumNode.val =newNodeL1.val + newNodeL2.val + reminder[0]
                newNodeL1 = newNodeL1.next
                newNodeL2 = newNodeL2.next
            if sumNode.val > 9 :
                value = sumNode.val %10
                sumNode.val = value
                reminder[0] = 1
            print (sumNode.val)
        return sumNode.next



solution = Solution()
l1 = [2,4,3]
for x in range(len(l1)):
    ListNode(l1[x])
    l2 = [5,6,4]
    for y in range(len(l2)):
        ListNode(l2[y])
        # if x >= y:
        solution.addTwoNumbers(ListNode(l1[x]), ListNode(l2[y]))
