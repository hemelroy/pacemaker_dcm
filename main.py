from tkinter import *
from PIL import ImageTk, Image
import sqlite3
import db_operations

user_id = -1

def raise_frame(frame):
    frame.tkraise()

def check_register_viability():
    is_full = db_operations.check_user_count()
    
    if is_full:
        full_label.grid(row=8, column=3, columnspan=8)
    else:
        raise_frame(register_frame)

def login():
    #raise_frame(login_frame)
    user = username_field.get()
    password = password_field.get()

    if not user and not password:
        print("Missing fields")
    else:
        global user_id
        user_id, params = db_operations.login_user(user, password)

        if params:
            uppRateInterval_field
            lowRateInterval_field.delete(0, END) #deletes the current value
            lowRateInterval_field.insert(0, params[1])
            uppRateInterval_field.delete(0, END)
            uppRateInterval_field.insert(0, params[2])
            vPaceAmp_field.delete(0, END)
            vPaceAmp_field.insert(0, params[3])
            vPulseWidth_field.delete(0, END)
            vPulseWidth_field.insert(0, params[4])
            aPaceAmp_field.delete(0, END)
            aPaceAmp_field.insert(0, params[5])
            aPulseWidth_field.delete(0, END)
            aPulseWidth_field.insert(0, params[6])
            raise_frame(params_frame)
        else:
            #unidentified_user_label.grid(row=9, column=5, columnspan=12)
            unidentified_user_label.place(relx=0.5, rely=0.8, anchor=CENTER)

    #call db function to check if user exists

    #if user exists, log them in and pull up their attributes

    #if not, display error message

def to_login():
    raise_frame(login_frame)

def register():
    user = register_username_field.get()
    password = register_password_field.get()

    if not user or not password:
        register_missingfield_label.place(relx=0.5, rely=0.8, anchor=CENTER)
    else:
        global user_id
        is_new_user = False
        is_new_user = db_operations.check_if_exists(user)
        if is_new_user:
            user_id = db_operations.register_user(user, password)
            db_operations.add_attribute(user_id, 50, 50, 50, 50, 50, 50)
            raise_frame(params_frame)
            parameter_list = db_operations.get_attributes(user_id)
            print(parameter_list)
            lowRateInterval_field.delete(0, END) #deletes the current value
            lowRateInterval_field.insert(0, parameter_list[1])
            uppRateInterval_field.delete(0, END)
            uppRateInterval_field.insert(0, parameter_list[2])
            vPaceAmp_field.delete(0, END)
            vPaceAmp_field.insert(0, parameter_list[3])
            vPulseWidth_field.delete(0, END)
            vPulseWidth_field.insert(0, parameter_list[4])
            aPaceAmp_field.delete(0, END)
            aPaceAmp_field.insert(0, parameter_list[5])
            aPulseWidth_field.delete(0, END)
            aPulseWidth_field.insert(0, parameter_list[6])
        else:
            register_existinguser_label.place(relx=0.5, rely=0.85, anchor=CENTER)

def update_params():
    parameterlist = []
    parameterlist.append(lowRateInterval_field.get())
    parameterlist.append(uppRateInterval_field.get())
    parameterlist.append(vPaceAmp_field.get())
    parameterlist.append(vPulseWidth_field.get())
    parameterlist.append(aPaceAmp_field.get())
    parameterlist.append(aPulseWidth_field.get())
    global user_id
    db_operations.update_attribute(user_id, parameterlist)

def logout():
    raise_frame(intro_frame)
    lowRateInterval_field.delete(0, END) #deletes the current value
    uppRateInterval_field.delete(0, END)
    vPaceAmp_field.delete(0, END)
    vPulseWidth_field.delete(0, END)
    aPaceAmp_field.delete(0, END)
    aPulseWidth_field.delete(0, END)
    register_username_field.delete(0, END)
    register_password_field.delete(0, END)
    username_field.delete(0, END)
    password_field.delete(0, END)
    #unidentified_user_label.grid_remove()
    unidentified_user_label.place(relx=2, rely=2)
    full_label.grid_remove()

def back_from_login():
    raise_frame(intro_frame)
    #unidentified_user_label.grid_remove()
    unidentified_user_label.place(relx=2, rely=2)
    username_field.delete(0, END)
    password_field.delete(0, END)

def register_to_intro():
    raise_frame(intro_frame)
    register_missingfield_label.place(relx=2, rely=2)
    register_existinguser_label.place(relx=2, rely=2)
    register_username_field.delete(0, END)
    register_password_field.delete(0, END)


window = Tk()
window.geometry("1280x720") #Width x Height

window.grid_rowconfigure(0, weight=1) # this needed to be added
window.grid_columnconfigure(0, weight=1)

intro_frame = Frame(window)
login_frame = Frame(window, bg="black")
register_frame = Frame(window)
params_frame = Frame(window)

