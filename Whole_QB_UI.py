import tkinter as tk
import random
from tkinter import messagebox
import pandas as pd

# Read data from Excel sheet
df = pd.read_excel("quiz_data.xlsx", engine="openpyxl")

# Mapping of answer letters to column indices
answer_mapping = {
    'A': 0,  # Column 2
    'B': 1,  # Column 3
    'C': 2,  # Column 4
    'D': 3,  # Column 5
}

# Extract questions and options from the DataFrame
questions = []
for index, row in df.iterrows():
    question = row[0]
    options = [row[i] for i in range(1, 5)]  # Assuming options are in columns 2 to 5
    correct_answer = row[5]  # Assuming the correct answer is in the 6th column

    # Map the answer letter to the correct column index
    correct_option = answer_mapping.get(correct_answer, -1)  # Default to -1 if not found
    if correct_option == -1:
        print(f"Warning: Invalid answer '{correct_answer}' for question: {question}")
        continue

    questions.append({
        "question": question,
        "options": options,
        "correct_option": correct_option,
    })

# Shuffle the questions randomly
random.shuffle(questions)

# Initialize variables to keep track of the current question and answer status
current_question = 0
score = 0
answered = False

# Function to check the selected option and update UI
def check_answer(option_index):
    global current_question, score, answered

    if answered or current_question >= len(questions):
        return

    answered = True

    if option_index == questions[current_question]["correct_option"]:
        option_buttons[option_index].config(bg="green")
        score += 1
    else:
        option_buttons[option_index].config(bg="red")
        correct_option = questions[current_question]["correct_option"]
        if correct_option < len(option_buttons):
            option_buttons[correct_option].config(bg="green")

    current_question += 1

    if current_question < len(questions):
        root.after(1000, show_question, current_question)  # Wait 1 second before showing the next question
    else:
        messagebox.showinfo("Quiz Finished", f"Your score: {score}/{len(questions)}")
        root.destroy()

# Function to display the current question and options
def show_question(q_num):
    global answered  # Update the global 'answered' variable
    answered = False  # Reset the answer status

    question_label.config(text=questions[q_num]["question"])

    for i, option in enumerate(option_buttons):
        option.config(text=questions[q_num]["options"][i], bg="SystemButtonFace")

# Create the main window with a fixed 1:1 aspect ratio and a larger size
root = tk.Tk()
root.title("MCQ Quiz")

# Set a fixed window size (adjust as needed)
window_size = 800
root.geometry(f"{window_size}x{window_size}")

# Create UI elements with space between the options
question_label = tk.Label(root, text="", padx=20, pady=10)
question_label.pack()

option_buttons = []
for i in range(4):
    option_btn = tk.Button(root, text="", padx=10, pady=5, command=lambda i=i: check_answer(i))
    option_buttons.append(option_btn)
    option_btn.pack(pady=10)  # Add space between the option buttons

# Start the quiz by displaying the first question
show_question(current_question)

# Start the Tkinter main loop
root.mainloop()
