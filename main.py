from tkinter import *
import customtkinter
from tkinter.filedialog import askopenfile
from pypdf import PdfReader
from Model.predictionModel import predict
import os
import re
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Add to Database")
        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=10)
        
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Descriptions", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=3, column=0, padx=20, pady=10)
        
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Configuration", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=4, column=0, padx=20, pady=10)
        
        
        
        
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
        
        # I guess this it category titles
        self.right_title_category_title_housing = customtkinter.CTkLabel(self.category_date_frame, text="Housing", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_housing.grid(row=0, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_utilities = customtkinter.CTkLabel(self.category_date_frame, text="Utilites", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_utilities.grid(row=1, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_food = customtkinter.CTkLabel(self.category_date_frame, text="Food", font=customtkinter.CTkFont(size=14), compound="left", text_color="gray70", justify="left", anchor="w")
        self.right_title_category_title_food.grid(row=2, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_transportation = customtkinter.CTkLabel(self.category_date_frame, text="Transportation", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_transportation.grid(row=3, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_healthcare = customtkinter.CTkLabel(self.category_date_frame, text="Healthcare", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_healthcare.grid(row=4, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_insurance = customtkinter.CTkLabel(self.category_date_frame, text="Insurance", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_insurance.grid(row=5, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_debt = customtkinter.CTkLabel(self.category_date_frame, text="Debt Payments", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_debt.grid(row=6, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_personal = customtkinter.CTkLabel(self.category_date_frame, text="Personal Care", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_personal.grid(row=7, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_entertainment = customtkinter.CTkLabel(self.category_date_frame, text="Entertainment", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_entertainment.grid(row=8, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_savings = customtkinter.CTkLabel(self.category_date_frame, text="Savings", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_savings.grid(row=9, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        self.right_title_category_title_misc = customtkinter.CTkLabel(self.category_date_frame, text="Miscellaneous", font=customtkinter.CTkFont(size=14), text_color="gray70", compound="left", justify="left", anchor="w")
        self.right_title_category_title_misc.grid(row=10, column=0, padx=(5, 0), pady=(0, 7), sticky="nsew")
        
        #self.right_title_category_title.text_label.place(relx=0, anchor="w")
        
        # I guess this is % for categories
        self.right_title_percentages_housing = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_housing.grid(row=0, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_utilities = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_utilities.grid(row=1, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_food = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_food.grid(row=2, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_transportation = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_transportation.grid(row=3, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_healthcare = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_healthcare.grid(row=4, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_insurance = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_insurance.grid(row=5, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_debt = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_debt.grid(row=6, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_personal = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_personal.grid(row=7, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_entertainment = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_entertainment.grid(row=8, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_savings = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_savings.grid(row=9, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        self.right_title_percentages_misc = customtkinter.CTkLabel(self.category_date_frame, text="x%", font=customtkinter.CTkFont(size=14), compound="right", justify="right", anchor="e")
        self.right_title_percentages_misc.grid(row=10, column=1, padx=(20, 5), pady=(0, 7), sticky="nsew")
        
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self.title_frame, placeholder_text="N/A")
        self.entry.grid(row=4, column=0, columnspan=4, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(self.title_frame, text="Select File", command=self.open_file, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=4, column=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        
        
        
        
        # default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")




    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
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
        if hasattr(self, "file"):
            
            #print(self.fullData.index("DEBITCARDPURCHASE MCDONALD'S F736311-22LAKECITYGA0731"))
            
            entries = {x["Description"]: x["Amount"] for x in self.fullData}
            predicted_data = predict(entries)
            
            
            expense_costs = {}
            
            # Adds the total of each category and puts it into an array
            for category in predicted_data:
                category_values = predicted_data[category]
                expense_costs[category] = sum(float(value) for value in category_values.values())
                
             
            #total = sum(float(value) for value in expense_values.values())
                
            # Converting data acquired to a pie chart
            
            # Split into lists
            categories = list(expense_costs.keys())
            costs = list(expense_costs.values())
            
            # Create pie chart
            fig, ax = plt.subplots()
            ax.pie(costs, labels=categories, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            fig.patch.set_facecolor("#2B2B2B")
            self.entry.configure(placeholder_text=f'Graphing File: {os.path.basename(self.file.name)}')
            
            fig.set_figheight(3.5)
            #plt.subplots_adjust(top=0.8, bottom=0.1)
            
            canvas = FigureCanvasTkAgg(fig, self.title_frame)
            canvas.get_tk_widget().grid(row=1, column=0, columnspan=3, rowspan=3, pady=(0, 0))
        
            return 
        else:
            self.entry.configure(placeholder_text="ERROR! Please select a file before continuing.")
            return None
        

        
        
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
        self.destroy()
        
if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()