for frame in (intro_frame, login_frame, register_frame, params_frame):
    frame.grid(row=0, column=0, sticky='news')

window.wm_title("Elite Beat")
window.configure(background='black')



#intro_frame
img = ImageTk.PhotoImage(Image.open("test2.jpg"))
panel = Label(intro_frame, image = img)
panel.place(x=0, y=0, relwidth=1, relheight=1)
intro_title_label = Label(intro_frame, text="Elite Beat Pacemaker Device Control Monitor", fg = "red", bg="black", font = "Helvetica 16 bold italic", justify="center", padx=370, pady=100)
intro_title_label.grid(row=0, column=3, columnspan=12, pady=20, sticky=N+S+E+W)
intro_login_button = Button(intro_frame, text="Login", width=15, command=lambda:raise_frame(login_frame))
intro_login_button.place(relx=0.4, rely=0.5, anchor=CENTER)
#intro_login_button.grid(row=6, column=2, rowspan=2, columnspan=3, padx=10, pady=10)
intro_register_button = Button(intro_frame, text="Register New User", width=15, command=check_register_viability)
intro_register_button.place(relx=0.6, rely=0.5, anchor=CENTER)
#intro_register_button.grid(row=6, column=6, rowspan=2, columnspan=3, padx=10, pady=10)
full_label = Label(intro_frame, text="Max number of users allowed to be registered has been reached.", fg="red", font="Helvetica 14", justify="center")
raise_frame(intro_frame)

texture_img = ImageTk.PhotoImage(Image.open("texture.png"))

#login_frame
login_panel = Label(login_frame, image = texture_img)
login_panel.place(x=0, y=0, relwidth=1, relheight=1, height=0)

login_title_label = Label(login_frame, text="Login", fg = "white", bg="#31749b", font = "Georgia 16 bold", justify="center")
login_title_label.place(relx=0.5, rely=0.3, anchor=CENTER)
##4263f5, #19181A
username_label = Label(login_frame, text="Username:", font = "Helvetica 12 bold", justify="center", bg="#31749b", fg="white")
username_label.place(relx = 0.4, rely = 0.4, anchor=CENTER)
login_username = StringVar()
username_field = Entry(login_frame, textvariable=login_username, width=40)
username_field.place(relx = 0.6, rely = 0.4, anchor=CENTER)

password_label = Label(login_frame, text="Password:", bg="#31749b", fg="white", font = "Helvetica 12 bold", justify="center")
#password_label.grid(row=3, column=0, columnspan=2)
password_label.place(relx=0.4, rely=0.5, anchor=CENTER)
login_password = StringVar()
password_field = Entry(login_frame, textvariable=login_password, show="*", width=40)
password_field.place(relx=0.6, rely=0.5, anchor=CENTER)
#password_field.grid(row=3, column=2, columnspan=8, sticky=N+S+E+W)

login_button = Button(login_frame, text="Login", width=15, command=login)
login_button.place(relx=0.4, rely=0.6, anchor=CENTER)
#login_button.grid(row=4, column=2, columnspan=3, padx=10, pady=10)
back_login_button = Button(login_frame, text="Back", width=15, command=back_from_login)
back_login_button.place(relx=0.6, rely=0.6, anchor=CENTER)
#back_login_button.grid(row=4, column=7, columnspan=3, padx=10, pady=10)

unidentified_user_label = Label(login_frame, text="Did not recognize this username and password combination", font = "Helvetica 12", justify="center")



#register_frame
register_panel = Label(register_frame, image = texture_img)
register_panel.place(x=0, y=0, relwidth=1, relheight=1, height=0)

register_title_label = Label(register_frame, text="Register New User", fg = "white", bg="#31749b", font = "Georgia 16 bold", justify="center")
register_title_label.place(relx=0.5, rely=0.3, anchor=CENTER)

register_username_label = Label(register_frame, text="Username:", bg="#31749b", fg="white", font = "Helvetica 12", justify="center")
register_username_label.place(relx = 0.4, rely = 0.4, anchor=CENTER)
register_username = StringVar()
register_username_field = Entry(register_frame, textvariable=register_username, width=40)
register_username_field.place(relx = 0.6, rely = 0.4, anchor=CENTER)

register_password_label = Label(register_frame, text="Password:", bg="#31749b", fg="white", font = "Helvetica 12", justify="center")
register_password_label.place(relx=0.4, rely=0.5, anchor=CENTER)
register_password = StringVar()
register_password_field = Entry(register_frame, textvariable=register_password, show="*", width=40)
register_password_field.place(relx=0.6, rely=0.5, anchor=CENTER)

register_button = Button(register_frame, text="Register", width=15, command=register)
register_button.place(relx=0.4, rely=0.6, anchor=CENTER)
register_back_button = Button(register_frame, text="Back", width=15, command=register_to_intro)
register_back_button.place(relx=0.6, rely=0.6, anchor=CENTER)

