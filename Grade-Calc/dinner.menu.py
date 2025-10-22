import random


def pick_dinner():
    # List of dinner options
    dinner_options = [
        "Spaghetti Bolognese",
        "Grilled Chicken with Vegetables",
        "Tacos with Beef and Salsa",
        "Vegetable Stir Fry with Rice",
        "Salmon with Asparagus",
        "Homemade Pizza",
        "Beef Stroganoff",
        "Quinoa Salad with Chickpeas",
        "Shrimp Curry",
        "Stuffed Bell Peppers",
    ]

    # Randomly select a dinner option
    selected_dinner = random.choice(dinner_options)

    return selected_dinner


# Pick and print a dinner option
if __name__ == "__main__":
    dinner = pick_dinner()
    print(f"Tonight's dinner option is: {dinner}")
