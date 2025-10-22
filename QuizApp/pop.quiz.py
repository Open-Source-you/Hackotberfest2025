def pop_quiz():
    # Define the questions and their corresponding answers
    questions = {
        "What is the capital of France?": "Paris",
        "What is 5 + 7?": "12",
        "Who wrote 'Romeo and Juliet'?": "Shakespeare",
    }

    score = 0  # Initialize the score

    # Loop through the questions
    for question, answer in questions.items():
        # Ask the user the question
        user_answer = input(question + " ").strip()

        # Check if the answer is correct
        if user_answer.lower() == answer.lower():
            print("Correct!")
            score += 1  # Increment the score for a correct answer
        else:
            print(f"Wrong! The correct answer is: {answer}")

    # Display the final score
    print(f"\nYour final score is: {score}/{len(questions)}")


# Run the pop quiz
if __name__ == "__main__":
    pop_quiz()
