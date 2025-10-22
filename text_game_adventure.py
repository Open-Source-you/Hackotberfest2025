import random
import tkinter as tk
from tkinter import messagebox


class AdventureGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Adventure Game")
        self.health = 100
        self.inventory = []

        self.label = tk.Label(master, text="Welcome to the Adventure Game!\nYou find yourself in a dark forest.", wraplength=300)
        self.label.pack(pady=20)

        self.health_label = tk.Label(master, text="Health: 100")
        self.health_label.pack(pady=10)

        self.inventory_label = tk.Label(master, text="Inventory: []")
        self.inventory_label.pack(pady=10)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        self.start_buttons()

    def start_buttons(self):
        self.clear_buttons()
        self.label.config(text="You can:")
        self.create_button("Go deeper into the forest", self.deep_forest)
        self.create_button("Climb a nearby tree", self.climb_tree)
        self.create_button("Sit down and rest", self.rest)
        self.create_button("Check crafting recipes", self.check_recipes)

    def create_button(self, text, command):
        button = tk.Button(self.button_frame, text=text, command=command)
        button.pack(pady=5)

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def update_inventory_display(self):
        if self.inventory:
            self.inventory_label.config(text=f"Inventory: {', '.join(self.inventory)}")
        else:
            self.inventory_label.config(text="Inventory: []")

    def update_health_display(self):
        self.health_label.config(text=f"Health: {self.health}")

    def deep_forest(self):
        self.clear_buttons()
        self.label.config(text="You venture deeper into the forest.\nSuddenly, you encounter a wild bear!")
        self.create_button("Fight the bear", self.fight_bear)
        self.create_button("Run away", self.run_away)
         self.label = tk.Label(master, text="Welcome to the Adventure Game!\nYou find yourself in a dark forest.", wraplength=300)
        self.label.pack(pady=20)

        self.health_label = tk.Label(master, text="Health: 100")
        self.health_label.pack(pady=10)

        self.inventory_label = tk.Label(master, text="Inventory: []")
        self.inventory_label.pack(pady=10)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()
 self.label = tk.Label(master, text="Welcome to the Adventure Game!\nYou find yourself in a dark forest.", wraplength=300)
        self.label.pack(pady=20)

        self.health_label = tk.Label(master, text="Health: 100")
        self.health_label.pack(pady=10)

        self.inventory_label = tk.Label(master, text="Inventory: []")
        self.inventory_label.pack(pady=10)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()


    def climb_tree(self):
        self.clear_buttons()
        self.label.config(text="You climb the tree and see a cave nearby.")
        self.create_button("Go to the cave", self.cave)
        self.create_button("Look for food in the forest", self.find_food)

    def rest(self):
        self.health += 20
        if self.health > 100:
            self.health = 100
        self.clear_buttons()
        self.label.config(text=f"You sit down and rest. Your health is now {self.health}.")
        self.update_health_display()
        self.start_buttons()

    def find_food(self):
        food_items = ["apple", "berry", "mushroom", "herb", "nut"]
        found_food = random.choice(food_items)
        self.inventory.append(found_food)
        self.clear_buttons()
        self.label.config(text=f"You found a {found_food}!")
        self.update_inventory_display()
        self.create_button("Continue exploring", self.start_buttons)

    def fight_bear(self):
        self.health -= 50
        self.update_health_display()
        if self.health <= 0:
            self.game_over()
        else:
            self.clear_buttons()
            self.label.config(text=f"You fought bravely and defeated the bear!\nYour health is now {self.health}.")
            self.create_button("Search the bear's cave", self.cave)
            self.create_button("Return to the forest", self.start_buttons)

    def run_away(self):
        self.clear_buttons()
        self.label.config(text="You run away safely but are now lost.")
        self.start_buttons()

    def cave(self):
        self.clear_buttons()
        self.label.config(text="You enter the cave and find a treasure chest!")
        self.create_button("Open the chest", self.open_chest)
        self.create_button("Leave the cave", self.leave_cave)

    def open_chest(self):
        treasures = ["gold coins", "a healing potion", "silver coins", "ancient scroll"]
        found_treasure = random.choice(treasures)
        self.inventory.append(found_treasure)
        self.clear_buttons()
        self.label.config(text=f"You found {found_treasure} in the chest!")
        self.update_inventory_display()
        self.create_button("Leave the cave", self.leave_cave)

    def leave_cave(self):
        self.clear_buttons()
        self.label.config(text="You decide to leave the cave.")
        self.start_buttons()

    def check_recipes(self):
        self.clear_buttons()
        self.label.config(text="Crafting Recipes:\n"
                              "1. Healing Potion: apple + berry\n"
                              "2. Magic Sword: gold coins\n"
                              "3. Nutty Bread: nut + herb + mushroom\n"
                              "4. Ancient Tome: ancient scroll + magical sword")
        self.create_button("Try to craft Healing Potion", self.craft_healing_potion)
        self.create_button("Try to craft Magic Sword", self.craft_magic_sword)
        self.create_button("Try to craft Nutty Bread", self.craft_nutty_bread)
        self.create_button("Try to craft Ancient Tome", self.craft_ancient_tome)
        self.create_button("Go back", self.start_buttons)

    def craft_healing_potion(self):
        if "apple" in self.inventory and "berry" in self.inventory:
            self.inventory.remove("apple")
            self.inventory.remove("berry")
            self.inventory.append("Healing Potion")
            messagebox.showinfo("Crafting", "You crafted a Healing Potion!")
        else:
            messagebox.showwarning("Crafting Failed", "You need an apple and a berry to craft a Healing Potion.")
        self.update_inventory_display()
        self.check_recipes()

    def craft_magic_sword(self):
        if "gold coins" in self.inventory in self.inventory:
            self.inventory.remove("a magical sword")
            self.inventory.append("Magic Sword")
            messagebox.showinfo("Crafting", "You crafted a Magic Sword!")
        else:
            messagebox.showwarning("Crafting Failed", "You need gold coins and a magical sword to craft a Magic Sword.")
        self.update_inventory_display()
        self.check_recipes()

    def craft_nutty_bread(self):
        if "nut" in self.inventory and "herb" in self.inventory and "mushroom" in self.inventory:
            self.inventory.remove("nut")
            self.inventory.remove("herb")
            self.inventory.remove("mushroom")
            self.inventory.append("Nutty Bread")
            messagebox.showinfo("Crafting", "You crafted Nutty Bread!")
        else:
            messagebox.showwarning("Crafting Failed", "You need a nut, an herb, and a mushroom to craft Nutty Bread.")
        self.update_inventory_display()
        self.check_recipes()

    def craft_ancient_tome(self):
        if "ancient scroll" in self.inventory and "a magical sword" in self.inventory:
            self.inventory.remove("ancient scroll")
            self.inventory.remove("a magical sword")
            self.inventory.append("Ancient Tome")
            messagebox.showinfo("Crafting", "You crafted an Ancient Tome!")
        else:
            messagebox.showwarning("Crafting Failed", "You need an ancient scroll and a magical sword to craft an Ancient Tome.")
        self.update_inventory_display()
        self.check_recipes()

    def game_over(self):
        messagebox.showinfo("Game Over", "You fought bravely but the bear overpowered you. Game over.")
        self.restart()

    def restart(self):
        self.health = 100
        self.inventory = []
        self.clear_buttons()
        self.label.config(text="Welcome to the Adventure Game!\nYou find yourself in a dark forest.")
        self.update_health_display()
        self.update_inventory_display()
        self.start_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    game = AdventureGame(root)
    root.mainloop()
