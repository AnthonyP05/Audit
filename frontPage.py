'''Example of how to use the grid() method to create a GUI layout'''
from tkinter import *
from methods import open_file

root  =  Tk()  # create root window
root.title("Financial Audit")
root.maxsize(900,  600)  # width x height
root.geometry("900x600")
root.config(bg="skyblue")

# Create left and right frames
left_frame  =  Frame(root,  width=200,  height=  400,  bg='grey')
left_frame.grid(row=0,  column=0,  padx=10,  pady=5)

right_frame  =  Frame(root,  width=600,  height=400,  bg='grey')
right_frame.grid(row=0,  column=1,  padx=10,  pady=5)
right_frame.grid_propagate(False)

# Create frames and labels in left_frame
Label(left_frame,  text="Financial Audit",  relief=RAISED).grid(row=0,  column=0,  padx=5,  pady=5)

image = PhotoImage(file="./images/SPBank.gif")
original_image  =  image.subsample(3,3)

Label(left_frame,  image=original_image).grid(row=1,  column=0,  padx=5,  pady=5)

title = Label(right_frame, text="File Selected: N/A", bg='gray', font=('Times New Roman', 15))
title.grid(row=0, column=0, padx=5, pady=5)
title.place(x=300, y=25, anchor='center')


tool_bar  =  Frame(left_frame,  width=180,  height=185,  bg='grey')
tool_bar.grid(row=2,  column=0,  padx=5,  pady=5)

def clicked():
    '''if button is clicked, display message'''
    print("Clicked.")


# Example labels that serve as placeholders for other widgets
Label(tool_bar,  text="Options",  relief=RAISED).grid(row=0,  column=0,  padx=5,  pady=3,  ipadx=10)
Label(tool_bar,  text="N/A",  relief=RAISED).grid(row=0,  column=1,  padx=5,  pady=3,  ipadx=10)

# For now, when the buttons are clicked, they only call the clicked() method. We will add functionality later.
Button(tool_bar,  text="Select File",  command=lambda:(open_file(title, right_frame))).grid(row=1,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')


Button(tool_bar,  text="Add to Database",  command=clicked).grid(row=2,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
Button(tool_bar,  text="Predict Entries",  command=clicked).grid(row=3,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
Button(tool_bar,  text="Resize",  command=clicked).grid(row=4,  column=0,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')
Button(tool_bar,  text="Check if file selected").grid(row=1,  column=1,  padx=5,  pady=5,  sticky='w'+'e'+'n'+'s')

root.mainloop()