import tkinter as tk
import speech_recognition as sr

# Create an array to store messages and responses
messages = []


doubtfulDiseases = []
symptoms = []
non_symptoms = []
global_doubt_column = []

import pandas as pd
import numpy as np
import re

training_dataset = pd.read_csv('Testing.csv')


def create_chatbot_screen(name):
    # Create a tkinter window
    window = tk.Tk()
    window.title("Healthcare Chatbot")

    # Saving the information of columns
    cols = training_dataset.columns
    cols = cols[:-1]

    # Set the window size
    window.geometry("500x600")  # Width x Height

    # Create a speech recognizer instance
    r = sr.Recognizer()
    messages.append(("Chatbot", f"Hi {name}, How may I assist you?"))
    # Doctor
    dimensionality_reduction = training_dataset.groupby(training_dataset['prognosis']).max()

    doc_dataset = pd.read_csv('doctors_dataset.csv', names = ['Name', 'Description'])

    diseases = dimensionality_reduction.index
    diseases = pd.DataFrame(diseases)
    doctors = pd.DataFrame()
    doctors['name'] = np.nan
    doctors['link'] = np.nan
    doctors['disease'] = np.nan
    doctors['disease'] = diseases['prognosis']
    doctors['name'] = doc_dataset['Name']
    doctors['link'] = doc_dataset['Description']
    record = doctors[doctors['disease'] == 'AIDS']
    record['name']
    record['link']

    def get_symptoms_for_prognosis(prognosis):
        filtered_df = training_dataset[training_dataset['prognosis'] == prognosis]
        columns_with_1 = filtered_df.columns[filtered_df.eq(1).any()].tolist()
        return ', '.join(columns_with_1).replace('_',' ')

    # Function to handle user input
    def process_input():
        message = message_entry.get().strip()
        response = get_chatbot_response(message)
        messages.append(("User", message))
        messages.append(("Chatbot", response))
        display_messages()
        message_entry.delete(0, tk.END)

    def process_clear():
        global symptoms, non_symptoms, global_doubt_column, messages
        symptoms = []
        non_symptoms = []
        global_doubt_column = []
        messages = []
        messages.append(("Chatbot", f"Hi {name}, How may I assist you?"))
        display_messages()

    def check_matching_prognosis(symptoms, non_symptoms):
        matching_prognoses = []

        for index, row in training_dataset.iterrows():
            if all(symptom in row.index and row[symptom] == 1 for symptom in symptoms) and \
            all(non_symptom in row.index and row[non_symptom] == 0 for non_symptom in non_symptoms):
                matching_prognoses.append(row['prognosis'])

        return matching_prognoses

    def get_next_column_name(prognosis):
        for col in training_dataset.columns[:-1]:  # Exclude the 'prognosis' column
            if (training_dataset.loc[training_dataset['prognosis'] == prognosis, col] == 1).all():
                if col not in symptoms:
                    return col

    # Function to generate chatbot response based on user input
    def get_chatbot_response(message):
        if message == 'yes':
            symptoms.append(global_doubt_column[-1])
        elif message == 'no':
            non_symptoms.append(global_doubt_column[-1])
        else:
            symps = re.sub('[^\w\s]', '', message).split()
            for symp in symps:
                if symp in cols:
                    symptoms.append(symp)

        doubtfulDiseases = check_matching_prognosis(symptoms,non_symptoms)
        if len(doubtfulDiseases) == 1:
            row = doctors[doctors['disease'] == doubtfulDiseases[0]]
            pos_symps = get_symptoms_for_prognosis(doubtfulDiseases[0])
            return f"Disease : {doubtfulDiseases[0]} \nPossible Symptoms of this Disease: {pos_symps} \nDoctor : {str((row)['name'].values[0])} \nLink : {str((row)['link'].values[0])}"
        if len(doubtfulDiseases) == 0:
            return "prognosis failed"
        doubtColumn = get_next_column_name(doubtfulDiseases[0])
        global_doubt_column.append(doubtColumn)
        return f"are you suffering from {doubtColumn.replace('_',' ')}? : yes/no"

    # Function to handle voice input
    def process_voice_input():
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            recognized_speech = r.recognize_google(audio)
            message_entry.delete(0, tk.END)
            message_entry.insert(tk.END, recognized_speech)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    # Create a frame for the message display and scrollbar
    message_frame = tk.Frame(window)
    message_frame.pack(fill=tk.BOTH, expand=True)

    # Create a scrollable text widget for message display
    message_text = tk.Text(message_frame, width=60, height=15)
    message_text.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

    # Create a scrollbar for the message text widget
    scrollbar = tk.Scrollbar(message_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the scrollbar to work with the message text widget
    scrollbar.config(command=message_text.yview)
    message_text.config(yscrollcommand=scrollbar.set)

    # Function to display the messages
    def display_messages():
        message_text.config(state=tk.NORMAL)
        message_text.delete("1.0", tk.END)
        for sender, message in messages:
            if sender == "User":
                message_text.insert(tk.END, f"{message}\n", "user_tag")
            else:
                message_text.insert(tk.END, f"{message}\n", "chatbot_tag")
        message_text.see(tk.END)
        message_text.config(state=tk.DISABLED)

    # Configure tag colors and fonts
    message_text.tag_config("user_tag", background="#DCF8C6", font=("Monotype Corsiva", 15), justify=tk.RIGHT)
    message_text.tag_config("chatbot_tag", background="#D1ECF1", font=("Monotype Corsiva", 15), justify=tk.LEFT)

    # Create a label and entry field for message
    message_label = tk.Label(window, text="Message:", fg="blue", font=("Monotype Corsiva", 20, "bold"))
    message_label.pack(anchor="w")

    message_entry = tk.Entry(window, width=80)
    message_entry.pack(anchor="w")
    message_entry.bind("<Return>", lambda event: button.invoke())  # Bind Enter key to button click

    # Create a button for voice input
    voice_button = tk.Button(window, text="Speak", command=process_voice_input, bg="orange", fg="white",
                            font=("Monotype Corsiva", 12, "bold"))
    voice_button.pack(side=tk.LEFT, padx=(5, 0), anchor="w")

    # Create a button to process the input
    button = tk.Button(window, text="Send", command=process_input, bg="green", fg="white", font=("Monotype Corsiva", 12, "bold"))
    button.pack(side=tk.LEFT, padx=(5, 0), anchor="w")

    clear_button = tk.Button(window, text="Clear", command=process_clear, bg="white", fg="blue", font=("Monotype Corsiva", 12, "bold"))
    clear_button.pack(side=tk.LEFT, padx=(5, 0), anchor="w")
    display_messages()

    # Run the tkinter event loop
    window.mainloop()
    return window
