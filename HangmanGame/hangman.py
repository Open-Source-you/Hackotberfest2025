import random
import os

class HangmanGame:
    def __init__(self):
        # Word lists by difficulty
        self.easy_words = [
            "cat", "dog", "sun", "run", "car", "bat", "hat", "pen", "box", "cup",
            "book", "tree", "fish", "bird", "moon", "star", "rain", "wind", "fire", "snow"
        ]
        
        self.medium_words = [
            "python", "computer", "keyboard", "mouse", "screen", "window", "puzzle", "guitar",
            "bicycle", "rainbow", "flower", "mountain", "ocean", "jungle", "castle", "wizard",
            "dragon", "treasure", "adventure", "friendship"
        ]
        
        self.hard_words = [
            "extraordinary", "unbelievable", "overwhelming", "responsibility", "sophisticated",
            "revolutionary", "transformation", "entertainment", "communication", "imagination",
            "understanding", "development", "independent", "international", "personality"
        ]
        
        # Hangman ASCII art stages
        self.hangman_stages = [
            """
               +---+
               |   |
                   |
                   |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
                   |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
               |   |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
              /|   |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
              /|\\  |
                   |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
              /|\\  |
              /    |
                   |
            =========
            """,
            """
               +---+
               |   |
               O   |
              /|\\  |
              / \\  |
                   |
            =========
            """
        ]
        
        self.word = ""
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.max_guesses = 6
        self.hints_used = 0
        self.difficulty = ""
        
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_welcome(self):
        """Display welcome message and game title."""
        self.clear_screen()
        print("""
 ██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
 ██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
 ███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
 ██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
 ██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║        
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝        

                    🎯 The Classic Word Guessing Game 🎯
        """)
        
    def choose_difficulty(self):
        """Let player choose difficulty level."""
        print("\nChoose Difficulty Level:")
        print("1. 🟢 Easy (3-4 letters)")
        print("2. 🟡 Medium (6-10 letters)")
        print("3. 🔴 Hard (11+ letters)")
        
        while True:
            try:
                choice = input("\nEnter your choice (1-3): ").strip()
                if choice == '1':
                    self.word = random.choice(self.easy_words).upper()
                    self.difficulty = "Easy"
                    break
                elif choice == '2':
                    self.word = random.choice(self.medium_words).upper()
                    self.difficulty = "Medium"
                    break
                elif choice == '3':
                    self.word = random.choice(self.hard_words).upper()
                    self.difficulty = "Hard"
                    break
                else:
                    print("❌ Invalid choice! Please enter 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing! 👋")
                exit()
                
    def display_word(self):
        """Display the current state of the word."""
        display = ""
        for letter in self.word:
            if letter in self.guessed_letters:
                display += letter + " "
            else:
                display += "_ "
        return display.strip()
        
    def display_game_state(self):
        """Display the current game state."""
        self.clear_screen()
        self.display_welcome()
        
        print(f"\nDifficulty: {self.difficulty}")
        print(f"\nCurrent Word:")
        print(f"  {self.display_word()}")
        
        print(f"\nGame Status:")
        print(f"  Wrong guesses: {self.incorrect_guesses}/{self.max_guesses}")
        print(f"  Remaining guesses: {self.max_guesses - self.incorrect_guesses}")
        
        if self.guessed_letters:
            correct_guesses = [letter for letter in self.guessed_letters if letter in self.word]
            wrong_guesses = [letter for letter in self.guessed_letters if letter not in self.word]
            
            if correct_guesses:
                print(f"  ✅ Correct letters: {', '.join(sorted(correct_guesses))}")
            if wrong_guesses:
                print(f"  ❌ Wrong letters: {', '.join(sorted(wrong_guesses))}")
        
        print(self.hangman_stages[self.incorrect_guesses])
        
    def get_hint(self):
        """Provide a hint to the player."""
        if self.hints_used >= 2:
            print("❌ You've used all your hints!")
            return
            
        unrevealed_letters = [letter for letter in self.word if letter not in self.guessed_letters]
        if unrevealed_letters:
            hint_letter = random.choice(unrevealed_letters)
            self.guessed_letters.add(hint_letter)
            self.hints_used += 1
            print(f"💡 Hint: The letter '{hint_letter}' is in the word!")
            print(f"   You have {2 - self.hints_used} hints remaining.")
        else:
            print("🎉 You've already found all the letters!")
            
    def is_word_complete(self):
        """Check if the word is completely guessed."""
        return all(letter in self.guessed_letters for letter in self.word)
        
    def play_round(self):
        """Play a single round of hangman."""
        while self.incorrect_guesses < self.max_guesses:
            self.display_game_state()
            
            if self.is_word_complete():
                print(f"🎉 Congratulations! You guessed the word: {self.word}")
                print(f"📊 Game Stats:")
                print(f"   - Difficulty: {self.difficulty}")
                print(f"   - Wrong guesses: {self.incorrect_guesses}/{self.max_guesses}")
                print(f"   - Hints used: {self.hints_used}/2")
                return True
                
            try:
                guess = input("\nEnter a letter (or 'hint' for a clue): ").upper().strip()
                
                if guess == 'HINT':
                    self.get_hint()
                    input("\nPress Enter to continue...")
                    continue
                    
                if len(guess) != 1 or not guess.isalpha():
                    print("❌ Please enter a single letter!")
                    input("Press Enter to continue...")
                    continue
                    
                if guess in self.guessed_letters:
                    print(f"❌ You already guessed '{guess}'!")
                    input("Press Enter to continue...")
                    continue
                    
                self.guessed_letters.add(guess)
                
                if guess in self.word:
                    print(f"✅ Great! '{guess}' is in the word!")
                else:
                    self.incorrect_guesses += 1
                    print(f"❌ Sorry, '{guess}' is not in the word.")
                    
                if not self.is_word_complete():
                    input("Press Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Thanks for playing! 👋")
                return False
                
        # Game over - player lost
        self.display_game_state()
        print(f"💀 Game Over! The word was: {self.word}")
        print("Better luck next time! 🎮")
        return False
        
    def play_again(self):
        """Ask if player wants to play again."""
        while True:
            try:
                choice = input("\n🎮 Would you like to play again? (y/n): ").lower().strip()
                if choice in ['y', 'yes']:
                    return True
                elif choice in ['n', 'no']:
                    return False
                else:
                    print("❌ Please enter 'y' for yes or 'n' for no.")
            except KeyboardInterrupt:
                print("\n\nThanks for playing! 👋")
                return False
                
    def reset_game(self):
        """Reset game state for a new round."""
        self.word = ""
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.hints_used = 0
        self.difficulty = ""
        
    def run(self):
        """Main game loop."""
        self.display_welcome()
        print("\n🎯 Welcome to Hangman!")
        print("Guess the word letter by letter. You have 6 wrong guesses before the game ends.")
        print("Type 'hint' to get a clue (you get 2 hints per game).")
        input("\nPress Enter to start...")
        
        while True:
            self.reset_game()
            self.choose_difficulty()
            self.play_round()
            
            if not self.play_again():
                self.clear_screen()
                print("""
🎯 Thanks for playing Hangman! 🎯

Hope you had fun guessing words! 🎮
Come back anytime for more word challenges! 🌟

                Goodbye! 👋
                """)
                break

if __name__ == "__main__":
    game = HangmanGame()
    game.run()