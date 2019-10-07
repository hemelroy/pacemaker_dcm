from tkinter import *
from PIL import ImageTk, Image
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
    #raise_frame(login_frame)
    user = username_field.get()
    password = password_field.get()

    if not user and not password:
        print("Missing fields")
    else:
        db_operations.login_user(user, password)

    #call db function to check if user exists

    #if user exists, log them in and pull up their attributes

    #if not, display error message

def to_login():
    raise_frame(login_frame)

def register():
    user = register_username_field.get()
    password = register_password_field.get()

    if not user or not password:
        print("flop")
    else:
        userid = db_operations.register_user(user, password)
        db_operations.add_attributes(userid, 50, 50, )
        raise_frame(params_frame)        



window = Tk()
window.geometry("800x400") #Width x Height

intro_frame = Frame(window, bg="red")
login_frame = Frame(window)
register_frame = Frame(window)
params_frame = Frame(window)

for frame in (intro_frame, login_frame, register_frame, params_frame):
    frame.grid(row=0, column=0, sticky='news')

window.wm_title("Elite Beat")
window.configure(background='black')


#intro_frame
intro_title_label = Label(intro_frame, text="Elite Beat Pacemaker Device Control Monitor", fg = "red", bg="black", font = "Helvetica 16 bold italic", justify="center", padx=170, pady=100)
intro_title_label.grid(row=0, column=3, columnspan=6, pady=20)
intro_login_button = Button(intro_frame, text="Login", width=15, command=lambda:raise_frame(login_frame))
intro_login_button.grid(row=6, column=2, columnspan=3, padx=10, pady=10)
intro_register_button = Button(intro_frame, text="Register New User", width=15, command=check_register_viability)
intro_register_button.grid(row=6, column=6, columnspan=3, padx=10, pady=10)

raise_frame(intro_frame)



#login_frame
login_title_label = Label(login_frame, text="Login", fg = "red", font = "Helvetica 16 bold italic", justify="center")
login_title_label.grid(row=0, column=3, columnspan=9)

username_label = Label(login_frame, text="Username", font = "Helvetica 12", justify="center")
username_label.grid(row=2, column=0, columnspan=2)
login_username = StringVar()
username_field = Entry(login_frame, textvariable=login_username)
username_field.grid(row=2, column=2, columnspan=8)

password_label = Label(login_frame, text="Password", font = "Helvetica 12", justify="center")
password_label.grid(row=3, column=0, columnspan=2)
login_password = StringVar()
password_field = Entry(login_frame, textvariable=login_password, show="*")
password_field.grid(row=3, column=2, columnspan=8)

login_button = Button(login_frame, text="Login", width=15, command=login)
login_button.grid(row=4, column=2, columnspan=3, padx=10, pady=10)
login_back_button = Button(login_frame, text="Back", width=15, command=lambda:raise_frame(intro_frame))
login_back_button.grid(row=4, column=7, columnspan=3, padx=10, pady=10)


#register_frame
register_title_label = Label(register_frame, text="Register New User", fg = "red", font = "Helvetica 16 bold italic", justify="center")
register_title_label.grid(row=0, column=3, columnspan=8, pady=20)

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


#params_frame
params_title_label = Label(params_frame, text="Programmable Parameters", fg = "red", font = "Helvetica 16 bold italic", justify="center")
params_title_label.grid(row=0, column=3, columnspan=6, pady=20)

default = StringVar(params_frame)
default.set("VOO") # default value
pacingModeOption = OptionMenu(params_frame, default, "VOO", "AOO", "AAI", "VVI")
pacingModeOption.grid(row=1, column=2, columnspan=5)
# pacingMode_label = Label(params_frame, text="Username", font = "Helvetica 12", justify="center")
# pacingMode_label.grid(row=2, column=0, columnspan=2)
# pacingMode = StringVar()
# pacingMode_field = Entry(params_frame, textvariable=pacingMode)
# pacingMode_field.grid(row=2, column=2, columnspan=5)

lowRateInterval_label = Label(params_frame, text="Lower Rate Limit", font = "Helvetica 12", justify="center")
lowRateInterval_label.grid(row=3, column=0, columnspan=2)
lowRateInterval = StringVar()
lowRateInterval_field = Entry(params_frame, textvariable=lowRateInterval)
lowRateInterval_field.grid(row=3, column=2, columnspan=5)

uppRateInterval_label = Label(params_frame, text="Upper Rate Limit", font = "Helvetica 12", justify="center")
uppRateInterval_label.grid(row=4, column=0, columnspan=2)
uppRateInterval = StringVar()
uppRateInterval_field = Entry(params_frame, textvariable=uppRateInterval)
uppRateInterval_field.grid(row=4, column=2, columnspan=5)

vPaceAmp_label = Label(params_frame, text="Ventricular Amplitude", font = "Helvetica 12", justify="center")
vPaceAmp_label.grid(row=5, column=0, columnspan=2)
vPaceAmp = StringVar()
vPaceAmp_field = Entry(params_frame, textvariable=vPaceAmp)
vPaceAmp_field.grid(row=5, column=2, columnspan=5)

vPulseWidth_label = Label(params_frame, text="Ventricular Pulse Width", font = "Helvetica 12", justify="center")
vPulseWidth_label.grid(row=6, column=0, columnspan=2)
vPulseWidth = StringVar()
vPulseWidth_field = Entry(params_frame, textvariable=vPulseWidth)
vPulseWidth_field.grid(row=6, column=2, columnspan=5)

aPaceAmp_label = Label(params_frame, text="Atrial Amplitude", font = "Helvetica 12", justify="center")
aPaceAmp_label.grid(row=7, column=0, columnspan=2)
aPaceAmp = StringVar()
aPaceAmp_field = Entry(params_frame, textvariable=aPaceAmp)
aPaceAmp_field.grid(row=7, column=2, columnspan=5)

aPulseWidth_label = Label(params_frame, text="Atrial Pulse Width", font = "Helvetica 12", justify="center")
aPulseWidth_label.grid(row=8, column=0, columnspan=2)
aPulseWidth = StringVar()
aPulseWidth_field = Entry(params_frame, textvariable=aPulseWidth)
aPulseWidth_field.grid(row=8, column=2, columnspan=5)

update_button = Button(params_frame, text="Update", width=15, command=register)
update_button.grid(row=9, column=2, columnspan=3, padx=10, pady=10)
params_back_button = Button(params_frame, text="Back", width=15, command=lambda:raise_frame(login_frame))
params_back_button.grid(row=9, column=7, columnspan=3, padx=10, pady=10)


window.mainloop()