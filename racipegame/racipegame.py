import random
import time

recipes = {
    "easy": {
        "pizza": ["flour", "cheese", "tomato", "salt"],
        "sandwich": ["bread", "butter", "cheese", "ham"],
        "juice": ["water", "orange", "sugar", "ice"],
    },
    "medium": {
        "pasta": ["flour", "eggs", "salt", "water", "garlic", "olive oil"],
        "cake": ["flour", "sugar", "eggs", "butter", "vanilla", "baking powder"],
        "soup": ["water", "vegetables", "salt", "spices", "garlic", "onion"],
        "tacos": ["tortilla", "meat", "cheese", "lettuce", "tomato", "salsa"],
    },
    "hard": {
        "lasagna": ["pasta", "meat", "tomato sauce", "cheese", "eggs", "garlic", "onion", "spices"],
        "risotto": ["rice", "broth", "wine", "butter", "cheese", "onion", "garlic", "mushrooms"],
        "pad thai": ["noodles", "shrimp", "eggs", "peanuts", "lime", "fish sauce", "garlic", "chili"],
        "sushi": ["rice", "seaweed", "fish", "cucumber", "avocado", "soy sauce", "wasabi", "vinegar"],
    }
}

class RecipeGame:
    def __init__(self):
        self.total_score = 0
        self.level = 1
        self.stats = {"correct": 0, "wrong": 0, "hints_used": 0}
    
    def display_menu(self):
        print("\n" + "="*50)
        print("🍳 RECIPE MASTER GAME 🍳".center(50))
        print("="*50)
        print("\n1. Play Easy")
        print("2. Play Medium")
        print("3. Play Hard")
        print("4. View Stats")
        print("5. Quit")
        return input("\nChoose option (1-5): ").strip()
    
    def play_round(self, difficulty):
        recipe_name = random.choice(list(recipes[difficulty].keys()))
        ingredients = recipes[difficulty][recipe_name]
        guessed = []
        wrong_attempts = 0
        hints_left = 2
        round_score = 0
        start_time = time.time()
        
        print(f"\n{'='*50}")
        print(f"🎯 Level: {self.level} | Difficulty: {difficulty.upper()}")
        print(f"{'='*50}")
        print(f"📝 Guess all {len(ingredients)} ingredients!")
        print(f"⏱️  Time started: {time.strftime('%H:%M:%S')}")
        print(f"💡 Hints remaining: {hints_left}\n")
        
        while len(guessed) < len(ingredients) and wrong_attempts < 5:
            remaining = len(ingredients) - len(guessed)
            guess = input(f"Guess ingredient ({len(guessed)}/{len(ingredients)}): ").lower().strip()
            
            if not guess:
                continue
            
            if guess == "quit":
                print(f"\n❌ Quitting... Recipe was: {recipe_name.upper()}")
                return 0
            
            if guess == "hint":
                if hints_left > 0:
                    hint_ingredients = [ing for ing in ingredients if ing not in guessed]
                    hint = random.choice(hint_ingredients)
                    print(f"💡 Hint: {hint}\n")
                    hints_left -= 1
                    self.stats["hints_used"] += 1
                else:
                    print("❌ No hints left!\n")
                continue
            
            if guess == "show":
                print(f"Ingredients: {', '.join(ingredients)}\n")
                continue
            
            if guess in ingredients and guess not in guessed:
                guessed.append(guess)
                points = max(10 - wrong_attempts, 5)
                round_score += points
                print(f"✅ Correct! +{points} points ({len(guessed)}/{len(ingredients)})\n")
                self.stats["correct"] += 1
            elif guess in guessed:
                print("⚠️  Already guessed!\n")
            else:
                wrong_attempts += 1
                print(f"❌ Wrong! ({wrong_attempts}/5)\n")
                self.stats["wrong"] += 1
        
        if len(guessed) == len(ingredients):
            elapsed = int(time.time() - start_time)
            time_bonus = max(50 - elapsed, 0)
            round_score += time_bonus
            print(f"\n{'='*50}")
            print(f"🎉 RECIPE COMPLETE: {recipe_name.upper()}!")
            print(f"Time: {elapsed}s | Time Bonus: +{time_bonus}")
            print(f"Round Score: {round_score}")
            print(f"{'='*50}\n")
            self.level += 1
            return round_score
        else:
            print(f"\n❌ Game Over! You reached {len(guessed)}/{len(ingredients)} ingredients")
            print(f"Recipe was: {recipe_name.upper()}\n")
            return 0
    
    def view_stats(self):
        print(f"\n{'='*50}")
        print("📊 GAME STATISTICS".center(50))
        print(f"{'='*50}")
        print(f"Total Score: {self.total_score}")
        print(f"Current Level: {self.level}")
        print(f"Correct Guesses: {self.stats['correct']}")
        print(f"Wrong Guesses: {self.stats['wrong']}")
        print(f"Hints Used: {self.stats['hints_used']}")
        if self.stats['correct'] + self.stats['wrong'] > 0:
            accuracy = (self.stats['correct'] / (self.stats['correct'] + self.stats['wrong'])) * 100
            print(f"Accuracy: {accuracy:.1f}%")
        print(f"{'='*50}\n")
    
    def run(self):
        while True:
            choice = self.display_menu()
            
            if choice == "1":
                score = self.play_round("easy")
                self.total_score += score
            elif choice == "2":
                score = self.play_round("medium")
                self.total_score += score
            elif choice == "3":
                score = self.play_round("hard")
                self.total_score += score
            elif choice == "4":
                self.view_stats()
            elif choice == "5":
                print(f"\n🏆 Final Score: {self.total_score} | Level Reached: {self.level}")
                print("Thanks for playing! 👋\n")
                break
            else:
                print("❌ Invalid choice!")

if __name__ == "__main__":
    game = RecipeGame()
    game.run()