from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from pypdf import PdfReader
import json
import os
import re
    
def open_file():
    file = askopenfile(mode='r', filetypes=[('Test files', '*.pdf')])
    if file is not None:        
        
        reader = PdfReader(os.path.abspath(file.name))
        
        for page in reader.pages:
            text = page.extract_text()
            if "ESSENTIAL CHECKING" in text:
                start = text.find("DATEDESCRIPTION")
                end = text.find("Deposits, creditsandinterest")
                
                expenses = text[start:end]
                
                global data 
                data = split_expenses(filter_non_date_strings(expenses))
                print(data)
                
                counter = 1
                
                for expense in data:
                    #listbox.insert(counter, expense["Description"])
                    counter += 1
                #frame.config(justify='left', text=f'{descriptions}')
                #print(descriptions)
        
    
    else:
        print("File has no content.")

# Clicked selection in list
def on_click(event):
    global clicked_item
    clicked_item = None
    
    # Get the index of the clicked item
    index = listbox.curselection()
    if index:
        # Get the text of the clicked item
        clicked_item = listbox.get(index[0])
        print("Clicked item:", clicked_item)


def is_in_database():
    in_database = False
    items = []
    for expense in data:
        description = expense["Description"]
        items.append(description)
    # Save data to JSON file
    file_path = 'items.json'
    if os.path.exists(file_path):
        # Read existing JSON file
        with open(file_path, 'r') as f:
            existing_items = json.load(f)
        descriptions = [d["description"] for d in existing_items]
    else:
        # Create an empty list if the file doesn't exist
        descriptions = []
        existing_items = []

    for new_item in items:
        if new_item["description"] not in descriptions:                        
            existing_items.append(new_item)
            in_database = False
        else:
            in_database = True

    return in_database
    
# Filter things that aren't the date
def filter_non_date_strings(text):
    # Split the text into lines and filter out lines that don't start with MM/DD
    lines = text.split('\n')
    filtered_lines = [line for line in lines if re.match(r'\b\d{1,2}/\d{1,2}', line)]
    return '\n'.join(filtered_lines)

# Split expenses into different categories for easier organization
def split_expenses(text):
    lines = text.split('\n')
    expenses = []
    for line in lines:
        data = line.split(" ")
        date = data[0]
        description = ' '.join(data[1:-1])
        amount = data[-1]
        expenses.append({"Date": date, "Description": description, "Amount": amount})
    return expenses   

