"""
hangman.py
Simple terminal Hangman game.
Usage: python hangman.py
If a file named 'words.txt' is present in the same folder (one word per line),
the game will use words from that file. Otherwise it uses the built-in list.
"""

import random
import sys
import os

HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
         |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    /    |
         |
    =========""",
    """
     +---+
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    ========="""
]


DEFAULT_WORDS = [
    "python", "hangman", "programming", "developer", "algorithm",
    "function", "variable", "keyboard", "project", "computer",
    "internet", "package", "repository", "github", "challenge"
]


def load_words(filename="words.txt"):
    if os.path.isfile(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                words = [w.strip() for w in f if w.strip()]
            if words:
                return words
        except Exception:
            pass
    return DEFAULT_WORDS


def choose_word(words):
    return random.choice(words).lower()


def display_state(missed_letters, correct_letters, secret_word):
    print(HANGMAN_PICS[len(missed_letters)])
    print()
    # Show missed letters
    print("Missed letters:", " ".join(missed_letters) if missed_letters else "(none)")
    # Show the word with blanks
    blanks = [letter if letter in correct_letters else "_" for letter in secret_word]
    print("Word:", " ".join(blanks))
    print()


def get_guess(already_guessed):
    while True:
        guess = input("Guess a letter (or '!quit' to exit): ").strip().lower()
        if guess == "!quit":
            print("Quitting game. Bye!")
            sys.exit(0)
        if len(guess) != 1:
            print("Please enter a single letter.")
            continue
        if not guess.isalpha():
            print("Please enter a letter (a-z).")
            continue
        if guess in already_guessed:
            print("You already guessed that letter. Try again.")
            continue
        return guess


def play_again():
    while True:
        ans = input("Play again? (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please answer 'y' or 'n'.")


def main():
    print("Welcome to Hangman!\n")
    words = load_words()
    while True:
        secret_word = choose_word(words)
        missed_letters = []
        correct_letters = []
        game_over = False

        while True:
            display_state(missed_letters, correct_letters, secret_word)
            # check for win
            if all(letter in correct_letters for letter in secret_word):
                print(f"Congratulations — you guessed the word: {secret_word}")
                game_over = True
                break
            # check for lose
            if len(missed_letters) >= (len(HANGMAN_PICS) - 1):
                display_state(missed_letters, correct_letters, secret_word)
                print(f"Sorry — you've been hanged! The word was: {secret_word}")
                game_over = True
                break

            guess = get_guess(missed_letters + correct_letters)

            if guess in secret_word:
                correct_letters.append(guess)
                print(f"Good guess: '{guess}' is in the word.\n")
            else:
                missed_letters.append(guess)
                print(f"Sorry: '{guess}' is NOT in the word.\n")

        if not play_again():
            print("Thanks for playing Hangman — goodbye!")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Bye!")
        sys.exit(0)
