import tkinter as tk
import random
from tkinter import messagebox
import pandas as pd

# Read data from Excel sheet
df = pd.read_excel("quiz_data.xlsx", engine="openpyxl")

# Mapping of answer letters to column indices
answer_mapping = {
    'A': 0,  # Column 1 (0-based indexing)
    'B': 1,  # Column 2
    'C': 2,  # Column 3
    'D': 3,  # Column 4
}

# Extract all questions and options from the DataFrame
all_questions = []
for index, row in df.iterrows():
    question = row[0]
    options = [row[i] for i in range(1, 5)]  # Assuming options are in columns 2 to 5
    correct_answer = row[5]  # Assuming the correct answer is in the 6th column

    # Map the answer letter to the correct column index
    correct_option = answer_mapping.get(correct_answer, -1)  # Default to -1 if not found
    if correct_option == -1:
        print(f"Warning: Invalid answer '{correct_answer}' for question: {question}")
        continue

    all_questions.append({
        "question": question,
        "options": options,
        "correct_option": correct_option,
    })

# Initialize variables to keep track of the current question and score
current_question = 0
score = 0
answered = False
test_started = False  # Added to track if the test has started

# Function to start the test
def start_test():
    global current_question, score, answered, test_started
    current_question = 0
    score = 0
    answered = False
    test_started = True  # Mark the test as started
    # Shuffle the questions for the test
    random.shuffle(all_questions)
    # Hide the "Start Test" button
    start_button.pack_forget()
    # Show the option buttons
    for option_btn in option_buttons:
        option_btn.pack()
    # Show the first question
    show_question(current_question)

# Function to check the selected option and update UI
def check_answer(option_index):
    global current_question, score, answered
    if answered or current_question >= len(all_questions):
        return

    answered = True

    if option_index == all_questions[current_question]["correct_option"]:
        score += 1
        option_buttons[option_index].config(bg="green")
    else:
        option_buttons[option_index].config(bg="red")
        option_buttons[all_questions[current_question]["correct_option"]].config(bg="green")

    # After a delay, move to the next question
    root.after(1500, next_question)  # Adjust the delay time as needed (2000 milliseconds = 2 seconds)

# Function to move to the next question
def next_question():
    global current_question, answered
    current_question += 1

    if current_question < len(all_questions) and current_question < 20:
        show_question(current_question)
        answered = False
    else:
        messagebox.showinfo("Test Finished", f"Your score: {score}/{min(20, len(all_questions))}")

# Function to display the current question and options
def show_question(q_num):
    global answered  # Update the global 'answered' variable
    answered = False  # Reset the answer status

    # Clear the previous answer background color
    for option_btn in option_buttons:
        option_btn.config(bg="SystemButtonFace")

    question_label.config(text=all_questions[q_num]["question"])

    for i, option in enumerate(option_buttons):
        option_btn = option_buttons[i]
        option_btn.config(text=all_questions[q_num]["options"][i], padx=10, pady=10)  # Increased pady for more spacing

# Create the main window with a 2:1 aspect ratio
root = tk.Tk()
root.title("Randomized Quiz Test")

# Calculate the width based on the desired height and 2:1 aspect ratio
desired_height = 400  # Adjust the desired height as needed
width = int(desired_height * 2)

# Set the window size
root.geometry(f"{width}x{desired_height}")

# Set the background color of the main window
root.configure(bg="lightblue")  # Change the color as desired

# Create UI elements with space between the options
question_label = tk.Label(root, text="", padx=20, pady=10, bg="lightblue")  # Set background color
question_label.pack()

# Create option buttons but hide them initially
option_buttons = []
for i in range(4):
    option_btn = tk.Button(root, text="", padx=10, pady=10, command=lambda i=i: check_answer(i))  # Increased pady
    option_buttons.append(option_btn)
    option_btn.pack()
    option_btn.pack_forget()  # Hide the option button initially

# Button to start the test
start_button = tk.Button(root, text="Start Test", padx=10, pady=5, command=start_test)
start_button.pack()

# Start the Tkinter main loop
root.mainloop()