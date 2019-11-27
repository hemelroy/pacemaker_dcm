#baud rate: 115200 bits/sec

#UI 
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
#database
import sqlite3
import db_operations
import serialComm
import time

############ Global non-widget variables ############
user_id = -1

############ Functions ############
#switch screens
def raise_frame(frame):
    frame.tkraise()

#determine if max number of users is registered
def check_register_viability():
    is_full = db_operations.check_user_count()
    
    if is_full:
        full_label.place(relx=0.5, rely=0.7, anchor=CENTER)
    else:
        raise_frame(register_frame)

#compare user credentials against database, log in user
def login():
	user = username_field.get()
	password = password_field.get()

	if not user and not password:
		login_missingfield_label.place(relx=0.5, rely=0.9, anchor=CENTER)
	else:
		global user_id
		user_id, params = db_operations.login_user(user, password)

		if params:
			lowRateInterval_field.delete(0, END) 
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
			vrp_field.delete(0, END)
			vrp_field.insert(0, params[7])
			arp_field.delete(0, END)
			arp_field.insert(0, params[8])
			avDelay_field.delete(0, END)
			avDelay_field.insert(0, params[9])
			raise_frame(params_frame)
		else:
			unidentified_user_label.place(relx=0.5, rely=0.8, anchor=CENTER)

def remove_error_messages():
	unidentified_user_label.place(relx=2, rely=2)
	register_missingfield_label.place(relx=2, rely=2)
	register_existinguser_label.place(relx=2, rely=2)
	full_label.place(relx=2, rely=2)
	login_missingfield_label.place(relx=2, rely=2)
	update_label.place(relx=2, rely=0.6, anchor=CENTER) #remove update label from parameter frame
	no_update_label.place(relx=2, rely=0.6, anchor=CENTER) #remove no update label from parameter frame

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
			db_operations.add_attribute(user_id, 60, 180, 2.5, 10, 2.5, 10, 320, 250, 150)
			raise_frame(params_frame)
			parameter_list = db_operations.get_attributes(user_id)
			print('Database:', parameter_list)
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
			vrp_field.delete(0, END)
			vrp_field.insert(0, parameter_list[7])
			arp_field.delete(0, END)
			arp_field.insert(0, parameter_list[8])
			avDelay_field.delete(0, END)
			avDelay_field.insert(0, parameter_list[9])

		else:
			register_existinguser_label.place(relx=0.5, rely=0.85, anchor=CENTER)

def update_params():
	serialCommTest()
	global user_id, confirmMode, communication_label
	if confirmMode == True:
		parameterlist = []
		try:
			update=(30 <= int(lowRateInterval_field.get()) <= 90 and 90 <= int(uppRateInterval_field.get()) <= 180 and
			0.00 <= float(vPaceAmp_field.get()) <= 5.00 and 1 <= int(vPulseWidth_field.get()) <= 100 and
			0.00 <= float(aPaceAmp_field.get()) <= 5.00 and 1 <= int(aPulseWidth_field.get()) <= 100 and
			150 <= int(vrp_field.get()) <= 500 and 150 <= int(arp_field.get()) <= 500 and 70 <= int(avDelay_field.get()) <= 300)
			if update:
				parameterlist.append(lowRateInterval_field.get())
				parameterlist.append(uppRateInterval_field.get())
				parameterlist.append(vPaceAmp_field.get())
				parameterlist.append(vPulseWidth_field.get())
				parameterlist.append(aPaceAmp_field.get())
				parameterlist.append(aPulseWidth_field.get())
				parameterlist.append(vrp_field.get())
				parameterlist.append(arp_field.get())
				parameterlist.append(avDelay_field.get())
				try:
					databaseList = parameterlist.copy()
					serialComm.serialTransmit(parameterlist, pacingModeOptionCount)
					print ('After Serial Before Database', databaseList)
					db_operations.update_attribute(user_id, databaseList)
					update_label.place(relx=0.5, rely=0.7, anchor=CENTER) #show update complete label from frame
					communication_label.config(text='Communicating with pacemaker: Yes')
				except:
					no_update_label['text'] = "Update Not Complete: Seems like there is no communication with the pacemaker"
					no_update_label.place(relx=0.5, rely=0.7, anchor=CENTER) #show update failed
					communication_label.config(text='Communicating with pacemaker: No')	
			else:
				no_update_label['text'] = "Update Not Complete: Value(s) were out of range!"
				no_update_label.place(relx=0.5, rely=0.7, anchor=CENTER) #show update failed	
		except:
			no_update_label['text'] = "Update Not Complete: Value(s) were not inputted in the correct format"
			no_update_label.place(relx=0.5, rely=0.7, anchor=CENTER) #show update failed if float inputted when expecting int
	elif confirmMode == False:
		no_update_label['text'] = "Please confirm the mode before sending update!"
		no_update_label.place(relx=0.5, rely=0.7, anchor=CENTER) #show update failed
		
