def romanToInt(self, s: str) -> int:
    """
    Convert a Roman numeral string to its integer equivalent.
    Example: 'XIV' -> 14
    """

    # Dictionary mapping Roman numeral symbols to their integer values
    roman_numerals = {
        "I": 1, "V": 5,
        "X": 10, "L": 50,
        "C": 100, "D": 500,
        "M": 1000
    }

    # Initialize the result with the value of the last Roman character
    # This handles the last character since it doesn't have a "next" character to compare to
    last_char = s[-1]
    value = roman_numerals[last_char]

    # Loop through the string from left to right (excluding the last char)
    for i in range(len(s) - 1):
        # Get the current Roman character and the next one
        char = s[i]
        next_char = s[i + 1]

        # Retrieve their corresponding values
        val_char = roman_numerals[char]
        val_next_char = roman_numerals[next_char]

        # If the current value is smaller, subtract it (like IV = 5 - 1 = 4)
        # Otherwise, add it (like VI = 5 + 1 = 6)
        if val_char < val_next_char:
            value -= val_char
        else:
            value += val_char

    return value


# Driver code
def main():
    s = input()
    print(romanToInt(s))

if __name__ == "__main__":
     main()
