def explore_library(self):
    print("You enter the library filled with dusty books.")
    found_item = random.choice(["a key", "a mysterious book", "nothing"])
    if found_item == "nothing":
        print("You found nothing of interest.")
    else:
        print(f"You found {found_item}!")
        self.inventory.append(found_item)

    def go_basement(self):
        print("You descend into the dark basement.")
        if "a key" in self.inventory:
            print(
                "You use the key to unlock a hidden door. You've discovered a secret room!"
            )
            self.game_over = True
            print("Congratulations! You solved the mystery!")
        else:
            print("The door is locked. You need to find a key to proceed.")

    def investigate_garden(self):
        print("You stroll through the garden and discover some clues.")
        clue_found = random.choice(["a footprint", "a piece of fabric", "nothing"])
        if clue_found != "nothing":
            print(f"You found {clue_found}!")
            self.inventory.append(clue_found)
        else:
            print("You found nothing unusual in the garden.")

    def check_inventory(self):
        if self.inventory:
            print("Your inventory contains: " + ", ".join(self.inventory))
        else:
            print("Your inventory is empty.")

    def end_game(self):
        print("Thank you for playing! Goodbye!")
        self.game_over = True


if __name__ == "__main__":
    game = MysteryAdventure()
    game.start_game()