def logout():
	raise_frame(intro_frame)
	lowRateInterval_field.delete(0, END)
	uppRateInterval_field.delete(0, END)
	vPaceAmp_field.delete(0, END)
	vPulseWidth_field.delete(0, END)
	aPaceAmp_field.delete(0, END)
	aPulseWidth_field.delete(0, END)
	vrp_field.delete(0, END)
	arp_field.delete(0, END)
	avDelay_field.delete(0,END)
	register_username_field.delete(0, END)
	register_password_field.delete(0, END)
	username_field.delete(0, END)
	password_field.delete(0, END)
	remove_error_messages()

def login_to_intro():
    raise_frame(intro_frame)
    remove_error_messages()
    username_field.delete(0, END)
    password_field.delete(0, END)

def register_to_intro():
    raise_frame(intro_frame)
    remove_error_messages()
    register_username_field.delete(0, END)
    register_password_field.delete(0, END)

#change parameter input display when pace mode changes
def update_params_page(direction):
	serialCommTest()
	hideAll()
	update_label.place(relx=2, rely=0.6, anchor=CENTER) #remove update label from frame
	no_update_label.place(relx=2, rely=0.6, anchor=CENTER) #remove no update label from frame
	global pacingModeOptionCount, pacingModeOptionText, pacingModes, numofModes, confirmMode
	if direction == 1: #cycle right
		confirmMode = False
		if pacingModeOptionCount == numofModes: #cycle through modes at the end
			pacingModeOptionCount = 0
		else:
			pacingModeOptionCount += 1
	elif direction == -1: #cycle left
		confirmMode = False
		if pacingModeOptionCount == 0: #cycle through modes at the end
			pacingModeOptionCount = numofModes
		else:
			pacingModeOptionCount -= 1
	elif direction == 0:
		confirmMode = True
	pacingModeOption['text'] = pacingModes[pacingModeOptionCount]

	if confirmMode == True:
		if pacingModeOptionCount == 0: #VOO
			hideAll()
			placeVentricle()
		elif pacingModeOptionCount == 1: #AOO
			hideAll()
			placeAtrial()
		elif pacingModeOptionCount == 2: #VVI
			hideAll()
			placeVentricle()
			placeVRP()
		elif pacingModeOptionCount == 3: #AAI
			hideAll()
			placeAtrial()
			placeARP()
		elif pacingModeOptionCount == 4: #VOOR
			hideAll()
			placeVentricle()
		elif pacingModeOptionCount == 5: #AOOR
			hideAll()
			placeAtrial()
		elif pacingModeOptionCount == 6: #DOO
			hideAll()
			placeDOOs(0,1)
		elif pacingModeOptionCount == 7: #DOOR
			hideAll()
			placeDOOs(1,1)
		elif pacingModeOptionCount == 8: #VVIR
			hideAll()
			placeDOOs(1,0)
			placeVRP()
		elif pacingModeOptionCount == 9: #AAIR
			hideAll()
			placeDOOs(1,0)
			placeARP()
		elif pacingModeOptionCount == 10: #DDDR
			hideAll()
			placeDOOs(1,1)
			placeARP()
			placeVRP()

