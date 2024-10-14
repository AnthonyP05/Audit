import customtkinter
from tkinter import *
from tkinter.ttk import *
from pypdf import PdfReader
import os
import re
import json
from tkinter.filedialog import askopenfile


# Initial dialog window for file selection
class Prompt(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Track if prompt was closed with a positive result
        self.result = False
        self.file = None
        
        # Configure window
        self.title("Select Data File")
        self.geometry(f'{400}x{200}')

        # Add some UI elements, such as buttons for file selection
        label = customtkinter.CTkLabel(self, text="FIRST:")
        label.pack(pady=20)

        select_button = customtkinter.CTkButton(self, text="Select Data File or Statement File", command=self.select_file)
        select_button.pack(pady=10)
                
    def filter_non_date_strings(self, text):
        # Split the text into lines and filter out lines that don't start with MM/DD
        lines = text.split('\n')
        filtered_lines = [line for line in lines if re.match(r'\b\d{1,2}/\d{1,2}', line)]
        
        return '\n'.join(filtered_lines)

    def split_expenses(self, text):
        lines = text.split('\n')
        
        expenses = []
        for line in lines:
            data = line.split(" ")
            date = data[0]
            description = ' '.join(data[1:-1])
            amount = data[-1]
            expenses.append({"Date": date, "Description": description, "Amount": amount})
        return expenses   


    def select_file(self):
        # Code for handling when the user doesn't have a data file
        self.result = True
        
        file = askopenfile(mode='r', filetypes=[('Test files', '*.pdf')])
        if file is not None:
            
            if file.name == "items.json":
                self.file = file.name
                self.on_closing()
                return
            
            self.record_file(file)        
    
    def record_file(self, file):
        pdf = PdfReader(os.path.abspath(file.name))
        for page in pdf.pages:
            text = page.extract_text()
            if "ESSENTIAL CHECKING" in text:
                start = text.find("DATEDESCRIPTION")
                end = text.find("Deposits, creditsandinterest")
                if (end == -1): end = text.find("continued")
                expenses = text[start:end]
                data = self.split_expenses(self.filter_non_date_strings(expenses))
                #print(data)
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
                        
            
                # Write updated data back to the JSON file
                with open(file_path, 'w') as f:
                    json.dump(existing_items, f, indent=4)
                    
                self.file = file_path
        
        self.on_closing()
                
    def content_to_JSON(self, file):
        pdf = PdfReader(os.path.abspath(file.name))
        for page in pdf.pages:
            text = page.extract_text()
            if "ESSENTIAL CHECKING" in text:
                start = text.find("DATEDESCRIPTION")
                end = text.find("Deposits, creditsandinterest")
                if (end == -1): end = text.find("continued")
                expenses = text[start:end]
                data = self.split_expenses(self.filter_non_date_strings(expenses))
                #print(data)
                items = []
                for expense in data:
                    description = expense["Description"]
                    amount = expense["Amount"]
                    date = expense["Date"]
                    category = ""
                    items.append({"description" : description, "category": category, "date": date, "amount": amount})
                return items
        return
                
    def on_closing(self):
        self.quit()
        return
        
    def get_file(self):
        return self.file    
    
    def get_result(self):
        return self.result
        
    