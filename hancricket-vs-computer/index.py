import random

print("welcome to the computer vs human hand cricket game, HOPE YOU ENJOY")
print("--------------------------------------------------------------------------------------------------------")
print("****RULES****PLEASE READ AND FOLLOW****\n1)please enter number as only 0,1,2,3,4,5,6.\n2)play slow and carefully.don't enter blank space.\n3)if error comes anywhere please restart program.")
print("--------------------------------------------------------------------------------------------------------")


#toss
oe=str(input("choose odd or even: "))
y=int(input("enter number for toss: "))
x=random.randint(0,6)



z=x+y


if oe=="odd":
    if z%2!=0:
        print("the computer choose: ",x)
        side=str(input("You won the toss!!!! Choose to bat or ball: "))
    elif z%2==0:
        k=random.randint(1,2)
        if k==1:
            side="bat"
            print("the computer choose: ",x)
            print("You lost the toss!!!! computer chooses to ball")
        elif k==2:
            side="ball"
            print("the computer choose: ",x)
            print("You lost the toss!!!! computer chooses to bat")
            
if oe=="even":
    if z%2==0:
        print("the computer choose: ",x)
        side=str(input("You won the toss!!!! Choose to bat or ball: "))
    elif z%2!=0:
        k=random.randint(1,2)
        if k==1:
            side="bat"
            print("the computer choose: ",x)
            print("You lost the toss!!!! computer chooses to ball")
        elif k==2:
            side="ball"
            print("the computer choose: ",x)
            print("You lost the toss!!!! computer chooses to bat")
print("--------------------------------------------------------------------------------------------------------")

#loop
if side == 'bat':
    print("YOU ARE NOW BATTING")
    sum1=0
    sum2=0
    while sum2<=sum1:
        i=int(input("Enter number"))
        z=i in range(0,7)
        r=random.randint(0,6)
        sum1=sum1+i
        ts=sum1+1-i
    
        if i!=r:
            print("the computer choose: ",r)
            print("your current score: ", sum1)
        elif i ==r:
            print("the computer choose: ",r)
            print("YOU ARE OUT!!!!!")
            print("your score was: ",sum1-i)
            print("xxxxxxxxxxxxxxxxx")
            print("the target score is: ",ts)
            print("THE COMPUTER IS BATTING")
            print("xxxxxxxxxxxxxxxxx")
            while sum2<sum1+2:
                l=int(input("enter number"))
                t=random.randint(0,6)
                sum2=sum2+t
                if l!=t and sum2>=ts:
                    print("the computer choose: ",t)
                    print("--------------------------------------------------------------------------------------------------------")
                    print("it's score was: ",sum2)
                    print("YOU LOST!!!!")
                    print("--------------------------------------------------------------------------------------------------------")
                elif l!=t:
                    print("the computer choose: ",t)
                    print("it's score is: ",sum2)
                elif l==t and sum2-t>=ts:
                    print("the computer choose: ",t)
                    print(" THE COMPUTER IS OUT!!!!")
                    print("--------------------------------------------------------------------------------------------------------")
                    print("it's score was: ",sum2-t)
                    print("YOU WON!!!!")
                    print("--------------------------------------------------------------------------------------------------------")
                elif l==t and sum2-t>=ts:
                    print("the computer choose: ",t)
                    print(" THE COMPUTER IS OUT!!!!")
                    print("--------------------------------------------------------------------------------------------------------")
                    print("it's score was: ",sum2-t)
                    print("YOU LOST!!!")
                    print("--------------------------------------------------------------------------------------------------------")




elif side == 'ball':
    print("YOU ARE NOW BALLING")
    sum3=0
    sum4=0
    while True:
        i=int(input("Enter number"))
        r=random.randint(0,6)
        sum3=sum3+r
        ts=sum3+1-r
        if i!=r:
            print("the computer choose: ",r)
            print("it's current score is: ", sum3)
        elif i ==r:
            print("the computer choose: ",r)
            print("THE COMPUTER IS OUT!!!!!")
            print("it's score was: ",sum3-r)
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            print("the target score is: ",ts)
            print("YOU ARE NOW BATTING")
            print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            while sum4<sum3+2:
                l=int(input("enter number"))
                t=random.randint(0,6)
                sum4=sum4+l
                if l!=t and sum4>=ts:
                    print("the computer choose: ",t)
                    print("--------------------------------------------------------------------------------------------------------")
                    print("your score was: ",sum4)
                    print("YOU WON!!!!")
                    print("--------------------------------------------------------------------------------------------------------")
                elif l!=t:
                    print("the computer choose: ",t)
                    print("your score is: ",sum4)
                elif l==t and sum4-l<=ts:
                    print("the computer choose: ",t)
                    print(" YOU ARE OUT!!!!")
                    print("--------------------------------------------------------------------------------------------------------")
                    print("your score was: ",sum4-l)
                    print("YOU LOST!!!!")
                    print("--------------------------------------------------------------------------------------------------------")
                elif l==t and sum4-l>=ts:
                    print("the computer choose: ",t)
                    print(" YOU ARE OUT!!!!")
                    print("--------------------------------------------------------------------------------------------------------")
                    print("your score was: ",sum4-l)
                    print("YOU WON!!!")
                    print("--------------------------------------------------------------------------------------------------------")





                    