import random


def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I have selected a number between 1 and 100. Try to guess it!")

    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        # Get the user's guess
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            # Check if the guess is too low, too high, or correct
            if guess < secret_number:
                print("Too low! Try again.")
            elif guess > secret_number:
                print("Too high! Try again.")
            else:
                print(
                    f"Congratulations! You've guessed the number {secret_number} in {attempts} attempts."
                )
                break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 100.")


if __name__ == "__main__":
    number_guessing_game()
