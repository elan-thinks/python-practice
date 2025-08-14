class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        count = 0
        i = 0
        for x in s:
            # ss = s.count(x)
            if s[i] == x:
                count += 1
                print(count)
                i += 1
        return count


s = "pwwkew"
solution = Solution()
print(solution.lengthOfLongestSubstring(s))