def placeVentricle():
	serialCommTest()
	vPaceAmp_label.place(relx=0.4, rely=0.35, anchor=CENTER)
	vPulseWidth_label.place(relx=0.4, rely=0.4, anchor=CENTER)
	vPaceAmp_field.place(relx=0.6, rely=0.35, anchor=CENTER)
	vPulseWidth_field.place(relx=0.6, rely=0.40, anchor=CENTER)
	aPaceAmp_label.place(relx=2, rely=0.45, anchor=CENTER)
	aPulseWidth_label.place(relx=2, rely=0.5, anchor=CENTER)
	aPaceAmp_field.place(relx=2, rely=0.45, anchor=CENTER)
	aPulseWidth_field.place(relx=2, rely=0.50, anchor=CENTER)
	lowRateInterval_field.place(relx=0.6, rely=0.25, anchor=CENTER)
	uppRateInterval_field.place(relx=0.6, rely=0.3, anchor=CENTER)
	lowRateInterval_label.place(relx=0.4, rely=0.25, anchor=CENTER)
	uppRateInterval_label.place(relx=0.4, rely=0.3, anchor=CENTER)
	
def placeAtrial():
	serialCommTest()
	vPaceAmp_label.place(relx=2, rely=0.35, anchor=CENTER)
	vPulseWidth_label.place(relx=2, rely=0.4, anchor=CENTER)
	vPaceAmp_field.place(relx=2, rely=2, anchor=CENTER)
	vPulseWidth_field.place(relx=2, rely=2, anchor=CENTER)
	aPaceAmp_label.place(relx=0.4, rely=0.45, anchor=CENTER)
	aPulseWidth_label.place(relx=0.4, rely=0.5, anchor=CENTER)
	aPaceAmp_field.place(relx=0.6, rely=0.45, anchor=CENTER)
	aPulseWidth_field.place(relx=0.6, rely=0.50, anchor=CENTER)
	lowRateInterval_field.place(relx=0.6, rely=0.25, anchor=CENTER)
	uppRateInterval_field.place(relx=0.6, rely=0.3, anchor=CENTER)
	lowRateInterval_label.place(relx=0.4, rely=0.25, anchor=CENTER)
	uppRateInterval_label.place(relx=0.4, rely=0.3, anchor=CENTER)

def placeDOOs(selection,selectionAV):
	serialCommTest()
	lowRateInterval_label.place(relx=0.4, rely=0.25, anchor=CENTER)
	lowRateInterval_field.place(relx=0.6, rely=0.25, anchor=CENTER)
	vPaceAmp_label.place(relx=0.4, rely=0.35, anchor=CENTER)
	vPulseWidth_label.place(relx=0.4, rely=0.4, anchor=CENTER)
	vPaceAmp_field.place(relx=0.6, rely=0.35, anchor=CENTER)
	vPulseWidth_field.place(relx=0.6, rely=0.40, anchor=CENTER)
	aPaceAmp_label.place(relx=0.4, rely=0.45, anchor=CENTER)
	aPulseWidth_label.place(relx=0.4, rely=0.5, anchor=CENTER)
	aPaceAmp_field.place(relx=0.6, rely=0.45, anchor=CENTER)
	aPulseWidth_field.place(relx=0.6, rely=0.50, anchor=CENTER)
	if selection == 1:
		uppRateInterval_field.place(relx=0.6, rely=0.3, anchor=CENTER)
		uppRateInterval_label.place(relx=0.4, rely=0.3, anchor=CENTER)
	if selectionAV == 1:
		avDelay_label.place(relx=0.4, rely=0.65, anchor=CENTER)
		avDelay_field.place(relx=0.6, rely=0.65, anchor=CENTER)

def placeVRP():
	serialCommTest()
	vrp_label.place(relx=0.4, rely=0.55, anchor=CENTER)
	vrp_field.place(relx=0.6, rely=0.55, anchor=CENTER)

def placeARP():
	serialCommTest()
	arp_label.place(relx=0.4, rely=0.6, anchor=CENTER)
	arp_field.place(relx=0.6, rely=0.6, anchor=CENTER)
	
