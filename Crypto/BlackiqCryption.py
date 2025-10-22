import sys

# Encryption/Decryption Mapping
CHAR_MAP = {
    "a": "!",
    "b": "@",
    "c": "#",
    "d": "$",
    "e": "%",
    "f": "^",
    "g": "&",
    "h": "*",
    "i": "(",
    "j": "-",
    "k": "+",
    "l": "=",
    "m": "_",
    "n": "/",
    "o": "|",
    "p": "}",
    "q": "{",
    "r": "]",
    "s": "[",
    "t": ")",
    "u": ":",
    "v": ";",
    "w": ",",
    "x": ">",
    "y": "<",
    "z": "'",
    "A": "!",
    "B": "@",
    "C": "#",
    "D": "$",
    "E": "%",
    "F": "^",
    "G": "&",
    "H": "*",
    "I": "(",
    "J": "-",
    "K": "+",
    "L": "=",
    "M": "_",
    "N": "/",
    "O": "|",
    "P": "}",
    "Q": "{",
    "R": "]",
    "S": "[",
    "T": ")",
    "U": ":",
    "V": ";",
    "W": ",",
    "X": ">",
    "Y": "<",
    "Z": "'",
    " ": " ",
    ".": ".",
}

REVERSE_MAP = {v: k for k, v in CHAR_MAP.items()}


# Utility functions for encryption and decryption
def encrypt(text):
    """Encrypts the given text using the CHAR_MAP."""
    encrypted_text = "".join([CHAR_MAP.get(ch, ch) for ch in text])
    return encrypted_text


def decrypt(text):
    """Decrypts the given text using the REVERSE_MAP."""
    decrypted_text = "".join([REVERSE_MAP.get(ch, ch) for ch in text])
    return decrypted_text


def validate_input(option, text):
    """Validates user input for encryption/decryption."""
    if option not in ["C", "E"]:
        print("Invalid option. Please choose 'C' for encryption or 'E' for decryption.")
        sys.exit(1)
    if not text.strip():
        print("Input text cannot be empty.")
        sys.exit(1)


def main():
    print("Welcome to BlackIQCryption")
    print("Choose an option: ")
    print("C - Cryption (Encryption)")
    print("E - Encryotion (Decryption)")

    option = input("What do you want? C or E: ").strip().upper()
    text = input("Enter your text: ").strip()

    # Validate inputs
    validate_input(option, text)

    if option == "C":
        result = encrypt(text)
        print(f"Encrypted Text: {result}")
    elif option == "E":
        result = decrypt(text)
        print(f"Decrypted Text: {result}")


if __name__ == "__main__":
    main()
