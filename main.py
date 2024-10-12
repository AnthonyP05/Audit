from tkinter import *
import customtkinter
from tkinter.filedialog import askopenfile
from pypdf import PdfReader
from Model.predictionModel import predict
import os
import re
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prompt import Prompt  # Import Prompt class and the flag
from data import Data
from Model.predictionModel import load

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        
        # config window (was x580)
        self.title("Expense Eval")
        self.geometry(f'{1100}x{580}')
        
        # config grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        
        
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1, uniform="Silent_Creme")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Expense", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.sidebar_button_0 = customtkinter.CTkButton(self.sidebar_frame, text="Graph File", command=self.data_to_graph)
        self.sidebar_button_0.grid(row=1, column=0, padx=20, pady=10)
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Add to Database", command=self.add_to_database)
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Descriptions", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Configuration", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Categorize Entries", command=self.categorize)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        
        
        
        # sidebar frame appearance settings
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=8, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=9, column=0, padx=20, pady=(10, 20))
        
        
        # create title frame and label
        self.title_frame = customtkinter.CTkFrame(self, width=900)
        self.title_frame.grid(row=0, column=1, rowspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        # config grid layout (4x4)
        self.title_frame.grid_columnconfigure(list(range(4)), weight=1, uniform="Silent_Creme")
        self.title_frame.grid_rowconfigure(list(range(4)), weight=1, uniform="Silent_Creme")
        
        # create additional sub frames within parent title frame
        self.sub_title_frame = customtkinter.CTkFrame(self.title_frame)
        self.sub_title_frame.grid(row=0, column=0, columnspan=4, padx=(20,0), pady=(20, 50), sticky="nsew")
        
        self.title_label = customtkinter.CTkLabel(self.sub_title_frame, text="No File Selected", font=customtkinter.CTkFont(size=15, weight="bold"), text_color="gray30")
        self.title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=(10, 10))
        
        
        self.right_title_frame = customtkinter.CTkFrame(self.title_frame)
        self.right_title_frame.grid(row=0, rowspan=4, column=4, padx=(20,20), pady=(20,20), sticky="nsew")

        
        self.right_title_label = customtkinter.CTkLabel(self.right_title_frame, text='CATEGORIES', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.right_title_label.grid(row=0, column=0, padx=10, pady=(8, 10), sticky="nsew")
        
        
        self.category_date_frame = customtkinter.CTkFrame(self.right_title_frame, fg_color="transparent")
        self.category_date_frame.grid(row=1, column=0, rowspan=4)
        
        # Padding for Category labels' titles within the Category frame
        category_padding_x = (5, 0)
        category_padding_y = (0, 4)
        
        # Category labels' titles within the Category frame
        self.right_title_category_title_housing = customtkinter.CTkLabel(self.category_date_frame, text="Housing", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_housing.grid(row=0, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_utilities = customtkinter.CTkLabel(self.category_date_frame, text="Utilities", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_utilities.grid(row=1, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_food = customtkinter.CTkLabel(self.category_date_frame, text="Food", font=customtkinter.CTkFont(size=14), compound="left", text_color="gray70", justify="left", anchor="w")
        self.right_title_category_title_food.grid(row=2, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_transportation = customtkinter.CTkLabel(self.category_date_frame, text="Transportation", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_transportation.grid(row=3, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_healthcare = customtkinter.CTkLabel(self.category_date_frame, text="Healthcare", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_healthcare.grid(row=4, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_insurance = customtkinter.CTkLabel(self.category_date_frame, text="Insurance", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_insurance.grid(row=5, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_debt = customtkinter.CTkLabel(self.category_date_frame, text="Debt Payments", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_debt.grid(row=6, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_personal = customtkinter.CTkLabel(self.category_date_frame, text="Personal Care", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_personal.grid(row=7, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_entertainment = customtkinter.CTkLabel(self.category_date_frame, text="Entertainment", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_entertainment.grid(row=8, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_savings = customtkinter.CTkLabel(self.category_date_frame, text="Savings", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_savings.grid(row=9, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        self.right_title_category_title_misc = customtkinter.CTkLabel(self.category_date_frame, text="Miscellaneous", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_misc.grid(row=10, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        
        self.right_title_category_title_total = customtkinter.CTkLabel(self.category_date_frame, text="Total Spent:", font=customtkinter.CTkFont(size=14), text_color="gray40", compound="left", justify="left", anchor="w")
        self.right_title_category_title_total.grid(row=11, column=0, padx=category_padding_x, pady=category_padding_y, sticky="nsew")
        
        # Padding for Category labels' percentages within the Category frame
        percentages_padding_x = (20, 5)
        percentages_padding_y = (0, 4)
        
        # Category labels' expense within the Category frame
        self.right_title_expense_housing = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_housing.grid(row=0, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_utilities = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_utilities.grid(row=1, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_food = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_food.grid(row=2, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_transportation = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_transportation.grid(row=3, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_healthcare = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_healthcare.grid(row=4, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_insurance = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_insurance.grid(row=5, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_debt = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_debt.grid(row=6, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_personal = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_personal.grid(row=7, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_entertainment = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_entertainment.grid(row=8, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_savings = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_savings.grid(row=9, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        self.right_title_expense_misc = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="right", justify="right", anchor="e")
        self.right_title_expense_misc.grid(row=10, column=1, padx=percentages_padding_x, pady=percentages_padding_y, sticky="nsew")
        
        # Category total label within the Category frame
        self.right_title_percentages_total = customtkinter.CTkLabel(self.category_date_frame, text="$0", font=customtkinter.CTkFont(size=14), text_color="gray40", compound="right", justify="right", anchor="e")
        self.right_title_percentages_total.grid(row=11, column=1, padx=percentages_padding_x, pady=(0, 7), sticky="nsew")
        
        # Information output entry
        self.entry = customtkinter.CTkEntry(self.title_frame, placeholder_text="N/A")
        self.entry.grid(row=4, column=0, columnspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew")

        # File selection button
        self.main_button_1 = customtkinter.CTkButton(self.title_frame, text="Select File", command=self.open_file, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=4, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        # default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")
        self.toplevel_window = None

        # config colors
        if customtkinter.get_appearance_mode() == "Light":
            self.right_title_label.configure(text_color="#575757")
            self.logo_label.configure(text_color="#575757")
        elif customtkinter.get_appearance_mode() == "Dark":
            self.right_title_label.configure(text_color="#DBDBDB")
            self.logo_label.configure(text_color="#DBDBDB")


    # Changes the color appearance of the application and pie chart (if applicable)
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
        if customtkinter.get_appearance_mode() == "Light":
            if hasattr(self, "ax"):
                for text in self.ax.texts: text.set_color("#575757")
                self.fig.patch.set_facecolor("#DBDBDB")
                self.fig.canvas.draw()
            self.right_title_label.configure(text_color="#575757")
            self.logo_label.configure(text_color="#575757")
            
        elif customtkinter.get_appearance_mode() == "Dark":
            if hasattr(self, "ax"):
                for text in self.ax.texts: text.set_color("#DBDBDB")
                self.fig.patch.set_facecolor("#2B2B2B")
                self.fig.canvas.draw()
            self.right_title_label.configure(text_color="#DBDBDB")
            self.logo_label.configure(text_color="#DBDBDB")
            
            
    # Changes the scaling of the application to desired choice
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    # Selects a desired file. 
    # TODO: Make it possible to catch a user trying to open a file that isn't a truist bank statement.
    def open_file(self):
        self.file = askopenfile(mode='r', filetypes=[('Test files', '*.pdf')])
        if self.file is not None:        
            
            reader = PdfReader(os.path.abspath(self.file.name))
            
            for page in reader.pages:
                text = page.extract_text()
                if "ESSENTIAL CHECKING" in text:
                    start = text.find("DATEDESCRIPTION")
                    end = text.find("Deposits, creditsandinterest")
                    
                    expenses = text[start:end]
                     
                    self.data = self.split_expenses_descriptions(self.filter_non_date_strings(expenses))
                    self.fullData = self.split_expenses(self.filter_non_date_strings(expenses))
                    # When file is selected, display file name in application
                    self.title_label.configure(text=f'Selected File: {os.path.basename(self.file.name)}', text_color="gray70")
    
    # Returns a dictionary with payment entries seperated into different categories
    def data_to_graph(self):
        # if self.file exists, or if a file has been chosen...
        if hasattr(self, "file"):
            entries = {x["Description"]: x["Amount"] for x in self.fullData}
            predicted_data = predict(entries)
            expense_costs = {}
            
            
            # Adds the total of each category and puts it into an array
            for category in predicted_data:
                category_values = predicted_data[category]
                expense_costs[category] = round(sum(float(value.replace(",", "")) for value in category_values.values()), 2)
             
            total = round(sum(float(value) for value in expense_costs.values()), 2)
                
            # Converting data acquired to a pie chart
            
            # Split into lists
            categories = list(expense_costs.keys())
            costs = list(expense_costs.values())
            
            # Create pie chart
            self.fig, self.ax = plt.subplots()
            self.ax.pie(costs, labels=categories, autopct='%1.1f%%', startangle=90)
            self.ax.axis('equal')
            self.entry.configure(placeholder_text=f'Graphing File: {os.path.basename(self.file.name)}')
            self.fig.set_figheight(3.5)
            
            self.canvas = FigureCanvasTkAgg(self.fig, self.title_frame)
            self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, rowspan=3, pady=(0, 0))
            
            # Changes the color of the pie chart according to the system color
            if customtkinter.get_appearance_mode() == "Light":
                for text in self.ax.texts: text.set_color("#575757")
                self.fig.patch.set_facecolor("#DBDBDB")
            elif customtkinter.get_appearance_mode() == "Dark":
                for text in self.ax.texts: text.set_color("#DBDBDB")
                self.fig.patch.set_facecolor("#2B2B2B")
                
            self.fig.canvas.draw()
            
            self.right_title_percentages_total.configure(text=f'${total}')
            
            # Changes each label expense in the Category frame to its appropriate expense amount if applicable
            try:
                self.right_title_expense_housing.configure(text=f'${expense_costs["HOUSING"]}') if "HOUSING" in expense_costs else self.right_title_expense_housing.configure(text=f'$0')
                self.right_title_expense_utilities.configure(text=f'${expense_costs["UTILITIES"]}') if "UTILITIES" in expense_costs else self.right_title_expense_utilities.configure(text=f'$0')
                self.right_title_expense_food.configure(text=f'${expense_costs["FOOD"]}') if "FOOD" in expense_costs else self.right_title_expense_food.configure(text=f'$0')
                self.right_title_expense_transportation.configure(text=f'${expense_costs["TRANSPORTATION"]}') if "TRANSPORTATION" in expense_costs else self.right_title_expense_transportation.configure(text=f'$0')
                self.right_title_expense_healthcare.configure(text=f'${expense_costs["HEALTHCARE"]}') if "HEALTHCARE" in expense_costs else self.right_title_expense_healthcare.configure(text=f'$0')
                self.right_title_expense_insurance.configure(text=f'${expense_costs["INSURANCE"]}') if "INSURANCE" in expense_costs else self.right_title_expense_insurance.configure(text=f'$0')
                self.right_title_expense_debt.configure(text=f'${expense_costs["DEBT"]}') if "DEBT" in expense_costs else self.right_title_expense_debt.configure(text=f'$0')
                self.right_title_expense_personal.configure(text=f'${expense_costs["PERSONAL"]}') if "PERSONAL" in expense_costs else self.right_title_expense_personal.configure(text=f'$0')
                self.right_title_expense_entertainment.configure(text=f'${expense_costs["ENTERTAINMENT"]}') if "ENTERTAINMENT" in expense_costs else self.right_title_expense_entertainment.configure(text=f'$0')
                self.right_title_expense_savings.configure(text=f'${expense_costs["SAVINGS"]}') if "SAVINGS" in expense_costs else self.right_title_expense_savings.configure(text=f'$0')
                self.right_title_expense_misc.configure(text=f'${expense_costs["MISCELLANEOUS"]}') if "MISCELLANEOUS" in expense_costs else self.right_title_expense_misc.configure(text=f'$0')
            except SyntaxError as e:
                print(e)
                pass
            return 
        else:
            self.entry.configure(placeholder_text="ERROR! Please select a file before continuing.")
            return None
    
    
    # Opens a new window and Asks the user what item belongs to what category
    def add_to_database(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = ToplevelWindow(self)  # create window if its None or destroyed
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()  # if window exists focus it
            
    def categorize(self):
        data = Data()
        data.mainloop()
        
    # Filter things that aren't the date
    def filter_non_date_strings(self, text):
        # Split the text into lines and filter out lines that don't start with MM/DD
        lines = text.split('\n')
        filtered_lines = [line for line in lines if re.match(r'\b\d{1,2}/\d{1,2}', line)]
        return '\n'.join(filtered_lines)

    # Split expenses into different categories for easier organization
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
    
    def split_expenses_descriptions(self, text):
        lines = text.split('\n')
        expenses = []
        for line in lines:
            data = line.split(" ")
            description = ' '.join(data[1:-1])
            expenses.append(description)
        return expenses
    
    def on_closing(self):
        plt.close('all')
        self.after(50, self.destroy)
        
        
class ToplevelWindow(customtkinter.CTkToplevel):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.app = app
        self.title("Expense Eval | Database Insertion")
        self.label = customtkinter.CTkLabel(self, text=f'{self.app.title}')
        self.label.pack(padx=20, pady=20)


if __name__ == "__main__":
    file = os.path.exists("items.json")
    if not file:
        prompt = Prompt()
        prompt.protocol("WM_DELETE_WINDOW", prompt.on_closing)
        prompt.mainloop()    
    
    if file or prompt.get_result():
        try:
            load()
            app = App()
            app.protocol("WM_DELETE_WINDOW", app.on_closing)
            app.mainloop()
        except Exception as e:
            print(f"Ignored error: {e}")