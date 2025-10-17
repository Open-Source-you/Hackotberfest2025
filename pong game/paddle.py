from turtle import Turtle

class Paddle(Turtle):

    def __init__(self,x_cor,y_cor):
        super().__init__()

        self.penup()
        self.setheading(90)
        self.color("white")
        self.shape("square")
        self.shapesize(stretch_len=5)
        self.speed("fastest")
        self.goto(x_cor, y_cor)


    def move_up(self):
        new_y = self.ycor() + 20
        self.goto(self.xcor(), new_y)

    def move_down(self):
        new_y = self.ycor() - 20
        self.goto(self.xcor(), new_y)