def hideAll():
	serialCommTest()
	vPaceAmp_label.place(relx=2, rely=0.35, anchor=CENTER)
	vPulseWidth_label.place(relx=2, rely=0.4, anchor=CENTER)
	vPaceAmp_field.place(relx=2, rely=2, anchor=CENTER)
	vPulseWidth_field.place(relx=2, rely=2, anchor=CENTER)
	aPaceAmp_label.place(relx=2, rely=0.45, anchor=CENTER)
	aPulseWidth_label.place(relx=2, rely=0.5, anchor=CENTER)
	aPaceAmp_field.place(relx=2, rely=0.45, anchor=CENTER)
	aPulseWidth_field.place(relx=2, rely=0.50, anchor=CENTER)
	lowRateInterval_field.place(relx=2, rely=0.25, anchor=CENTER)
	uppRateInterval_field.place(relx=2, rely=0.3, anchor=CENTER)
	lowRateInterval_label.place(relx=2, rely=0.25, anchor=CENTER)
	uppRateInterval_label.place(relx=2, rely=0.3, anchor=CENTER)
	vrp_field.place(relx=2, rely=0.3, anchor=CENTER)
	vrp_label.place(relx=2, rely=0.3, anchor=CENTER)
	arp_field.place(relx=2, rely=0.3, anchor=CENTER)
	arp_label.place(relx=2, rely=0.3, anchor=CENTER)
	avDelay_label.place(relx=2, rely=0.65, anchor=CENTER)
	avDelay_field.place(relx=2, rely=0.65, anchor=CENTER)


def show_egram():
	serialCommTest()
	serialComm.serialReceive()

def serialCommTest():
	try:
		serialComm.serialTest()
		communication_label.config(text = 'Communicating with pacemaker: YES')
	except:
		communication_label.config(text = 'Communicating with pacemaker: NO')

############ Window Configuration ############
window = Tk()
window.geometry("1280x720")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
window.wm_title("Elite Beat")
window.configure(background='black')
texture_img = ImageTk.PhotoImage(Image.open("texture.png")) #background image for frames

#Initialize Frames
intro_frame = Frame(window)
login_frame = Frame(window, bg="black")
register_frame = Frame(window)
params_frame = Frame(window)

for frame in (intro_frame, login_frame, register_frame, params_frame):
    frame.grid(row=0, column=0, sticky='news')

############ Widget Configuration ############
##intro_frame##
#Background image
intro_img = ImageTk.PhotoImage(Image.open("TitlePage.png"))
intro_panel = Label(intro_frame, image = intro_img)
intro_panel.place(x=0, y=0, relwidth=1, relheight=1)
#Buttons
intro_login_button = Button(intro_frame, text="Login", width=15, command=lambda:raise_frame(login_frame))
intro_login_button.place(relx=0.3, rely=0.5, anchor=CENTER)
intro_register_button = Button(intro_frame, text="Register New User", width=15, command=check_register_viability)
intro_register_button.place(relx=0.7, rely=0.5, anchor=CENTER)
#Error Labels
full_label = Label(intro_frame, text="Max number of users allowed to be registered has been reached.", fg="red", font="Helvetica 14", justify="center")
raise_frame(intro_frame)

##login_frame##
#Background image
login_panel = Label(login_frame, image = texture_img)
login_panel.place(x=0, y=0, relwidth=1, relheight=1, height=0)
#Title
login_title_label = Label(login_frame, text="Login", fg = "white", bg="#31749b", font = "Georgia 16 bold", justify="center")
login_title_label.place(relx=0.5, rely=0.3, anchor=CENTER)
#Username
username_label = Label(login_frame, text="Username:", font = "Helvetica 12 bold", justify="center", bg="#31749b", fg="white")
username_label.place(relx = 0.4, rely = 0.4, anchor=CENTER)
login_username = StringVar()
username_field = Entry(login_frame, textvariable=login_username, width=40)
username_field.place(relx = 0.6, rely = 0.4, anchor=CENTER)
#Password
password_label = Label(login_frame, text="Password:", bg="#31749b", fg="white", font = "Helvetica 12 bold", justify="center")
password_label.place(relx=0.4, rely=0.5, anchor=CENTER)
login_password = StringVar()
password_field = Entry(login_frame, textvariable=login_password, show="*", width=40)
password_field.place(relx=0.6, rely=0.5, anchor=CENTER)
#Buttons
login_button = Button(login_frame, text="Login", width=15, command=login)
login_button.place(relx=0.4, rely=0.6, anchor=CENTER)
back_login_button = Button(login_frame, text="Back", width=15, command=login_to_intro)
back_login_button.place(relx=0.6, rely=0.6, anchor=CENTER)
#Error labels
unidentified_user_label = Label(login_frame, text="Did not recognize this username and password combination", font = "Helvetica 12", justify="center")
login_missingfield_label = Label(login_frame, text="Username or password field is empty", font="Helvetica 12", justify="center")

