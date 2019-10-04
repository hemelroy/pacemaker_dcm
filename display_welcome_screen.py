from tkinter import *
import sqlite3
import db_operations


window = Tk()
window.geometry("800x400") #Width x Height


def view_command():
    is_full = db_operations.check_user_count()
    print(is_full)

window.wm_title("Elite Beat")

l1 = Label(window, text="Elite Beat Pacemaker Device Control Monitor", fg = "red", font = "Helvetica 16 bold italic", justify="center")
l1.grid(row=0, column=3, columnspan=6, pady=20)

## Text field
#title_text = StringVar()
#e1 = Entry(window, textvariable=title_text)
#e1.grid(row=0, column=1)



b1 = Button(window, text="Login", width=15, command=view_command)
b1.grid(row=6, column=2, columnspan=3, padx=10, pady=10)
b2 = Button(window, text="Register New User", width=15, command=view_command)
b2.grid(row=6, column=7, columnspan=3, padx=10, pady=10)

window.mainloop()