"""
Problem - Swap and Delete
You are given a binary string s (a string consisting only of 0s and 1s).
You can perform two types of operations on s:

1. Delete one character from s. This operation costs 1 coin.
2. Swap any pair of characters in s. This operation is free (costs 0 coins).

You can perform these operations any number of times and in any order.
Let's call a string you obtain after performing the above operations t. The string t is good if for each i from 1 to |t|, t_i ≠ s_i (|t| is the length of t). The empty string is always good. Note that you are comparing the resulting string t with the initial string s.
What is the minimum total cost to make the string t good?

Input
The first line contains a single integer t (1 ≤ t ≤ 10^4) — the number of test cases. Then t test cases follow.
The only line of each test case contains a binary string s (1 ≤ |s| ≤ 2⋅10^5; s_i ∈ {0, 1}) — the initial string, consisting of characters 0 and/or 1.
Additional constraint: the total length of all strings s doesn't exceed 2⋅10^5.

Output
For each test case, print one integer — the minimum total cost to make string t good.

Examples

Input
4
0
011
0101110001
111100

Output
1
1
0
4

Note
In the first test case, you have to delete the only character from s to get the empty string t. Only then t becomes good. One deletion costs 1 coin.
In the second test case, you can, for example, delete the second character from s to get the string "01", and then swap the first and second characters to get t = "10". String t is good, since t_1 ≠ s_1 and t_2 ≠ s_2. The total cost is 1 coin.
In the third test case, you can, for example, swap s_1 with s_2, swap s_3 with s_4, swap s_5 with s_7, swap s_6 with s_8, and swap s_9 with s_10. You'll get t = "1010001110". All swap operations are free, so the total cost is 0.
In the fourth test case, you need to delete all four characters to get the empty string. The cost is 4 coins.
"""

t = int(input())  # Number of test cases

for _ in range(t): 
    s = input()  # Read the string for this test case

    char_count = {}  # Dictionary to count occurrences of each character
    for i in range(len(s)):
        if s[i] not in char_count:
            char_count[s[i]] = 1  # First occurrence of the character
        else:
            char_count[s[i]] += 1  # Increment existing count

    # Iterate again to simulate removing opposite pairs (0-1 or 1-0)
    for i in range(len(s)):
        if s[i] == "0":
            if "1" in char_count:  # If a '1' exists, remove one
                char_count["1"] -= 1
                if char_count["1"] == 0:
                    char_count.pop("1")  # Remove key if count reaches 0
            else:
                break  # Stop if no '1' left to pair with

        elif s[i] == "1":
            if "0" in char_count:  # If a '0' exists, remove one
                char_count["0"] -= 1
                if char_count["0"] == 0:
                    char_count.pop("0")  # Remove key if count reaches 0
            else:
                break  # Stop if no '0' left to pair with

    # Count remaining unpaired characters
    coins = 0
    for char in char_count:
        coins += char_count[char]

    print(coins)  # Output total remaining characters after pairing