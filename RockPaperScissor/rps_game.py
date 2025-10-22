# rps_app.py

import streamlit as st
import random

st.title("🪨 Rock Paper Scissors 🎮")

choices = ["Rock", "Paper", "Scissors"]
ascii_art = {
    "Rock": '''
        _______
    ---'   ____)
          (_____)
          (_____)
          (____)
    ---.__(___)
    ''',
    "Paper": '''
        _______
    ---'   ____)____
              ______)
              _______)
             _______)
    ---.__________)
    ''',
    "Scissors": '''
        _______
    ---'   ____)____
              ______)
           __________)
          (____)
    ---.__(___)
    '''
}

user_choice = st.selectbox("Choose your move:", choices)

if st.button("Play"):
    comp_choice = random.choice(choices)
    
    st.subheader("Your Choice:")
    st.code(ascii_art[user_choice], language="")   # 👈 Better formatting
    
    st.subheader("Computer's Choice:")
    st.code(ascii_art[comp_choice], language="")   # 👈 Looks neat
    
    if user_choice == comp_choice:
        st.success("It's a draw!")
    elif (user_choice == "Rock" and comp_choice == "Scissors") or \
         (user_choice == "Paper" and comp_choice == "Rock") or \
         (user_choice == "Scissors" and comp_choice == "Paper"):
        st.success("You win! 🎉")
    else:
        st.error("You lose! 😢")
