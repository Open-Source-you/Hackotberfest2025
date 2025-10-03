# 🎯 Hangman Game

A classic word-guessing game implemented in Python with multiple difficulty levels, hints, and beautiful ASCII art!

## 🎮 How to Play

1. **Choose Difficulty**: Select from Easy, Medium, or Hard difficulty levels
2. **Guess Letters**: Enter one letter at a time to guess the hidden word
3. **Use Hints**: Type 'hint' to reveal a random letter (2 hints per game)
4. **Win or Lose**: Guess the word before making 6 wrong guesses!

## 🚀 Features

- **Three Difficulty Levels**:
  - 🟢 Easy: 3-4 letter words
  - 🟡 Medium: 6-10 letter words
  - 🔴 Hard: 11+ letter words

- **Game Features**:
  - Beautiful ASCII art hangman drawings
  - Colorful emoji indicators
  - Hint system (2 hints per game)
  - Game statistics tracking
  - Play again functionality
  - Clear screen for better UX

- **User Experience**:
  - Input validation
  - Clear game state display
  - Progress tracking
  - Keyboard interrupt handling

## 🎯 How to Run

1. Make sure you have Python installed
2. Navigate to the HangmanGame folder
3. Run the game:

   ```bash
   python hangman.py
   ```

## 📖 Game Rules

1. A random word is selected based on your chosen difficulty
2. You have 6 wrong guesses before losing
3. Guess one letter at a time
4. Use 'hint' to reveal a random letter (limited to 2 hints)
5. Win by guessing all letters in the word
6. Lose if you make 6 incorrect guesses

## 🎨 Screenshots

```text
 ██╗  ██╗ █████╗ ███╗   ██╗ ██████╗ ███╗   ███╗ █████╗ ███╗   ██╗
 ██║  ██║██╔══██╗████╗  ██║██╔════╝ ████╗ ████║██╔══██╗████╗  ██║
 ███████║███████║██╔██╗ ██║██║  ███╗██╔████╔██║███████║██╔██╗ ██║
 ██╔══██║██╔══██║██║╚██╗██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║
 ██║  ██║██║  ██║██║ ╚████║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║        
 ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝        

                    🎯 The Classic Word Guessing Game 🎯

Current Word: P _ T H O N
Game Status:
  Wrong guesses: 1/6
  Remaining guesses: 5
  ✅ Correct letters: H, N, O, P, T
  ❌ Wrong letters: X

               +---+
               |   |
               O   |
                   |
                   |
                   |
            =========
```

## 🛠️ Technical Details

- **Language**: Python 3.x
- **Dependencies**: Standard library only (random, os)
- **Features**: Object-oriented design, clean code structure
- **Compatibility**: Cross-platform (Windows, macOS, Linux)

## 🎯 Game Statistics

The game tracks:

- Difficulty level played
- Number of wrong guesses
- Hints used
- Final result (win/lose)

## 🔧 Customization

You can easily customize the game by:

- Adding new words to the word lists
- Changing difficulty levels
- Modifying the hangman ASCII art
- Adjusting the number of allowed guesses
- Adding new features

## 🤝 Contributing

Feel free to contribute by:

- Adding new word categories
- Improving the user interface
- Adding new features
- Fixing bugs
- Enhancing documentation

## 📝 License

This project is open source and available under the MIT License.

---

Enjoy playing Hangman! 🎮🎯