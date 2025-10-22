# create a python game where the user plays rock-paper-scissors
# against the computer until they type "quit".
# The computer's choice should be random

import random
# a=1
# b=6
# print(random.randint(a,b))



number = random.randint(0,2)
while True:
    user_move = input("Input something:  ")
    # if user_move == "quit":
    #     break
if(number == 0 ):
    print("Rock")
    if user_move == "Rock":
        print("Draw")
    elif (user_move == "Scissors"):
        print("Computer wins")
    else:
        print("User Wins!!")
elif(number==1):
    print("Scissors")
    if user_move == "Rock":
        print("User Wins!!")
    elif (user_move == "Scissors"):
        print("Draw")
    else:
        print("Computer wins!!")
else:
    print("Paper")
    if user_move == "Rock":
        print("Computer Wins!!")
    elif (user_move == "Scissors"):
        print("User Wins!!")
    else:
        print("Draw")

        