from tkinter import *
from tkinter.ttk import *
from pypdf import PdfReader
import os
import re
import json

"""

Reads a Truist Bank Statement and sends the expenses provided into items.json

"""

# importing askopenfile from class filedialog
from tkinter.filedialog import askopenfile

def filter_non_date_strings(text):
    # Split the text into lines and filter out lines that don't start with MM/DD
    lines = text.split('\n')
    filtered_lines = [line for line in lines if re.match(r'\b\d{1,2}/\d{1,2}', line)]
    return '\n'.join(filtered_lines)

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

def open_file(window):
    file = askopenfile(mode='r', filetypes=[('Test files', '*.pdf')])
    if file is not None:
        pdf = PdfReader(os.path.abspath(file.name))
        for page in pdf.pages:
            text = page.extract_text()
            if "ESSENTIAL CHECKING" in text:
                start = text.find("DATEDESCRIPTION")
                end = text.find("Deposits, creditsandinterest")
                
                expenses = text[start:end]
                                
                data = split_expenses(filter_non_date_strings(expenses))
                print(data)
                items = []
                for expense in data:
                    description = expense["Description"]
                    amount = expense["Amount"]
                    date = expense["Date"]
                    category = ""
                    items.append({"description" : description, "category": category, "date": date, "amount": amount})
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

                # Add new items to existing items if they are not already present
                for new_item in items:
                    if new_item["description"] not in descriptions:                        
                        existing_items.append(new_item)
                        label = Label(window, text="Added to database.")
                    else:
                        label = Label(window, text="Already in database.")
                        
                #label.pack()
            
                # Write updated data back to the JSON file
                with open(file_path, 'w') as f:
                    json.dump(existing_items, f, indent=4)
                
                
        
root = Tk()
root.geometry('500x300')        

btn = Button(root, text='Import file', command=lambda:open_file(root))
btn.pack()
mainloop()