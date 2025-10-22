def longestPalindrome(s: str) -> str:
    """Returns the first longest palindrome in a substring"""

    # Handles Edge case: If string is empty, return empty
    if not s:
        return ""

    longest = s[0] # Initialize longest string to the first letter
    for i in range(len(s)):
        substring = s[i] # Gets a single character E.g s = "book", substring = "b" when i = 0

        for j in range(i+1, len(s)):
            substring += s[j] # Keep adding more characters that are right of it E.g, substring = "bo", then "boo", then "book"

            # If substring is palindrome check if it is longer than current longest palindrome, if so, 
            if is_palindrome(substring):

                if len(substring) > len(longest):
                    longest = substring

    return longest


def is_palindrome(substr: str) -> bool:
    result = True

    # Iterate to the middle of the length of the sting
    for i in range(len(substr) + 1 // 2):
        # Keep checking if a letters equidisant from the middle are the same
        if substr[i] != substr[len(substr) - i - 1]:
            result = False
            break
    return result

# Driver code
def main():
    s = input()
    print(longestPalindrome(s))

if __name__ == "__main__":
    main()
