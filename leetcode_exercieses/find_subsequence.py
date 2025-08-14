from typing import List


class Solution:
    def maxSubsequence(self, nums: List[int], k: int) -> List[int]:
        sum = [0]
        t = []
        for i in nums:
            for z in range(k):
                for j in nums:
                    # t = []
                    sum.append(i + j)
                    t.append(i)
                    t.append(j)
            if len(sum) > 1:
                max(sum)
                print(sum)
                return t


solution = Solution()
num = [2, 1, 3, 3]
k = int(2)
print(solution.maxSubsequence(num, k))