#register_frame
#Background image
register_panel = Label(register_frame, image = texture_img)
register_panel.place(x=0, y=0, relwidth=1, relheight=1, height=0)
#Title
register_title_label = Label(register_frame, text="Register New User", fg = "white", bg="#31749b", font = "Georgia 16 bold", justify="center")
register_title_label.place(relx=0.5, rely=0.3, anchor=CENTER)
#Username
register_username_label = Label(register_frame, text="Username:", bg="#31749b", fg="white", font = "Helvetica 12", justify="center")
register_username_label.place(relx = 0.4, rely = 0.4, anchor=CENTER)
register_username = StringVar()
register_username_field = Entry(register_frame, textvariable=register_username, width=40)
register_username_field.place(relx = 0.6, rely = 0.4, anchor=CENTER)
#Password
register_password_label = Label(register_frame, text="Password:", bg="#31749b", fg="white", font = "Helvetica 12", justify="center")
register_password_label.place(relx=0.4, rely=0.5, anchor=CENTER)
register_password = StringVar()
register_password_field = Entry(register_frame, textvariable=register_password, show="*", width=40)
register_password_field.place(relx=0.6, rely=0.5, anchor=CENTER)
#Button
register_button = Button(register_frame, text="Register", width=15, command=register)
register_button.place(relx=0.4, rely=0.6, anchor=CENTER)
register_back_button = Button(register_frame, text="Back", width=15, command=register_to_intro)
register_back_button.place(relx=0.6, rely=0.6, anchor=CENTER)
#Error labels
register_missingfield_label = Label(register_frame, text="Username or password is missing", bg="#31749b", fg="orange", font="Helvetica 12 bold", justify="center")
register_existinguser_label = Label(register_frame, text="Username chosen already exists", bg="#31749b", fg="orange", font="Helvetica 12 bold", justify="center")

##params_frame##
#Background image
params_panel = Label(params_frame, image = texture_img)
params_panel.place(x=0, y=0, relwidth=1, relheight=1, height=0)
#Title
params_title_label = Label(params_frame, text="Programmable Parameters", fg = "white", bg="#31749b", font = "Georgia 16 bold", justify="center")
params_title_label.place(relx=0.5, rely=0.1, anchor=CENTER)

#Pacing Mode
pacingModes = ["VOO", "AOO", "VVI", "AAI", "VOOR", "AOOR", "DOO", "DOOR", "VVIR", "AAIR", "DDDR"]
numofModes = len(pacingModes) - 1
confirmMode = True
pacingModeOptionCount = 0
pacingModeOptionText = "VOO"
pacingModeOption = Label(params_frame , text = pacingModeOptionText, fg = "white", bg="#31749b", font = "Helvetica 12")
pacingModeOption.place(relx=0.5, rely=0.2, anchor=CENTER)

