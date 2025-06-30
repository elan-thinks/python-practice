from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}

        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]

            seen[num] = i


solution = Solution()
# num = [2,7,11,15]
num = [3,2,3]
# num = [3,3]
k = int(6)
print(solution.twoSum(num , k))
