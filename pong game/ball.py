from turtle import Turtle

class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.color("white")
        self.shape("circle")
        self.x_move = 10
        self.y_move = 10
        self.move_speed = 0.06

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x,new_y)

    def bounce(self):
        self.y_move *= -1

    def bounce_back(self):
        self.x_move *= -1
        self.move_speed *= 0.9

    def go(self):
        self.x_move *= -1
        self.y_move *= -1

    def reset_position(self):
        self.goto(0,0)
        self.move_speed = 0.06
        self.bounce_back()