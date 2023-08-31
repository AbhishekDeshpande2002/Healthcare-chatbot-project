import tkinter as tk
from chatbot import create_chatbot_screen

# Create a tkinter input_screen
input_screen = tk.Tk()
input_screen.title("Healthcare Chatbot")
input_screen.geometry("500x600")  # Width x Height

# Create labels and entry fields for name and age
name_label = tk.Label(input_screen, text="Name:", fg="blue", font=("Monotype Corsiva", 20, "bold"))
name_label.pack(anchor="w")

name_entry = tk.Entry(input_screen, width=80)
name_entry.pack(anchor="w")

age_label = tk.Label(input_screen, text="Age:", fg="blue", font=("Monotype Corsiva", 20, "bold"))
age_label.pack(anchor="w")

age_entry = tk.Entry(input_screen, width=80)
age_entry.pack(anchor="w")

# Function to proceed to the chatbot screen
def proceed_to_chatbot():
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    if name and age:
        # Hide the input screen
        input_screen.destroy()

        # Create the chatbot screen
        chatbot_screen = create_chatbot_screen(name)
        chatbot_screen.mainloop()

# Create a button to proceed to the chatbot screen
proceed_button = tk.Button(input_screen, text="Proceed", command=proceed_to_chatbot, bg="green", fg="white",
                           font=("Monotype Corsiva", 12, "bold"))
proceed_button.pack(anchor="w")

# Run the tkinter event loop
input_screen.mainloop()
