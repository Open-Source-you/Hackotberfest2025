import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

# User Choice

user = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors."))

if user == 0:
    print(rock)
elif user == 1:
    print(paper)
elif user == 2:
    print(scissors)
else:
    print("You typed an invalid number, you lose!")
    exit()

# Computer Choice

botPlay = random.randint(0, 2)
if botPlay == 0:
    print(f'Computer chose:{rock}')
elif botPlay == 1:
    print(f'Computer chose:{paper}')
else:
    print(f'Computer chose:{scissors}')

# Who wins?
## Draw cases
if user == botPlay:
    print("Its a draw")


## User win cases
elif user == 0 and botPlay == 2:
    print("You win!")
elif user == 2 and botPlay == 1:
    print("You win!")
elif user == 1 and botPlay == 0:
    print("You win!")

## User lose cases
elif user == 2 and botPlay == 0:
    print("You lose!")
elif user ==  1 and botPlay == 2:
    print("You lose!")
elif user == 0 and botPlay == 1:
    print("You lose!")