#Lower Rate Interval
lowRateInterval_label = Label(params_frame, text="Lower Rate Limit [30 - 90 bpm]:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
lowRateInterval_label.place(relx=0.4, rely=0.25, anchor=CENTER)
lowRateInterval = StringVar()
lowRateInterval_field = Entry(params_frame, textvariable=lowRateInterval)
lowRateInterval_field.place(relx=0.6, rely=0.25, anchor=CENTER)
#Upper Rate Interval
uppRateInterval_label = Label(params_frame, text="Upper Rate Limit [90 - 180 bpm]:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
uppRateInterval_label.place(relx=0.4, rely=0.3, anchor=CENTER)
uppRateInterval = StringVar()
uppRateInterval_field = Entry(params_frame, textvariable=uppRateInterval)
uppRateInterval_field.place(relx=0.6, rely=0.3, anchor=CENTER)
#Ventricle Pace Amplitude
vPaceAmp_label = Label(params_frame, text="Ventricular Amplitude [0 - 5.0 V]:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
vPaceAmp_label.place(relx=0.4, rely=0.35, anchor=CENTER)
vPaceAmp = StringVar()
vPaceAmp_field = Entry(params_frame, textvariable=vPaceAmp)
vPaceAmp_field.place(relx=0.6, rely=0.35, anchor=CENTER)
#Ventricle pulse width
vPulseWidth_label = Label(params_frame, text="Ventricular Pulse Width [1 - 100 ms]:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
vPulseWidth_label.place(relx=0.4, rely=0.4, anchor=CENTER)
vPulseWidth = StringVar()
vPulseWidth_field = Entry(params_frame, textvariable=vPulseWidth)
vPulseWidth_field.place(relx=0.6, rely=0.4, anchor=CENTER)
#Atrial pace amplitude
aPaceAmp_label = Label(params_frame, text="Atrial Amplitude [0 - 5 V]: ", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
aPaceAmp_label.place(relx=2, rely=0.45, anchor=CENTER)
aPaceAmp = StringVar()
aPaceAmp_field = Entry(params_frame, textvariable=aPaceAmp)
aPaceAmp_field.place(relx=2, rely=0.45, anchor=CENTER)
#Atrial pulse width
aPulseWidth_label = Label(params_frame, text="Atrial Pulse Width [1 - 100 ms]: ", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
aPulseWidth_label.place(relx=2, rely=0.5, anchor=CENTER)
aPulseWidth = StringVar()
aPulseWidth_field = Entry(params_frame, textvariable=aPulseWidth)
aPulseWidth_field.place(relx=2, rely=0.5, anchor=CENTER)
#Ventrical refractory period
vrp_label = Label(params_frame, text="Ventricle Refractory Period [150 - 500 ms]:", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
vrp_label.place(relx=2, rely=0.55, anchor=CENTER)
vrp = StringVar()
vrp_field = Entry(params_frame, textvariable=vrp)
vrp_field.place(relx=2, rely=0.55, anchor=CENTER)
#Atrial refractory period
arp_label = Label(params_frame, text="Atrial Refractory Period [150 - 500 ms] :", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
arp_label.place(relx=2, rely=0.6, anchor=CENTER)
arp = StringVar()
arp_field = Entry(params_frame, textvariable=arp)
arp_field.place(relx=2, rely=0.6, anchor=CENTER)
#AV Delay Period
avDelay_label = Label(params_frame, text="AV Delay [70 - 300 ms] :", fg = "white", bg="#31749b", font = "Helvetica 12", justify="left")
avDelay_label.place(relx=2, rely=0.65, anchor=CENTER)
avDelay = StringVar()
avDelay_field = Entry(params_frame, textvariable=avDelay)
avDelay_field.place(relx=2, rely=0.65, anchor=CENTER)
#Buttons
update_button = Button(params_frame, text="Update", width=15, command=update_params)
update_button.place(relx=0.4, rely=0.85, anchor=CENTER)
modeRight_button = Button(params_frame, text="->", width=5, command= lambda: update_params_page(1))
modeRight_button.place(relx=0.6, rely=0.2, anchor=CENTER)
modeLeft_button = Button(params_frame, text="<-", width=5, command= lambda: update_params_page(-1))
modeLeft_button.place(relx=0.4, rely=0.2, anchor=CENTER)
logout_button = Button(params_frame, text="Logout", width=15, command=logout)
logout_button.place(relx=0.6, rely=0.85, anchor=CENTER)
confirm_button = Button(params_frame, text="CONFIRM", width=15, command= lambda: update_params_page(0))
confirm_button.place(relx=0.7, rely=0.2, anchor=CENTER)
egram_button = Button(params_frame, text="EGRAM", width=15, command=show_egram)
egram_button.place(relx=0.9, rely=0.9, anchor=CENTER)
#Indicator Labels
communication_label = Label(params_frame, text="Communicating with pacemaker: No", font = "Helvetica 12", justify="left")
communication_label.place(relx=0.5, rely=0.75, anchor=CENTER)
unexpectedConn_label = Label(params_frame, text="--Unexpected Pacemaker Device Detected--", font = "Helvetica 12", justify="left")
update_label = Label(params_frame, text="Update Complete", font = "Helvetica 12", justify="center")
update_label.place(relx=2, rely=0.70, anchor=CENTER) #remove update label from frame

noUpdateText = ""
no_update_label= Label(params_frame , text = noUpdateText, font = "Helvetica 12", justify = "center")
no_update_label.place(relx=2, rely=0.70, anchor=CENTER) #remove no update label from frame

window.mainloop()
