import random

import pyfiglet

# Some cool fonts you can experiment with
fonts = ["slant", "block", "digital", "bubble", "starwars", "doom", "big"]

print("\n✨ Welcome to Gopika's Hacktoberfest Contribution ✨\n")

# Generate ASCII art with random font
banner = pyfiglet.figlet_format("Gopika 🚀", font=random.choice(fonts))

print(banner)
print("💜 Made with love by Gopika 💜")
