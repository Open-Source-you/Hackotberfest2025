"""
Problem:
Given an array of integer nums and an integer target, 
return indices of two numbers such that they add up to target. 
You may assume that each input would have exactly one solution, 
and you may not use the same element twice
Come up with an algorithm that is less than O(n**2) time complexity
"""

"""
Thought Process:
Aim: Get indices of two numbers that sum up to the target
Brute Force:
- Find all possible num pairs
- Get each of their sum
- if sum  == target:
      return indices of each num in pair
Analysis of Algorithm:
    The function has to nested for loops: O(n**2)
    While one loops through the entire nums: the other loops through the remaining nums to get distinct combinations
    
    LeetCode Stats: ACCEPTED
    Runtime: 1760ms    Beats: 23.37%
    Memory
    18.34mb            Beats: 87.06%
My question: Is there a way for me to reduce my time complexity to O(n) ?
My answer: Probably since my TC: O(n**2) and AS: O(1)
Maybe we can make them both O(n) ?
New Idea:
Aim: Optimize Soln to O(n)
if x, y in nums and x + y == target:
    return [nums.index(x), nums.index(y)]
x + y = target -> x = target - y
This means that if we keep track of all possible x until we find a match, We can change our TC to O(n): Loop once
Problem:
    Searching for num in target_inverses would be O(n) leading to a O(n**2)
Solution:
    If we store x and its index as key, val pairs, We can search in O(1) with the help of hashing
Analysis Of Algorithm:
    The function's TC has decreased from O(n**2) O(n) as we loop through nums once
    The AC has increased from O(1) to O(n) as we make use of dictionary to keep track of possible matches
    LeetCode Stats: ACCEPTED
    Runtime: 0ms             Beats: 100.00%
    Memory
    18.90mb                  Beats: 51.02%
My question: Is there another way to further optimixe this solution ?
             To reduce the Space Complexity and Memory Used without Affecting the runtime ?
        
"""


def main():
    nums = list(map(int, input().split()))
    target = int(input())
    soln = Solution()
    print(soln.twoSum(nums, target))


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:

        target_inverses = {}
        for i in range(len(nums)):
            if target - nums[i] in target_inverses:
                return ([i, target_inverses[target- nums[i]]])

            target_inverses[nums[i]] = i


if __name__ == "__main__":
    main()


