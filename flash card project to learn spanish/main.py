import pandas
from tkinter import *
import random
word_data = pandas.read_csv("spanish_word.csv")
word_meaning_dict=word_data.to_dict(orient="records")
random_card={}

def tick_button():
    global random_card, flip_timer
    window.after_cancel(flip_timer)
    try:
        to_learn_data = pandas.read_csv("words_to_learn.csv")
    except FileNotFoundError:

        random_card = random.choice(word_meaning_dict)
        word_meaning_dict.remove(random_card)
        updated_data = pandas.DataFrame(word_meaning_dict)
        updated_data.to_csv("words_to_learn.csv",index=False)
    else:
        to_learn_dict = to_learn_data.to_dict(orient="records")
        random_card = random.choice(to_learn_dict)
        to_learn_dict.remove(random_card)
        updated_data = pandas.DataFrame(to_learn_dict)
        updated_data.to_csv("words_to_learn.csv", index=False)
    finally:
        canvas.itemconfig(title, text="Spanish", fill="black")
        canvas.itemconfig(word, text=random_card["Spanish"], fill="black")
        canvas.itemconfig(image, image=card_front)
        flip_timer = window.after(5000, flip_card)


def word_generator():
    global random_card, flip_timer
    window.after_cancel(flip_timer)
    random_card = random.choice(word_meaning_dict)
    canvas.itemconfig(title, text="Spanish", fill="black")
    canvas.itemconfig(word, text=random_card["Spanish"], fill="black")
    canvas.itemconfig(image, image=card_front)
    flip_timer = window.after(5000, flip_card)

def flip_card():
    canvas.itemconfig(image, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, fill="white",text=random_card["English"])

green = "#B1DDC6"

window=Tk()
window.title("Flashy")
window.config(bg=green)
window.config(padx=50,pady=50)
flip_timer = window.after(5000, flip_card)

card_front=PhotoImage(file="card_front.png")
card_back=PhotoImage(file="card_back.png")
canvas=Canvas(width=800, height=526)
canvas.grid(row=0, column=0, columnspan=2)
canvas.config(bg=green, highlightthickness=0)
image=canvas.create_image(400, 263, image=card_front)
title=canvas.create_text(400, 150, text="", font=("Ariel", 45, "italic"))
word=canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))



cross_image=PhotoImage(file="wrong.png")
cross_button =Button(image=cross_image,highlightthickness=0,height=60,width=60,pady=50,command=word_generator)
cross_button.grid(row=1,column=0)

tick_image=PhotoImage(file="right.png")
check_button =Button(image=tick_image,highlightthickness=0,height=60,width=60,pady=50,command=tick_button)
check_button.grid(row=1,column=1)
word_generator()

window.mainloop()
