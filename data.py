from tkinter import TclError
import customtkinter
import json
import os

# File path for items.json
JSON_FILE_PATH = "items.json"

class Data(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.id = None
        
        # Track the items and their categories
        self.items = []
        self.categories = ["HOUSING", "UTILITIES", "FOOD", "TRANSPORTATION", "HEALTHCARE", "INSURANCE", "DEBT", "PERSONAL", "ENTERTAINMENT", "SAVINGS", "MISCELLANEOUS"]  # Add more categories as needed

        # Load items from items.json
        self.load_items()

        # Configure window
        self.title("Categorize Items")
        self.geometry(f'{900}x{500}')

        # Create a label
        label = customtkinter.CTkLabel(self, text="Categorize Your Expenses")
        label.pack(pady=10)

        # Create a scrollable frame to hold the items
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, width=380, height=200)
        self.scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Create an entry for each item
        self.entries = {}  # Dictionary to store selected categories
        for item in self.items:
            if item['category'] == '':  # Check if the category is empty
                self.create_item_entry(item)

        # Add a button to save changes
        submit_button = customtkinter.CTkButton(self, text="Submit", command=self.button_scheduling)
        submit_button.pack(pady=10)
                        
    def button_scheduling(self):
        self.after(100, self.save_items)
                
    def load_items(self):
        """Load items from the JSON file."""
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, 'r') as file:
                self.items = json.load(file)
        return

    def create_item_entry(self, item):
        """Create an entry for each item to specify the category."""
        frame = customtkinter.CTkFrame(self.scrollable_frame)
        frame.pack(pady=5, fill="x")

        # Use grid to align description and dropdown in separate columns
        description_label = customtkinter.CTkLabel(frame, text=item['description'], anchor="w")
        description_label.grid(row=0, column=0, padx=(10, 5), sticky="w")

        # Create a dropdown (combobox) for selecting categories
        category_dropdown = customtkinter.CTkOptionMenu(frame, values=self.categories)
        category_dropdown.set(item['category'] if item['category'] else "Select Category")  # Set default category
        category_dropdown.grid(row=0, column=1, padx=5, sticky="e")

        # Configure grid column weight to center items
        frame.columnconfigure(0, weight=1)  # Make the description column expand
        frame.columnconfigure(1, weight=1)  # Make the category dropdown column expand

        # Store the selected category in the entries dictionary
        self.entries[item['description']] = category_dropdown
        
        return

    def category_selected(self, value):
        """Callback for when a category is selected."""
        print(f"Selected category: {value}")  # Optional: for debugging
        return

    def save_items(self):
        """Save the updated items with their categories back to the JSON file."""
        for description, dropdown in self.entries.items():
            # Update the category in items
            for item in self.items:
                if item['description'] == description:
                    if dropdown.get() == "Select Category":
                        item['category'] = ''
                    else:
                        item['category'] = dropdown.get() # Get the selected category from the dropdown

        # Write the updated items back to the JSON file
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(self.items, file, indent=4)

        #self.id = self.after(100000, self.save_items)
        #self.id = self.after(100, self.on_closing())
        self.on_closing()
        
    
    def on_closing(self):
        try:
            if self.id:
                print("Cancelling")
                self.after_cancel(self.id)
                self.id = None
            self.quit()
            self.destroy()
        except TclError as e:
            print(f'Error occurred while closing: {e}')