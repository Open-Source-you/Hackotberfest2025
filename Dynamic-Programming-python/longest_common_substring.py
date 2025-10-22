def longest_common_subsequence(text1: str, text2: str) -> int:
    m = len(text1)
    n = len(text2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


if __name__ == "__main__":
    string1 = input("Enter String 1: ")
    string2 = input("Enter String 2: ")

    lcs_length = longest_common_subsequence(string1, string2)

    print(f"\nString 1: '{string1}'")
    print(f"String 2: '{string2}'")
    print(f"Length of the Longest Common Subsequence: {lcs_length}")
