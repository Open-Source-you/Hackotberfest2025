#!/usr/bin/env python3
"""
Night City Skyline Generator

A Turtle graphics program that generates a random city skyline
with buildings of varying heights and randomly placed windows.

Author: Madhan Kumar R
Date: 2025-10-16
License: MIT
"""

import turtle
import random


def draw_building(x, y, width, height, pen):
    """
    Draw a single building with random windows.

    Args:
        x: X-coordinate of building bottom-left corner.
        y: Y-coordinate of building bottom-left corner.
        width: Width of the building.
        height: Height of the building.
        pen: Turtle graphics pen object.
    """
    pen.penup()
    pen.goto(x, y)
    pen.pendown()

    # Draw building outline
    pen.fillcolor("gray20")
    pen.begin_fill()
    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)
    pen.end_fill()

    # Draw random windows
    window_size = 8
    window_spacing = 12
    rows = int(height // window_spacing)
    cols = int(width // window_spacing)

    for row in range(rows - 1):
        for col in range(cols - 1):
            if random.random() > 0.3:  # 70% chance of window
                win_x = x + col * window_spacing + 2
                win_y = y + height - (row + 1) * window_spacing - 2
                pen.penup()
                pen.goto(win_x, win_y)
                pen.pendown()
                pen.fillcolor("yellow")
                pen.begin_fill()
                for _ in range(4):
                    pen.forward(window_size)
                    pen.left(90)
                pen.end_fill()


def create_gradient_background(screen, width, height):
    """
    Create a gradient dark blue background.

    Args:
        screen: Turtle screen object.
        width: Screen width.
        height: Screen height.
    """
    pen = turtle.Turtle()
    pen.speed(0)
    pen.hideturtle()

    # Create gradient from dark blue to lighter blue
    y_start = height / 2
    num_stripes = height

    for i in range(num_stripes):
        # Gradient from navy (0, 0, 50) to darker blue (25, 25, 112)
        ratio = i / num_stripes
        r = int(0 + 25 * ratio)
        g = int(0 + 25 * ratio)
        b = int(50 + 62 * ratio)
        color = (r / 255, g / 255, b / 255)

        pen.pencolor(color)
        pen.speed(11)
        pen.pensize(5)
        pen.penup()
        pen.goto(-width / 2, y_start - i)
        pen.pendown()
        pen.forward(width)

    pen.hideturtle()


def main():
    """Main function to generate and display the city skyline."""
    screen = turtle.Screen()
    screen.setup(width=1000, height=600)
    screen.bgcolor("black")
    screen.title("Night City Skyline")

    # Create gradient background
    create_gradient_background(screen, 1000, 600)

    pen = turtle.Turtle()
    pen.speed(11)
    pen.hideturtle()

    # Generate buildings across the screen width
    building_count = 10
    screen_width = 1000
    building_width = screen_width // building_count
    ground_y = -200

    for i in range(building_count):
        building_x = -500 + i * building_width
        building_height = random.randint(80, 280)
        draw_building(building_x, ground_y, building_width - 5,
                      building_height, pen)

    # Draw ground line
    pen.penup()
    pen.goto(-500, ground_y)
    pen.pendown()
    pen.pencolor("darkgray")
    pen.pensize(3)
    pen.forward(1000)

    pen.hideturtle()
    screen.update()
    screen.mainloop()


if __name__ == "__main__":
    main()
