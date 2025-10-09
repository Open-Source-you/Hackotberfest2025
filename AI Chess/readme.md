# AI Chess Game

A modern chess game implementation featuring an AI opponent using Stockfish engine, built with Python, Pygame, and python-chess.

![Chess Game Screenshot](screenshots/gameplay.png)

## Features

- 🤖 AI opponent powered by Stockfish engine
- 🎮 Intuitive graphical interface using Pygame
- ⚡ Real-time move validation and game state tracking
- 🎨 Beautiful piece and board rendering
- ⏱️ Game timer with timeout detection
- 📊 Move history and game state tracking
- 🎯 Legal move highlighting
- 🏆 Checkmate and draw detection
- 🎨 Customizable board colors
- 🖱️ Smooth piece movement animations

## Requirements

- Python 3.8 or higher
- Pygame 2.0 or higher
- python-chess library
- Stockfish chess engine

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-chess-game.git
cd ai-chess-game
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Download and install Stockfish:
   - Download Stockfish from [official website](https://stockfishchess.org/download/)
   - Place the Stockfish executable in the project directory
   - Make sure it's named `stockfish.exe` (Windows) or `stockfish` (Linux/Mac)

## Usage

Run the game:
```bash
python enhanced_chess.py
```

### Game Controls

- Left-click to select a piece
- Left-click on a valid move to make the move
- Right-click to deselect a piece
- ESC to exit the game

### AI Settings

The AI difficulty can be adjusted by modifying the `time_limit` parameter in the `ChessGame` class:
```python
self.engine.set_skill_level(20)  # Range: 0-20
self.engine.set_depth(20)        # Range: 1-20
```

## Project Structure

```
ai-chess-game/
├── enhanced_chess.py    # Main game implementation
├── chess_game.py        # Core chess logic
├── create_pieces.py     # Piece creation and rendering
├── requirements.txt     # Python dependencies
├── stockfish/          # Stockfish engine directory
└── README.md           # This file
```

## Technical Details

### AI Implementation
- Uses Stockfish engine for move generation and evaluation
- Configurable skill level and search depth
- Multi-threaded analysis support
- Opening book integration

### Game Engine
- Bitboard representation for efficient move generation
- Legal move validation
- Check and checkmate detection
- Draw detection (stalemate, insufficient material, etc.)

### UI Features
- Smooth piece movement animations
- Legal move highlighting
- Game state indicators
- Timer display
- Move history

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [python-chess](https://github.com/niklasf/python-chess) - Chess library for Python
- [Stockfish](https://stockfishchess.org/) - Chess engine
- [Pygame](https://www.pygame.org/) - Python game development library

## Contact

Your Name - Aamod Kumar((https://www.linkedin.com/in/aamod-kumar-9882782ab/))

