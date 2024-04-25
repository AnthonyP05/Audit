from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from pypdf import PdfReader
import os
import re

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

def open_file():
    file = askopenfile(mode='r', filetypes=[('Test files', '*.pdf')])
    if file is not None:
        pdf = PdfReader(os.path.abspath(file.name))
        print(pdf)
        for page in pdf.pages:
            text = page.extract_text()
            if "ESSENTIAL CHECKING" in text:
                start = text.find("DATEDESCRIPTION")
                end = text.find("Deposits, creditsandinterest")
                
                expenses = text[start:end]
                                
                data = split_expenses(filter_non_date_strings(expenses))
                descriptions = ""
                for expense in data:
                    descriptions += expense["Description"] + "\n"
                print(descriptions)
                




# Gui Stuf        
root = Tk()
root.geometry('500x300')        

btn = Button(root, text='Import file', command=lambda:open_file())
btn.pack(side=LEFT, pady=10, padx=30)
mainloop()