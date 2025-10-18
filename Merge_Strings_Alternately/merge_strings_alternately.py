"""
Problem: https://leetcode.com/problems/merge-strings-alternately/

You are given two strings, word1 and word2. Merge the strings by adding letters in alternating order,
starting with word1. If one string is longer, append the remaining letters of the longer string
to the merged result.

Example 1:
Input: word1 = "abc", word2 = "pqr"
Output: "apbqcr"

Example 2:
Input: word1 = "ab", word2 = "pqrs"
Output: "apbqrs"

Example 3:
Input: word1 = "abcd", word2 = "pq"
Output: "apbqcd"

Constraints:
- 1 <= len(word1), len(word2) <= 100
- word1 and word2 consist of lowercase English letters only.
"""

# -------------------- FIRST ATTEMPT --------------------
# Approach: Loop up to the minimum length of the two strings,
# appending characters alternately. Then, append any remaining substring.

def mergeAlternately(word1: str, word2: str) -> str:
    # Find the smallest length between the two words
    minLen = min(len(word1), len(word2))

    # Initialize an empty string to store the result
    new_word = ""

    # Loop through indices up to the smaller length
    for i in range(minLen):
        new_word += word1[i]  # Add character from word1
        new_word += word2[i]  # Add character from word2

    # If word1 is longer, append the remaining characters
    if len(word1) > minLen:
        new_word += word1[minLen:]

    # If word2 is longer, append its remaining characters
    elif len(word2) > minLen:
        new_word += word2[minLen:]
    
    # Return the merged result
    return new_word


"""
Thought Process:

This first solution is intuitive and readable. It loops up to the shorter string’s length, 
then concatenates the leftovers from the longer one.

However, each time you use the '+' operator on strings inside a loop, Python creates a *new string* 
(because strings are immutable). This results in higher time complexity.

   Analysis of Algorithm:
    - Time Complexity: O(n²) due to repeated string concatenations
    - Space Complexity: O(n + m)
    - Readability: Clear and simple

   Problem:
    - Not optimal for longer strings.
    - Each concatenation creates a temporary copy → inefficient.
"""

# -------------------- OPTIMIZED VERSION --------------------
# Approach: Use a list to accumulate characters, then join at the end.
# This avoids multiple string copies and runs in linear time.

def mergeAlternatelyOptimized(word1: str, word2: str) -> str:
    """Optimized: Merge two strings alternately using list accumulation."""
    
    maxLen = max(len(word1), len(word2))  # Loop up to the longer string length
    new_arr = []  # Use a list to efficiently collect characters

    for i in range(maxLen):
        if i < len(word1):  # Check boundary for word1
            new_arr.append(word1[i])
        if i < len(word2):  # Check boundary for word2
            new_arr.append(word2[i])

    # Join list into a single string at the end
    return ''.join(new_arr)


"""
Optimized Approach Discussion:

 Idea:
    Instead of concatenating strings in every loop iteration, 
    store all characters in a list and join once at the end.

 Why This Works:
    - Lists are mutable → appending is O(1) amortized.
    - `''.join(list)` efficiently combines all elements in one pass.

 Analysis of Algorithm:
    - Time Complexity: O(n + m)
    - Space Complexity: O(n + m)
    - Readability:  Still simple and elegant
    - Performance:  Much faster for longer inputs

"""
# Driver code
def main():
    word1 = "abcd"
    word2 = "pq"
    print(mergeAlternatelyOptimized(word1, word2))  # Output: "apbqcd"

if __name__ == "__main__":
    main()