register_missingfield_label = Label(register_frame, text="Username or password is missing", bg="#31749b", fg="orange", font="Helvetica 12 bold", justify="center")
register_existinguser_label = Label(register_frame, text="Username chosen already exists", bg="#31749b", fg="orange", font="Helvetica 12 bold", justify="center")


#params_frame
params_title_label = Label(params_frame, text="Programmable Parameters", fg = "white", bg="#31749b", font = "Georgia 16 bold", justify="center")
params_title_label.place(relx=0.5, rely=0.1, anchor=CENTER)

default = StringVar(params_frame)
default.set("VOO") # default value
pacingModeOption = OptionMenu(params_frame, default, "VOO", "AOO", "AAI", "VVI")
pacingModeOption.place(relx=0.6, rely=0.2, anchor=CENTER)

lowRateInterval_label = Label(params_frame, text="Lower Rate Limit:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
lowRateInterval_label.place(relx=0.4, rely=0.25, anchor=CENTER)
#lowRateInterval_label.grid(row=3, column=0, columnspan=2)
lowRateInterval = StringVar()
lowRateInterval_field = Entry(params_frame, textvariable=lowRateInterval)
lowRateInterval_field.place(relx=0.6, rely=0.25, anchor=CENTER)
#lowRateInterval_field.grid(row=3, column=2, columnspan=5)

uppRateInterval_label = Label(params_frame, text="Upper Rate Limit:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
uppRateInterval_label.place(relx=0.4, rely=0.3, anchor=CENTER)
#uppRateInterval_label.grid(row=4, column=0, columnspan=2)
uppRateInterval = StringVar()
uppRateInterval_field = Entry(params_frame, textvariable=uppRateInterval)
uppRateInterval_field.place(relx=0.6, rely=0.3, anchor=CENTER)
#uppRateInterval_field.grid(row=4, column=2, columnspan=5)

vPaceAmp_label = Label(params_frame, text="Ventricular Amplitude:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
vPaceAmp_label.place(relx=0.4, rely=0.35, anchor=CENTER)
#vPaceAmp_label.grid(row=5, column=0, columnspan=2)
vPaceAmp = StringVar()
vPaceAmp_field = Entry(params_frame, textvariable=vPaceAmp)
vPaceAmp_field.place(relx=0.6, rely=0.35, anchor=CENTER)
#vPaceAmp_field.grid(row=5, column=2, columnspan=5)

vPulseWidth_label = Label(params_frame, text="Ventricular Pulse Width:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
vPulseWidth_label.place(relx=0.4, rely=0.4, anchor=CENTER)
#vPulseWidth_label.grid(row=6, column=0, columnspan=2)
vPulseWidth = StringVar()
vPulseWidth_field = Entry(params_frame, textvariable=vPulseWidth)
vPulseWidth_field.place(relx=0.6, rely=0.4, anchor=CENTER)
#vPulseWidth_field.grid(row=6, column=2, columnspan=5)

aPaceAmp_label = Label(params_frame, text="Atrial Amplitude:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
aPaceAmp_label.place(relx=0.4, rely=0.45, anchor=CENTER)
#aPaceAmp_label.grid(row=7, column=0, columnspan=2)
aPaceAmp = StringVar()
aPaceAmp_field = Entry(params_frame, textvariable=aPaceAmp)
aPaceAmp_field.place(relx=0.6, rely=0.45, anchor=CENTER)
#aPaceAmp_field.grid(row=7, column=2, columnspan=5)

aPulseWidth_label = Label(params_frame, text="Atrial Pulse Width:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
aPulseWidth_label.place(relx=0.4, rely=0.5, anchor=CENTER)
#aPulseWidth_label.grid(row=8, column=0, columnspan=2)
aPulseWidth = StringVar()
aPulseWidth_field = Entry(params_frame, textvariable=aPulseWidth)
aPulseWidth_field.place(relx=0.6, rely=0.5, anchor=CENTER)
#aPulseWidth_field.grid(row=8, column=2, columnspan=5)

update_button = Button(params_frame, text="Update", width=15, command=update_params)
update_button.place(relx=0.4, rely=0.6, anchor=CENTER)
#update_button.grid(row=9, column=2, columnspan=3, padx=10, pady=10)
logout_button = Button(params_frame, text="Logout", width=15, command=logout)
logout_button.place(relx=0.6, rely=0.6, anchor=CENTER)
#logout_button.grid(row=9, column=7, columnspan=3, padx=10, pady=10)

communication_label = Label(params_frame, text="Communicating with pacemaker: No", font = "Helvetica 12", justify="left")
communication_label.place(relx=0.5, rely=0.7, anchor=CENTER)

unexpectedConn_label = Label(params_frame, text="--Unexpected Pacemaker Device Detected--", font = "Helvetica 12", justify="left")

window.mainloop()