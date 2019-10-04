from tkinter import *
import sqlite3
import db_operations

def raise_frame(frame):
    frame.tkraise()

def check_register_viability():
    is_full = db_operations.check_user_count()
    
    if is_full:
        full_label = Label(intro_frame, text="Max number of users allowed to be registered has been reached.", fg="red", font="Helvetica 14", justify="center")
        full_label.grid(row=7, column=4, columnspan=4)
    else:
        raise_frame(register_frame)

def login():
    raise_frame(login_frame)

def register():
    user = register_username_field.get()
    password = register_password_field.get()

    if not user or not password:
        print("flop")
    else:
        db_operations.register_user(user, password)

window = Tk()
window.geometry("800x400") #Width x Height

intro_frame = Frame(window)
login_frame = Frame(window)
register_frame = Frame(window)

for frame in (intro_frame, login_frame, register_frame):
    frame.grid(row=0, column=0, sticky='news')

window.wm_title("Elite Beat")

#intro_frame
l1 = Label(intro_frame, text="Elite Beat Pacemaker Device Control Monitor", fg = "red", font = "Helvetica 16 bold italic", justify="center")
l1.grid(row=0, column=3, columnspan=6, pady=20)
b1 = Button(intro_frame, text="Login", width=15, command=login)
b1.grid(row=6, column=2, columnspan=3, padx=10, pady=10)
b2 = Button(intro_frame, text="Register New User", width=15, command=check_register_viability)
b2.grid(row=6, column=7, columnspan=3, padx=10, pady=10)
raise_frame(intro_frame)



#login_frame
login_title_label = Label(login_frame, text="Login", fg = "red", font = "Helvetica 16 bold italic", justify="center")
login_title_label.grid(row=0, column=3, columnspan=6, pady=20)

username_label = Label(login_frame, text="Username", font = "Helvetica 12", justify="center")
username_label.grid(row=2, column=0, columnspan=2)
login_username = StringVar()
username_field = Entry(login_frame, textvariable=login_username)
username_field.grid(row=2, column=2, columnspan=5)

password_label = Label(login_frame, text="Password", font = "Helvetica 12", justify="center")
password_label.grid(row=3, column=0, columnspan=2)
login_password = StringVar()
username_field = Entry(login_frame, textvariable=login_password)
username_field.grid(row=3, column=2, columnspan=5)

login_button = Button(login_frame, text="Login", width=15, command=login)
login_button.grid(row=4, column=2, columnspan=3, padx=10, pady=10)
login_back_button = Button(login_frame, text="Back", width=15, command=lambda:raise_frame(intro_frame))
login_back_button.grid(row=4, column=7, columnspan=3, padx=10, pady=10)


#register_frame
register_title_label = Label(register_frame, text="Login", fg = "red", font = "Helvetica 16 bold italic", justify="center")
register_title_label.grid(row=0, column=3, columnspan=6, pady=20)

register_username_label = Label(register_frame, text="Username", font = "Helvetica 12", justify="center")
register_username_label.grid(row=2, column=0, columnspan=2)
register_username = StringVar()
register_username_field = Entry(register_frame, textvariable=register_username)
register_username_field.grid(row=2, column=2, columnspan=5)

register_password_label = Label(register_frame, text="Password", font = "Helvetica 12", justify="center")
register_password_label.grid(row=3, column=0, columnspan=2)
register_password = StringVar()
register_password_field = Entry(register_frame, textvariable=register_password)
register_password_field.grid(row=3, column=2, columnspan=5)

register_button = Button(register_frame, text="Register", width=15, command=register)
register_button.grid(row=4, column=2, columnspan=3, padx=10, pady=10)
register_back_button = Button(register_frame, text="Back", width=15, command=lambda:raise_frame(intro_frame))
register_back_button.grid(row=4, column=7, columnspan=3, padx=10, pady=10)


## Text field
#title_text = StringVar()
#e1 = Entry(window, textvariable=title_text)
#e1.grid(row=0, column=1)



window.mainloop()