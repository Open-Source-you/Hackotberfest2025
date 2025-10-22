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
    print(is_palindrome(s))

if __name__ == "__main__":
    main()