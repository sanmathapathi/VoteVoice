from tkinter import *
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from PIL import Image, ImageTk
import datetime
import time

#connecting to the Database
db = mysql.connector.connect(
    host="sql3.freemysqlhosting.net",
    user="sql3355866",
    passwd="zQfhdzzy2f",
    db="sql3355866"
)

#Creating a cursor that will write SQL code and interact with the databse
global cursor
cursor = db.cursor(buffered=True)

#getting the current time for various features
current_time = datetime.datetime.now()

#saving what has been entered for the post into the Database
def post_data():
    #getting the current row number
    get_rownum = "SELECT COUNT(*) FROM posts"
    cursor.execute(get_rownum)
    posts_string = str(cursor.fetchall())
    posts1 = posts_string.replace("'", "")
    posts2 = posts1.replace("[", "")
    posts3 = posts2.replace("]", "")
    posts4 = posts3.replace("(", "")
    posts5 = posts4.replace(")", "")
    posts6 = posts5.replace(",", "")
    currentrownum = int(posts6)

    if area == 'l':
        try:
            post = "INSERT INTO posts (rownum, user, date, subject, area, title, description, upvotes, downvotes, gov1, gov2, gov3, gov4, gov5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            postdetails = (currentrownum + 1, username_final, str(current_time.strftime("%m/%d/%y")), posttype, area, post_title, post_description, 0, 0, local1data, local2data, local3data, local4data, local5data)
            cursor.execute(post, postdetails)
            db.commit()
        except:
            post = "INSERT INTO posts (rownum, user, date, subject, area, title, description, upvotes, downvotes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            postdetails = (currentrownum + 1, username_final, str(current_time.strftime("%m/%d/%y")), posttype, area, post_title, post_description, 0, 0)
            cursor.execute(post, postdetails)
            db.commit()
    elif area =='s':
        try:
            post = "INSERT INTO posts (rownum, user, date, subject, area, title, description, upvotes, downvotes, gov1, gov2) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            postdetails = (currentrownum + 1, username_final, str(current_time.strftime("%m/%d/%y")), posttype, area, post_title, post_description, 0, 0, state1data, state2data)
            cursor.execute(post, postdetails)
            db.commit()
        except:
            post = "INSERT INTO posts (rownum, user, date, subject, area, title, description, upvotes, downvotes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            postdetails = (currentrownum + 1, username_final, str(current_time.strftime("%m/%d/%y")), posttype, area, post_title, post_description, 0, 0)
            cursor.execute(post, postdetails)
            db.commit()
    elif area == 'f':
        try:
            post = "INSERT INTO posts (rownum, user, date, subject, area, title, description, upvotes, downvotes, gov1, gov2, gov3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            postdetails = (currentrownum + 1, username_final, str(current_time.strftime("%m/%d/%y")), posttype, area, post_title, post_description, "0", "0", federal1data, federal2data, federal3data)
            cursor.execute(post, postdetails)
            db.commit()
        except:
            post = "INSERT INTO posts (rownum, user, date, subject, area, title, description, upvotes, downvotes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            postdetails = (currentrownum + 1, username_final, str(current_time.strftime("%m/%d/%y")), posttype, area, post_title, post_description, "0", "0")
            cursor.execute(post, postdetails)
            db.commit()

    postbutton.destroy()
    editbutton.destroy()

    global successlabel
    successlabel = Label(window, text = "Posted Successfully.", font="none 14", bg="white", fg="green")
    successlabel.place(x=400, y=540)

def edit():
    post_preview.destroy()
    editbutton.destroy()
    newpostbutton.destroy()

    previousarea = area

    session_background_label.config(image = post_background_image)
    create_post()
    preview_post_destroy()
    #Inserting the posttype
    if posttype == 'e':
        posttype_education()
    elif posttype == 's':
        posttype_safety()
    elif posttype == 'h':
        posttype_health()
    elif posttype == 'b':
        posttype_business()
    else:
        posttype_other()
        other_entry.insert(newposttype)
        new_posttype()

    #selecting the area previously selected
    if previousarea == 'l':
        localselect()
    elif previousarea == 's':
        stateselect()
    elif previousarea == 'f':
        federalselect()

    #Inserting the title and description
    title_text.insert('1.0', post_title)

    description.insert('1.0', post_description)

#creating a frame that represents what the post will look like to other users
def preview_post_screen():
    global post_preview
    post_preview = Frame(window, bg="white", width=700, height=157, bd=3, relief="ridge")
    post_preview.place(x=150, y=380)

    global post_background_image
    global post_background_label
    post_background_image = PhotoImage(file = "projectimages\\post_frame_background.png")
    post_background_label = Label(post_preview, image = post_background_image)
    post_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #adding icon to frame representing subject it covers
    global posttype_label
    if posttype == "e":
        print(posttype)
        posttype_label = Label(post_preview, image = educationicon, bg="white", borderwidth=0)
        posttype_label.place(x=3, y=3)

    elif posttype == "s":
        posttype_label = Label(post_preview, image = safetyicon, bg="white", borderwidth=0)
        posttype_label.place(x=3, y=3)

    elif posttype == "h":
        posttype_label = Label(post_preview, image = healthicon, bg="white", borderwidth=0)
        posttype_label.place(x=3, y=3)

    elif posttype == "b":
        posttype_label = Label(post_preview, image = businessicon, bg="white", borderwidth=0)
        posttype_label.place(x=3, y=3)

    else:
        global othersubjectselected
        othersubjectselected = "True"
        posttype_label = Label(post_preview, text=newposttype, bg="white", font="none 10 bold", borderwidth=0)
        posttype_label.place(x=0, y=1)

    global arealabel
    #Writing Area in Frame
    if area == "l":
        arealabel = Label(post_preview, text="Local", bg="white", font="none 12 italic")
        try:
            if othersubjectselected == "True":
                arealabel.config(font="none 10 italic")
                arealabel.place(x=0, y=18)

        except:
            arealabel.place(x=40, y=18)

    if area == "s":
        arealabel = Label(post_preview, text="State", bg="white", font="none 12 italic")
        try:
            if othersubjectselected == "True":
                arealabel.config(font="none 10 italic")
                arealabel.place(x=0, y=18)
        except:
            arealabel.place(x=40, y=18)

    if area == "f":
        arealabel = Label(post_preview, text="Federal", bg="white", font="none 12 italic")
        try:
            if othersubjectselected == "True":
                arealabel.config(font="none 10 italic")
                arealabel.place(x=0, y=18)
        except:
            arealabel.place(x=40, y=18)



    #Writing Main Idea in Frame
    global mainidea
    mainidea = Label(post_preview, text=post_title, bg="white", font="none 12 bold", wraplength=690)
    mainidea.place(x=85, y=18)

    #writing description in frame
    global description
    description = Label(post_preview, text=post_description, bg="white", font="none 12", wraplength=690, anchor=W, justify=LEFT)
    description.place(x=0, y=50)

    #placing line separator
    global line
    line = PhotoImage(file = "projectimages\\line.png")

    line_label = Label(post_preview, image=line, bg="white", borderwidth=0)
    line_label.place(x=0, y=40)

    #Edit Button
    global editpicture
    editpicture = PhotoImage(file = "projectimages\\edit.png")

    global editbutton
    editbutton = Button(window, image=editpicture, borderwidth=0, bg="white", command=edit)
    editbutton.place(x=475, y=540)

    #Post Button
    global postpicture
    postpicture = PhotoImage(file = "projectimages\\post.png")

    global postbutton
    postbutton = Button(window, image=postpicture, borderwidth=0, bg="white", command=post_data)
    postbutton.place(x=472, y=580)

def clear_screen():
    #clearing the screen
    educationbutton.destroy()
    safetybutton.destroy()
    healthbutton.destroy()
    businessbutton.destroy()
    morebutton.destroy()
    local.destroy()
    state.destroy()
    federal.destroy()
    title_text.destroy()
    description.destroy() #get
    yesbutton.destroy()
    nobutton.destroy()
    continue_button.destroy()

    try:
        localcheckbutton1.destroy()
        localcheckbutton2.destroy()
        localcheckbutton3.destroy()
        localcheckbutton4.destroy()
        localcheckbutton5.destroy()

    except:
        print(" ")

    try:
        statecheckbutton1.destroy()
        statecheckbutton2.destroy()

    except:
        print(" ")

    try:
        federalcheckbutton1.destroy()
        federalcheckbutton2.destroy()
        federalcheckbutton3.destroy()

    except:
        print(" ")

    try:
        tryagainbutton.destroy()

    except:
        print(" ")

    try:
        changeareabutton.destroy()

    except:
        print(" ")

    try:
        notcompleted.destroy()

    except:
        print(" ")

    try:
        other_entry.destroy()
        submitbutton.destroy()

    except:
        print(" ")

    try:
        edit_profile_destroy()

    except:
        print(" ")

    #changing to next screen
    global preview_background
    preview_background = PhotoImage(file = "projectimages\\preview_sessionbackground.png")

    session_background_label.config(image = preview_background)

    preview_post_screen()

def not_completed():
    global notcompleted
    notcompleted = Label(window, text = "Please fill out/select all fields.", fg="red", font="none 12", bg="white")
    notcompleted.place(x=375, y=665)

#Verifying everything was filled out
def verify_post_completion():
    try:
        if posttype == "e" or posttype == "s" or posttype == "h" or posttype == "b" or posttype == newposttype:
            if area =="l" or area =="s" or area =="f":
                if len(post_title) >= 2:
                    if len(post_description) >= 2:
                        clear_screen()
                    else:
                        print("failed with post description")
                        not_completed()
                else:
                    print("failed with post title")
                    not_completed()
    except NameError:
        print("failed with name error")
        not_completed()


#saving post data
def save_postdata():
    #getting unsaved data
    global post_title
    global post_description
    post_title = title_text.get('1.0', END)
    post_description = description.get('1.0', END)

    if area == "l":
        try:
            global local1data
            global local2data
            global local3data
            global local4data
            global local5data

            local1data = local1.get()
            local2data = local2.get()
            local3data = local3.get()
            local4data = local4.get()
            local5data = local5.get()

        except:
            print(" ")

    if area == "s":
        try:
            global state1data
            global state2data

            state1data = state1.get()
            state2data = state2.get()

        except:
            print(" ")

    if area == "f":
        try:
            global federal1data
            global federal2data
            global federal3data

            federal1data = federal1.get()
            federal2data = federal2.get()
            federal3data = federal3.get()

        except:
            print(" ")

    verify_post_completion()
def posttype_education():
    global posttype
    posttype = StringVar()
    posttype = 'e' #stands for education, trying to keep database compact

    #disabling button after being clicked
    educationbutton.config(state='disabled')

    #enabling all other buttons
    safetybutton.config(state='normal')
    healthbutton.config(state='normal')
    businessbutton.config(state='normal')
    morebutton.config(state='normal')

    try:
        other_entry.destroy()
        submitbutton.destroy()

    except:
        print(" ")

def posttype_safety():
    global posttype
    posttype = StringVar()
    posttype = 's'

    safetybutton.config(state='disabled')

    educationbutton.config(state='normal')
    healthbutton.config(state='normal')
    businessbutton.config(state='normal')
    morebutton.config(state='normal')

    try:
        other_entry.destroy()
        submitbutton.destroy()

    except:
        print(" ")

def posttype_health():
    global posttype
    posttype = StringVar()
    posttype = 'h'

    healthbutton.config(state='disabled')

    educationbutton.config(state='normal')
    safetybutton.config(state='normal')
    businessbutton.config(state='normal')
    morebutton.config(state='normal')

    try:
        other_entry.destroy()
        submitbutton.destroy()

    except:
        print(" ")
def posttype_business():
    global posttype
    posttype = StringVar()
    posttype = 'b'

    businessbutton.config(state='disabled')

    educationbutton.config(state='normal')
    safetybutton.config(state='normal')
    healthbutton.config(state='normal')
    morebutton.config(state='normal')

    try:
        other_entry.destroy()
        submitbutton.destroy()

    except:
        print(" ")

def new_posttype():
    morebutton.config(state='disabled')

    global newposttype
    newposttype = othersubject.get()

    global posttype
    posttype = newposttype


def posttype_other():
    businessbutton.config(state='normal')
    educationbutton.config(state='normal')
    safetybutton.config(state='normal')
    healthbutton.config(state='normal')
    morebutton.config(state='normal')

    global othersubject

    othersubject = StringVar()

    global other_entry
    other_entry = Entry(window, textvariable = othersubject, width=10)
    other_entry.place(x=730, y=372)

    global submitbutton
    submitbutton = Button(window, text="Enter", command=new_posttype)
    submitbutton.place(x=800, y=372)

#area selection commands
def localselect():
    global area
    area = StringVar()
    area = "l"

    local.configure(state="disabled")
    state.configure(state="normal")
    federal.configure(state="normal")

def stateselect():
    global area
    area = StringVar()
    area = "s"

    state.configure(state="disabled")
    local.configure(state="normal")
    federal.configure(state="normal")

def federalselect():
    global area
    area = StringVar()
    area = "f"

    federal.configure(state="disabled")
    local.configure(state="normal")
    state.configure(state="normal")

def no_forward():
    global continue_image
    continue_image = PhotoImage(file = "projectimages\\continue.png")

    global continue_button
    continue_button = Button(window, image=continue_image, command=save_postdata, borderwidth=0, bg="white")
    continue_button.place(x=425, y=680)
#Selecting whether or not the post should be forwarded to representatives
def forward():
    global localcheckbutton1
    global localcheckbutton2
    global localcheckbutton3
    global localcheckbutton4
    global localcheckbutton5
    global statecheckbutton1
    global statecheckbutton2
    global federalcheckbutton1
    global federalcheckbutton2
    global federalcheckbutton3

    try:
        localcheckbutton1.destroy()
        localcheckbutton2.destroy()
        localcheckbutton3.destroy()
        localcheckbutton4.destroy()
        localcheckbutton5.destroy()

    except:
        print(" ")

    try:
        statecheckbutton1.destroy()
        statecheckbutton2.destroy()

    except:
        print(" ")

    try:
        federalcheckbutton1.destroy()
        federalcheckbutton2.destroy()
        federalcheckbutton3.destroy()

    except:
        print(" ")

    global local_forward_background_image
    local_forward_background_image = PhotoImage(file = "projectimages\\local_forward_sessionbackground.png")

    global state_forward_background_image
    state_forward_background_image = PhotoImage(file = "projectimages\\state_forward_sessionbackground.png")

    global federal_forward_background_image
    federal_forward_background_image = PhotoImage(file = "projectimages\\federal_forward_sessionbackground.png")

    global unselected_forward_background_image
    unselected_forward_background_image = PhotoImage(file = "projectimages\\unselected_forward_sessionbackground.png")

    yesbutton.destroy()
    nobutton.destroy()

    global tryagain
    tryagain = PhotoImage(file = "projectimages\\tryagain.png")

    global tryagainbutton
    tryagainbutton = Button(window, image=tryagain, command=forward, borderwidth=0, bg="white")
    tryagainbutton.place(x=745, y=666)

    global changearea
    changearea = PhotoImage(file = "projectimages\\changearea.png")

    global changeareabutton
    changeareabutton = Button(window, image=changearea, command=forward, borderwidth=0, bg="white")
    changeareabutton.place(x=745, y=666)

    global continue_image
    continue_image = PhotoImage(file = "projectimages\\continue.png")

    global continue_button
    continue_button = Button(window, image=continue_image, command=save_postdata, borderwidth=0, bg="white")
    continue_button.place(x=425, y=680)

    if area == "l":
        try:
            tryagainbutton.destroy()

        except:
            print(" ")

        session_background_label.config(image=local_forward_background_image)

        #Checkboxes to select the representatives they would like to contact
        global local1
        global local2
        global local3
        global local4
        global local5

        local1 = StringVar()
        local2 = StringVar()
        local3 = StringVar()
        local4 = StringVar()
        local5 = StringVar()

        localcheckbutton1 = Checkbutton(window, variable = local1, bg="white", onvalue="1", offvalue="0")
        localcheckbutton1.deselect()
        localcheckbutton1.place(x=125, y=618)

        localcheckbutton2 = Checkbutton(window, variable = local2, bg="white", onvalue="1", offvalue="0")
        localcheckbutton2.deselect()
        localcheckbutton2.place(x=294, y=618)

        localcheckbutton3 = Checkbutton(window, variable = local3, bg="white", onvalue="1", offvalue="0")
        localcheckbutton3.deselect()
        localcheckbutton3.place(x=490, y=618)

        localcheckbutton4 = Checkbutton(window, variable = local4, bg="white", onvalue="1", offvalue="0")
        localcheckbutton4.deselect()
        localcheckbutton4.place(x=700, y=618)

        localcheckbutton5 = Checkbutton(window, variable = local5, bg="white", onvalue="1", offvalue="0")
        localcheckbutton5.deselect()
        localcheckbutton5.place(x=900, y=618)

    if area == "s":
        try:
            tryagainbutton.destroy()

        except:
            print(" ")

        session_background_label.config(image=state_forward_background_image)

        global state1
        global state2

        state1 = StringVar()
        state2 = StringVar()

        statecheckbutton1 = Checkbutton(window, variable = state1, bg="white", onvalue="1", offvalue="0")
        statecheckbutton1.deselect()
        statecheckbutton1.place(x=403, y=618)

        statecheckbutton2 = Checkbutton(window, variable = state2, bg="white", onvalue="1", offvalue="0")
        statecheckbutton2.deselect()
        statecheckbutton2.place(x=646, y=618)

    if area == "f":
        try:
            tryagainbutton.destroy()

        except:
            print(" ")

        session_background_label.config(image=federal_forward_background_image)

        global federal1
        global federal2
        global federal3

        federal1 = StringVar()
        federal2 = StringVar()
        federal3 = StringVar()

        federalcheckbutton1 = Checkbutton(window, variable = federal1, bg="white", onvalue="1", offvalue="0")
        federalcheckbutton1.deselect()
        federalcheckbutton1.place(x=290, y=618)

        federalcheckbutton2 = Checkbutton(window, variable = federal2, bg="white", onvalue="1", offvalue="0")
        federalcheckbutton2.deselect()
        federalcheckbutton2.place(x=520, y=618)

        federalcheckbutton3 = Checkbutton(window, variable = federal3, bg="white", onvalue="1", offvalue="0")
        federalcheckbutton3.deselect()
        federalcheckbutton3.place(x=810, y=618)

    if area == "u":
        changeareabutton.destroy()
        session_background_label.config(image=unselected_forward_background_image)

def preview_post_destroy():
    post_preview.destroy()

def create_post_destroy():
    educationbutton.destroy()
    safetybutton.destroy()
    healthbutton.destroy()
    businessbutton.destroy()
    morebutton.destroy()
    local.destroy()
    state.destroy()
    federal.destroy()
    title_text.destroy()
    description.destroy() #get
    yesbutton.destroy()
    nobutton.destroy()
    continue_button.destroy()

    try:
        localcheckbutton1.destroy()
        localcheckbutton2.destroy()
        localcheckbutton3.destroy()
        localcheckbutton4.destroy()
        localcheckbutton5.destroy()

    except:
        print(" ")

    try:
        statecheckbutton1.destroy()
        statecheckbutton2.destroy()

    except:
        print(" ")

    try:
        federalcheckbutton1.destroy()
        federalcheckbutton2.destroy()
        federalcheckbutton3.destroy()

    except:
        print(" ")

    try:
        tryagainbutton.destroy()

    except:
        print(" ")

    try:
        changeareabutton.destroy()

    except:
        print(" ")

    try:
        notcompleted.destroy()

    except:
        print(" ")

    try:
        other_entry.destroy()
        submitbutton.destroy()

    except:
        print(" ")

#posting screen
def create_post():
    try:
        feed_destroy()
    except:
        print(" ")

    try:
        edit_profile_destroy()

    except:
        print(" ")

    try:
        preview_post_destroy()

    except:
        print(" ")
    #changing the background to have post background UI
    global post_background_image
    post_background_image = PhotoImage(file = "projectimages\\post_sessionbackground.png")

    session_background_label.config(image=post_background_image)

    #Icons + Buttons for subject selection
    global educationicon
    educationicon = PhotoImage(file = "projectimages\\book.png")

    global educationbutton
    educationbutton = Button(window, image=educationicon, borderwidth=0, bg="white", command=posttype_education)
    educationbutton.place(x=250, y=363)

    global safetyicon
    safetyicon = PhotoImage(file = "projectimages\\safety.png")

    global safetybutton
    safetybutton = Button(window, image=safetyicon, borderwidth=0, bg="white", command=posttype_safety)
    safetybutton.place(x=363, y=363)

    global healthicon
    healthicon = PhotoImage(file = "projectimages\\hospital.png")

    global healthbutton
    healthbutton = Button(window, image=healthicon, borderwidth=0, bg="white", command=posttype_health)
    healthbutton.place(x=473, y=362)

    global businessicon
    businessicon = PhotoImage(file = "projectimages\\invoice.png")

    global businessbutton
    businessbutton = Button(window, image=businessicon, borderwidth=0, bg="white", command=posttype_business)
    businessbutton.place(x=588, y=365)

    global moreicon
    moreicon = PhotoImage(file = "projectimages\\more.png")

    global morebutton
    morebutton = Button(window, image=moreicon, borderwidth=0, bg="white", command=posttype_other)
    morebutton.place(x=690, y=363)

    #Area selection
    global area
    area = StringVar()
    area = "u" #undefined for now

    global localicon
    localicon = PhotoImage(file = "projectimages\\local.png")

    global local
    local = Button(window, image=localicon, command=localselect, borderwidth=0, bg="white")
    local.place(x=307, y=415)

    global stateicon
    stateicon = PhotoImage(file = "projectimages\\state.png")

    global state
    state = Button(window, image=stateicon, command=stateselect, borderwidth=0, bg="white")
    state.place(x=470, y=415)

    global federalicon
    federalicon = PhotoImage(file = "projectimages\\federal.png")

    global federal
    federal = Button(window, image=federalicon, command=federalselect, borderwidth=0, bg="white")
    federal.place(x=639, y=415)

    #Labels + Entries for the post
    global posttitle
    posttitle = StringVar()

    global title_text
    title_text = Text(window, height=2, width=70)
    title_text.place(x=200, y=450)

    global description
    description = Text(window, height=5, width=70)
    description.place(x=200, y=505)

    global yesicon
    yesicon = PhotoImage(file = "projectimages\\yes.png")

    global yesbutton
    yesbutton = Button(window, image=yesicon, command=forward, borderwidth=0, bg="white")
    yesbutton.place(x=600, y=644)

    global noicon
    noicon = PhotoImage(file = "projectimages\\no.png")

    global nobutton
    nobutton = Button(window, image=noicon, command=no_forward, borderwidth=0, bg="white")
    nobutton.place(x=630, y=643)

    global homeicon
    homeicon = PhotoImage(file="projectimages\\homeicon.png")

    homebutton = Button(window, image=homeicon, command=home, borderwidth=0, bg="black")
    homebutton.place(x=455, y=240)

    global profileicon
    profileicon = PhotoImage(file="projectimages\\user.png")

    profilebutton = Button(window, image=profileicon, command=edit_profile, borderwidth=0, bg="black")
    profilebutton.place(x=655, y=240)

def feed_destroy():
    votes_remaining.destroy()
    main_frame.destroy()

def agree(varname):
    rownum_get = varname.replace("agreebutton", "")

    get_current_upvotes = "SELECT upvotes FROM posts WHERE rownum = %s"
    cursor.execute(get_current_upvotes, (rownum_get,))
    upvotes_returned = cursor.fetchall()
    upvotes_string = str(upvotes_returned)
    upvotes1 = upvotes_string.replace("[", "")
    upvotes2 = upvotes1.replace("]", "")
    upvotes3 = upvotes2.replace("(", "")
    upvotes4 = upvotes3.replace(")", "")
    upvotes5 = upvotes4.replace("'", "")
    upvotes_got = upvotes5.replace(",", "")

    addition = (int(upvotes_got) + 1,)

    add_upvotes = "UPDATE posts SET upvotes = %s WHERE rownum = " + rownum_get
    cursor.execute(add_upvotes, addition)

    db.commit()

    get_current_uservotes = "SELECT votes FROM userinfo WHERE username = %s"
    cursor.execute(get_current_uservotes, username_get)
    current_uservotes = cursor.fetchall()

    current_votes_string = str(current_uservotes)
    current_votes1 = current_votes_string.replace("[", "")
    current_votes2 = current_votes1.replace("]", "")
    current_votes3 = current_votes2.replace("(", "")
    current_votes4 = current_votes3.replace(")", "")
    current_votes5 = current_votes4.replace("'", "")
    current_votes_got = current_votes5.replace(",", "")

    votesremaining = str(int(current_votes_got) - 1)
    if (int(current_votes_got) - 1) <= 0:
        votesremaining = str(0)

    remove_uservote = "UPDATE userinfo SET votes = " + votesremaining + " WHERE username = %s"
    cursor.execute(remove_uservote, username_get)

    db.commit()

    feed_destroy()
    feed()

def disagree(varname):
    rownum_get = varname.replace("disagreebutton", "")

    get_current_downvotes = "SELECT downvotes FROM posts WHERE rownum = %s"
    cursor.execute(get_current_downvotes, (rownum_get,))
    downvotes_returned = cursor.fetchall()
    downvotes_string = str(downvotes_returned)
    downvotes1 = downvotes_string.replace("[", "")
    downvotes2 = downvotes1.replace("]", "")
    downvotes3 = downvotes2.replace("(", "")
    downvotes4 = downvotes3.replace(")", "")
    downvotes5 = downvotes4.replace("'", "")
    downvotes_got = downvotes5.replace(",", "")

    subtraction = (int(downvotes_got) + 1,)

    add_downvotes = "UPDATE posts SET downvotes = %s WHERE rownum = " + rownum_get
    cursor.execute(add_downvotes, subtraction)

    db.commit()

    get_current_uservotes = "SELECT votes FROM userinfo WHERE username = %s"
    cursor.execute(get_current_uservotes, username_get)
    current_uservotes = cursor.fetchall()

    current_votes_string = str(current_uservotes)
    current_votes1 = current_votes_string.replace("[", "")
    current_votes2 = current_votes1.replace("]", "")
    current_votes3 = current_votes2.replace("(", "")
    current_votes4 = current_votes3.replace(")", "")
    current_votes5 = current_votes4.replace("'", "")
    current_votes_got = current_votes5.replace(",", "")

    votesremaining = str(int(current_votes_got) - 1)

    if (int(current_votes_got) - 1) <= 0:
        votesremaining = str(0)

    remove_uservote = "UPDATE userinfo SET votes = " + votesremaining + " WHERE username = %s"
    cursor.execute(remove_uservote, username_get)

    db.commit()

    feed_destroy()
    feed()

def generate_feed(rownum):
    get_subject = "SELECT subject FROM posts WHERE rownum = %s "
    cursor.execute(get_subject, (rownum,))
    subject = cursor.fetchone()

    subject_string = str(subject)
    subject1 = subject_string.replace("(", "")
    subject2 = subject1.replace(")", "")
    subject3 = subject2.replace("'", "")
    subject4 = subject3.replace(",", "")

    get_area = "SELECT area FROM posts WHERE rownum = %s "
    cursor.execute(get_area, (rownum,))
    area = cursor.fetchone()

    area_string = str(area)
    area1 = area_string.replace("(", "")
    area2 = area1.replace(")", "")
    area3 = area2.replace("'", "")
    area4 = area3.replace(",", "")

    get_title = "SELECT title FROM posts WHERE rownum = %s"
    cursor.execute(get_title, (rownum,))
    post_title = cursor.fetchone()

    title_string = str(post_title)
    title1 = title_string.replace("(", "")
    title2 = title1.replace(")", "")
    title3 = title2.replace("'", "")
    title4 = title3.replace(",", "")
    title5 = title4.replace('\\n', "")

    get_description = "SELECT description FROM posts WHERE rownum = %s"
    cursor.execute(get_description, (rownum,))
    post_description = cursor.fetchone()

    description_string = str(post_description)
    description1 = description_string.replace("(", "")
    description2 = description1.replace(")", "")
    description3 = description2.replace("'", "")
    description4 = description3.replace(",", "")
    description_final = description4.replace("\\n", " ")

    global post
    post = Frame(all_posts_frame, bg="white", width=700, height=157, bd=3, relief="ridge")
    post.pack(pady=15, padx=150)

    global post_background_image
    global post_background_label

    post_background_image = PhotoImage(file = "projectimages\\post_frame_background.png")
    post_background_label = Label(post, image = post_background_image, bg="white", borderwidth=0)
    post_background_label.image = post_background_image
    post_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    if subject4 == "e":
        posttype_label = Label(post, image = educationicon, bg="white", borderwidth=0)
        posttype_label.image = educationicon
        posttype_label.place(x=3, y=3)

    elif subject4 == "s":
        posttype_label = Label(post, image = safetyicon, bg="white", borderwidth=0)
        posttype_label.image = safetyicon
        posttype_label.place(x=3, y=3)

    elif subject4 == "h":
        posttype_label = Label(post, image = healthicon, bg="white", borderwidth=0)
        posttype_label.image = healthicon
        posttype_label.place(x=3, y=3)

    elif subject4 == "b":
        posttype_label = Label(post, image = businessicon, bg="white", borderwidth=0)
        posttype_label.image = businessicon
        posttype_label.place(x=3, y=3)

    else:
        posttype_label = Label(post, text=subject4, bg="white", font="none 14 bold", borderwidth=0)
        posttype_label.place(x=3, y=10)

    global arealabel
    #Writing Area in Frame
    if area4 == "l":
        arealabel = Label(post, text="Local", bg="white", font="none 12 italic")
        arealabel.place(x=40, y=18)

    if area4 == "s":
        arealabel = Label(post, text="State", bg="white", font="none 12 italic")
        arealabel.place(x=40, y=18)

    if area4 == "f":
        arealabel = Label(post, text="Federal", bg="white", font="none 12 italic")
        arealabel.place(x=40, y=18)

    #Writing Main Idea in Frame
    mainidea = Label(post, text=title5, bg="white", font="none 12 bold", wraplength = 690)
    mainidea.place(x=85, y=18)

    #writing description in frame
    description = Label(post, text=description_final, bg="white", font="none 12", wraplength = 690, anchor=W, justify=LEFT)
    description.place(x=0, y=50)

    #Upvote and Downvote buttons
    print("Votes got:")
    print(str(votes_got))

    for i in range(rownum-1, rownum):
        global agree_newrowbutton
        agree_newrowbutton = "agreebutton" + str(rownum)
        agree_newrowbutton = Button(post, image=agreeicon, text=rownum, borderwidth=0, bg="white", command=lambda name=agree_newrowbutton:agree(name))
        agree_newrowbutton.place(x=580, y=3)


    for i in range(rownum-1, rownum):
        global disagree_newrowbutton
        disagree_newrowbutton = "disagreebutton" + str(rownum)
        disagree_newrowbutton = Button(post, image=disagreeicon, text=rownum, borderwidth=0, bg="white", command=lambda name=disagree_newrowbutton:disagree(name))
        disagree_newrowbutton.place(x=660, y=3)

    if votes_got == str(0):
        agree_newrowbutton.config(state="disabled")
        disagree_newrowbutton.config(state="disabled")

    #Writing in added number of upvotes
    get_upvotes = "SELECT upvotes FROM posts WHERE rownum = %s"
    cursor.execute(get_upvotes, (rownum,))
    upvotes = cursor.fetchone()

    upvotes_string = str(upvotes)
    upvotes1 = upvotes_string.replace("(", "")
    upvotes2 = upvotes1.replace(")", "")
    upvotes3 = upvotes2.replace("'", "")
    upvotes_final = upvotes3.replace(",", "")
    print(upvotes_final)

    get_downvotes = "SELECT downvotes FROM posts WHERE rownum = %s"
    cursor.execute(get_downvotes, (rownum,))
    downvotes = cursor.fetchone()

    downvotes_string = str(downvotes)
    downvotes1 = downvotes_string.replace("(", "")
    downvotes2 = downvotes1.replace(")", "")
    downvotes3 = downvotes2.replace("'", "")
    downvotes_final = downvotes3.replace(",", "")
    print(downvotes_final)

    if upvotes_final == "None":
        print(" ")
    elif downvotes_final =="None":
        print(" ")
    else:
        global net
        net = int(upvotes_final) - int(downvotes_final)
        if net <= 0:
            net = 0

        global netlabel
        netlabel = Label(post, text=" ", bg="white", font="none 12")
        netlabel.place(x=628, y=10)
        netlabel.config(text=net)
        print("net was labeled")
        netlabel.place(x=628, y=10)

    #placing line separator
    global line
    line = PhotoImage(file = "projectimages\\line.png")

    line_label = Label(post, image=line, bg="black", borderwidth=0)
    line_label.image = line
    line_label.place(x=0, y=40)

    if subject4 == "None":
        post.destroy()
        return
    else:
        generate_feed(rownum + 1)

#the feed where users can scroll through posts
def feed():
    #Labeling top of screen with votes remaining
    global votes_remaining
    votes_remaining = Label(window, text=" ", bg="white", font="none 12 bold")
    votes_remaining.pack(pady=(245, 0), padx=(42,0))

    global votes_got
    get_user_votes = "SELECT votes FROM userinfo WHERE username = %s"
    cursor.execute(get_user_votes, username_get)
    votes_got = cursor.fetchall()
    votes_string = str(votes_got)
    votes1 = votes_string.replace("[", "")
    votes2 = votes1.replace("]", "")
    votes3 = votes2.replace("(", "")
    votes4 = votes3.replace(")", "")
    votes5 = votes4.replace("'", "")
    votes_got = votes5.replace(",", "")

    votes_remaining.config(text= votes_got + " votes remaining.")

    global main_frame
    main_frame = Frame(window, bg="white")
    main_frame.pack(fill=BOTH, expand=1, pady=(7, 0))

    feed_canvas = Canvas(main_frame, bg="white")
    feed_canvas.pack(side=LEFT, fill=BOTH, expand=1)

    feed_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=feed_canvas.yview, width=16)
    feed_scrollbar.pack(side=RIGHT, fill=Y)

    feed_canvas.configure(yscrollcommand=feed_scrollbar.set)
    feed_canvas.bind('<Configure>', lambda e: feed_canvas.configure(scrollregion = feed_canvas.bbox("all")))

    global all_posts_frame
    all_posts_frame = Frame(feed_canvas, bg="white")

    feed_canvas.create_window((0,0), window=all_posts_frame, anchor="nw")

    global educationicon
    educationicon = PhotoImage(file = "projectimages\\book.png")

    global safetyicon
    safetyicon = PhotoImage(file = "projectimages\\safety.png")

    global healthicon
    healthicon = PhotoImage(file = "projectimages\\hospital.png")

    global businessicon
    businessicon = PhotoImage(file = "projectimages\\invoice.png")

    global agreeicon
    agreeicon = PhotoImage(file = "projectimages\\correct.png")

    global disagreeicon
    disagreeicon = PhotoImage(file = "projectimages\\disagree.png")

    global commenticon
    commenticon = PhotoImage(file = "projectimages\\comment.png")

    generate_feed(1)

def creategroup():
    global creategroup_frame
    creatgroup_frame = Frame(window, bg="white")
    creategroup_frame.pack(fill=BOTH, expand=1, pady=(245, 0))

    global title_text
    title_text = Text(creategroups_frame, height=2, width=70)
    title_text.place(x=200, y=450)

    global description
    description = Text(creategroups_frame, height=5, width=70)
    description.place(x=200, y=505)

def notification():
    get_all_notifications = "SELECT notification FROM " + username_final + "notifications"

    cursor.execute(get_all_notifications)
    all_notifications = cursor.fetchall()

    get_descriptions = "SELECT text FROM " + username_final + "notifications"
    cursor.execute(get_descriptions)
    descriptions = cursor.fetchone()

    notification_string = str(notification)
    notification1 = notification_string.replace("(", "")
    notification2 = notification1.replace(")", "")
    notification3 = notification2.replace("'", "")
    notification_final= notification3.replace(",", "")

    descriptions_string = str(descriptions)
    descriptions1 = descriptions_string.replace("(", "")
    descriptions2 = descriptions1.replace(")", "")
    descriptions3 = descriptions2.replace("'", "")
    descriptions_final= descriptions3.replace(",", "")

    messagebox.showinfo("Registration Successful!", descriptions_final)

    notification_viewed = "DELETE FROM " + username_final + "notifications"

    cursor.execute(notification_viewed)

    db.commit()

    notificationbutton.config(state="disabled")

def modified_register_user():
    edited_name_get = edited_name_entered.get()
    edited_email_get = edited_email_entered.get()
    edited_username_get = edited_username_entered.get()
    edited_password_get = edited_password_entered.get()

    register_user = "INSERT INTO userinfo (name, email, username, password) VALUES (%s, %s, %s, %s)"

    cursor.execute(register_user, (edited_name_get, edited_email_get, edited_username_get, edited_password_get))

    db.commit()

    changestatus.config(text="Changes Successfully Made", fg="green")

#Verifying that the user has entered a password of a strong length
def modified_verify_password():
    global edited_password_get
    edited_password_get = edited_password_entered.get()

    if len(edited_password_get) <= 7:
        edited_password_entry.delete(0, END)
        changestatus.config(text="Please make your password strong and longer than 8 characters", fg="red")

    else:
        print(len(edited_password_get))
        modified_register_user()

#Verifying that the username entered is unique
def modified_verify_username():
    modified_verify_password()

#Verifying the email by sending a test email to the address
def modified_verify_email():
    email_get = edited_email_entered.get()

    sender_email = "votevoicenotifications@gmail.com"
    rec_email = email_get
    email_password = "<hack>cupertino2020"
    msg = MIMEText('Hello,' + """, \n \n
    Your modifications have been made to your account details as requested via the Vote Voice application \n
    If you did not request this change, contact Sannath Mathapathi at sanmathapathi@gmail.com \n
    Sincerely,
    Sannath Mathapathi
    Vote Voice """)
    msg['Subject'] = 'Vote Voice Account Details Changed'
    msg['From'] = 'votevoicenotifications@gmail.com'
    msg['To'] = email_get

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        print("Login Success")
        server.sendmail(sender_email, rec_email, msg.as_string())
        print("Email has been sent to " + rec_email)

        server.quit()

        modified_verify_username()

    except smtplib.SMTPRecipientsRefused:
        edited_email_entry.delete(0, END)
        changestatus.config(text="Email Invalid.", fg="red")

#verifying that the name and last name were actually username_entered
def modified_verify_name():
    global edited_name_get
    edited_name_get = edited_name_entered.get()

    print(len(edited_name_get))
    if len(edited_name_get) <= 1:
        edited_name_entry.delete(0, END)
        changestatus.config(text="Please enter your name.")

    else:
        modified_verify_email()

def edit_profile_destroy():
    edited_name_label.destroy()
    edited_name_entry.destroy()
    edited_email_label.destroy()
    edited_email_entry.destroy()
    edited_usernamelabel.destroy()
    edited_username_entry.destroy()
    edited_passwordlabel.destroy()
    edited_password_entry.destroy()
    applychanges.destroy()
    changestatus.destroy()

def edit_profile():

    try:
        feed_destroy()

    except:
        print(" ")

    try:
        create_post_destroy()

    except:
        print(" ")

    try:
        preview_post_destroy()

    except:
        print(" ")

    global session_background_image
    global session_background_label
    session_background_image = PhotoImage(file = "projectimages\\sessionbackground.png")
    session_background_label = Label(window, image=session_background_image)
    session_background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #Icons + Buttons for each page of the application
    global notificationicon
    notificationicon = PhotoImage(file="projectimages\\notification.png")

    global notificationbutton
    notificationbutton = Button(window, image=notificationicon, command=notification, borderwidth=0, bg="black")
    notificationbutton.place(x=255, y=240)

    notification_status = "SELECT notification FROM " + username_final + "notifications"
    cursor.execute(notification_status)
    notifications_remaining = cursor.fetchall()

    notifications_string = str(notifications_remaining)
    notifications1 = notifications_string.replace("[", "")
    notifications2 = notifications1.replace("]", "")
    notifications3 = notifications2.replace("(", "")
    notifications4 = notifications3.replace(")", "")
    notifications5 = notifications4.replace("'", "")
    notifications_final= notifications5.replace(",", "")

    print(notifications_final)
    print("Registration Successful!")

    if notifications_final == "Registration Successful!":
        print(" ")
    else:
        notificationbutton.config(state="disabled")

    global homeicon
    homeicon = PhotoImage(file="projectimages\\homeicon.png")

    homebutton = Button(window, image=homeicon, command=home, borderwidth=0, bg="black")
    homebutton.place(x=455, y=240)

    global profileicon
    profileicon = PhotoImage(file="projectimages\\user.png")

    profilebutton = Button(window, image=profileicon, command=edit_profile, borderwidth=0, bg="black")
    profilebutton.place(x=655, y=240)

    global posticon
    posticon = PhotoImage(file="projectimages\\plus.png")

    global newpostbutton
    newpostbutton = Button(window, image=posticon, command=create_post)
    newpostbutton.place(x=460, y=290)

    global edited_name_entered
    global edited_email_entered
    global edited_username_entered
    global edited_password_entered

    edited_name_entered = StringVar()
    edited_email_entered = StringVar()
    edited_username_entered = StringVar()
    edited_password_entered = StringVar()

    get_current_name = "SELECT name FROM userinfo WHERE username = %s"
    cursor.execute(get_current_name, (username_final,))
    current_name = cursor.fetchall()

    current_name_string = str(current_name)
    current_name1 = current_name_string.replace("(", "")
    current_name2 = current_name1.replace(")", "")
    current_name3 = current_name2.replace("'", "")
    current_name4 = current_name3.replace("[", "")
    current_name5 = current_name4.replace("]", "")
    current_name_final= current_name5.replace(",", "")

    global edited_name_label
    edited_name_label = Label(window, text="Name", font="none 12", bg="white")
    edited_name_label.place(x=455, y=330)

    global edited_name_entry
    edited_name_entry = Entry(window, textvariable = edited_name_entered)
    edited_name_entry.place(x=420, y=350)

    edited_name_entry.delete(0, END)
    edited_name_entry.insert(END, current_name_final)

    global edited_email_label
    edited_email_label = Label(window, text="Email", font="none 12", bg="white")
    edited_email_label.place(x=456, y=380)

    get_current_email = "SELECT email FROM userinfo WHERE username = %s"
    cursor.execute(get_current_email, (username_final,))
    current_email = cursor.fetchall()

    current_email_string = str(current_email)
    current_email1 = current_email_string.replace("(", "")
    current_email2 = current_email1.replace(")", "")
    current_email3 = current_email2.replace("'", "")
    current_email4 = current_email3.replace("[", "")
    current_email5 = current_email4.replace("]", "")
    current_email_final= current_email5.replace(",", "")

    global edited_email_entry
    edited_email_entry = Entry(window, textvariable = edited_email_entered)
    edited_email_entry.place(x=420, y=400)

    edited_email_entry.delete(0, END)
    edited_email_entry.insert(END, current_email_final)

    global edited_usernamelabel
    edited_usernamelabel = Label(window, text = "Username", font="none 12", bg="white")
    edited_usernamelabel.place(x=440, y=430)

    get_current_username = "SELECT username FROM userinfo WHERE username = %s"
    cursor.execute(get_current_username, (username_final,))
    current_username = cursor.fetchall()

    current_username_string = str(current_username)
    current_username1 = current_username_string.replace("(", "")
    current_username2 = current_username1.replace(")", "")
    current_username3 = current_username2.replace("'", "")
    current_username4 = current_username3.replace("[", "")
    current_username5 = current_username4.replace("]", "")
    current_username_final = current_username5.replace(",", "")

    global edited_username_entry
    edited_username_entry = Entry(window, textvariable = edited_username_entered)
    edited_username_entry.place(x=420, y=450)

    edited_username_entry.delete(0, END)
    edited_username_entry.insert(END, current_username_final)

    global edited_passwordlabel
    edited_passwordlabel = Label(window, text="Password", font = "none 12", bg="white")
    edited_passwordlabel.place(x=440, y=480)

    get_current_password = "SELECT password FROM userinfo WHERE username = %s"
    cursor.execute(get_current_password, (username_final,))
    current_password = cursor.fetchall()

    current_password_string = str(current_password)
    current_password1 = current_password_string.replace("(", "")
    current_password2 = current_password1.replace(")", "")
    current_password3 = current_password2.replace("'", "")
    current_password4 = current_password3.replace("[", "")
    current_password5 = current_password4.replace("]", "")
    current_password_final= current_password5.replace(",", "")

    global edited_password_entry
    edited_password_entry = Entry(window, textvariable = edited_password_entered)
    edited_password_entry.place(x=420, y=500)

    edited_password_entry.delete(0, END)
    edited_password_entry.insert(END, current_password_final)

    global applychanges
    applychanges = Button(window, text="Apply Changes", command=modified_verify_name)
    applychanges.place(x=435, y=530)

    global changestatus
    changestatus = Label(window, text=" ", bg="white", font="none 12")
    changestatus.place(x=390, y=570)

    profilebutton.config(state="disabled")

#the home screen where users can move through their feed or create posts
def home():
    try:
        create_post_destroy()

    except:
        print(" ")

    try:
        preview_post_destroy()
    except:
        print(" ")

    try:
        edit_profile_destroy()

    except:
        print(" ")

    global session_background_image
    global session_background_label
    session_background_image = PhotoImage(file = "projectimages\\sessionbackground.png")
    session_background_label = Label(window, image=session_background_image)
    session_background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #Icons + Buttons for each page of the application
    global notificationicon
    notificationicon = PhotoImage(file="projectimages\\notification.png")

    global notificationbutton
    notificationbutton = Button(window, image=notificationicon, command=notification, borderwidth=0, bg="black")
    notificationbutton.place(x=255, y=240)

    notification_status = "SELECT notification FROM " + username_final + "notifications"
    cursor.execute(notification_status)
    notifications_remaining = cursor.fetchall()

    notifications_string = str(notifications_remaining)
    notifications1 = notifications_string.replace("[", "")
    notifications2 = notifications1.replace("]", "")
    notifications3 = notifications2.replace("(", "")
    notifications4 = notifications3.replace(")", "")
    notifications5 = notifications4.replace("'", "")
    notifications_final= notifications5.replace(",", "")

    print(notifications_final)
    print("Registration Successful!")

    if notifications_final == "Registration Successful!":
        print(" ")
    else:
        notificationbutton.config(state="disabled")

    global homeicon
    homeicon = PhotoImage(file="projectimages\\homeicon.png")

    homebutton = Button(window, image=homeicon, command=home, borderwidth=0, bg="black")
    homebutton.place(x=455, y=240)

    global profileicon
    profileicon = PhotoImage(file="projectimages\\user.png")

    profilebutton = Button(window, image=profileicon, command=edit_profile, borderwidth=0, bg="black")
    profilebutton.place(x=655, y=240)

    global posticon
    posticon = PhotoImage(file="projectimages\\plus.png")

    global newpostbutton
    newpostbutton = Button(window, image=posticon, command=create_post)
    newpostbutton.place(x=460, y=290)

    homebutton.config(state = "disabled")

    feed()

#session that starts after every login
def session():
    #Remembering the user's details throughout the session
    global username_final
    username_string = str(username_get)
    username1 = username_string.replace("(", "")
    username2 = username1.replace(")", "")
    username3 = username2.replace("'", "")
    username_final = username3.replace(",", "")

    #Rather than creating new windows for every task, clearing the screen to keep things consistent
    background_label.destroy()
    open_loginbutton.destroy()
    open_registrationbutton.destroy()
    usernamelabel.destroy()
    username_entry.destroy()
    passwordlabel.destroy()
    password_entry.destroy()
    loginbutton.destroy()
    loginstatus.destroy()
    change_register.destroy()

    #Making the background image
    global session_background_image
    global session_background_label
    session_background_image = PhotoImage(file = "projectimages\\sessionbackground.png")
    session_background_label = Label(window, image=session_background_image)
    session_background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #Icons + Buttons for each page of the application
    home()

#if username not recognized
def user_not_found():
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    loginstatus.config(text="Username not recognized.", fg="red")

#if password not recognized
def password_not_found():
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    loginstatus.config(text="Password not recognized", fg="red")

#if both username and password are accurate, begin session
def login_success():
    give_votes = "UPDATE userinfo SET votes = 3 WHERE username = %s"
    cursor.execute(give_votes, username_get)
    db.commit()

    session()

#verifying the user logged in with accurate credentials
def login_verify():
    global username_get
    username_get = (username_entered.get(),)

    password_get = password_entered.get()
    username_search = "SELECT password FROM userinfo WHERE username = %s"
    cursor.execute(username_search, username_get)

    password_returned = cursor.fetchall()

    if len(password_returned) == 0:
        user_not_found()
    else:
        password_string = str(password_returned)
        password_replace1 = password_string.replace("'", "")
        password_replace2 = password_replace1.replace("(", "")
        password_replace3 = password_replace2.replace(")", "")
        password_replace4 = password_replace3.replace("[", "")
        password_replace5 = password_replace4.replace("]","")
        password_final = password_replace5.replace(",", "")
        if password_final == password_get:
            login_success()
        else:
            password_not_found()

#opening login screen
def open_login():
    try:
        open_loginbutton.destroy()
        open_registrationbutton.destroy()
        instructionslabel.destroy()
        firstnamelabel.destroy()
        firstname_entry.destroy()
        lastnamelabel.destroy()
        lastname_entry.destroy()
        emaillabel.destroy()
        email_entry.destroy()
        registration_usernamelabel.destroy()
        registration_username_entry.destroy()
        registration_passwordlabel.destroy()
        registration_password_entry.destroy()
        registerbutton.destroy()
        change_login.destroy()
        registration_status.destroy()
    except:
        print(" ")

    global username_entered
    global password_entered

    username_entered = StringVar()
    password_entered = StringVar()

    global usernamelabel
    usernamelabel = Label(window, text = "Username", font="none 12", bg="white")
    usernamelabel.place(x=440, y=70)

    global username_entry
    username_entry = Entry(window, textvariable = username_entered)
    username_entry.place(x=420, y=100)

    global passwordlabel
    passwordlabel = Label(window, text="Password", font = "none 12", bg="white")
    passwordlabel.place(x=440, y=120)

    global password_entry
    password_entry = Entry(window, textvariable = password_entered)
    password_entry.place(x=420, y=150)

    global loginbutton
    loginbutton = Button(window, text="Login", width=10, height=1, command=login_verify, bg="white")
    loginbutton.place(x=435, y=180)

    global change_register
    change_register = Button(window, text="New User?", width=10, command=open_registration, bg="white")
    change_register.place(x=435, y=210)

    global loginstatus
    loginstatus = Label(window, text = " ", bg="white")
    loginstatus.place(x=407, y=235)
def register_user():
    firstname_get = firstname.get()
    lastname_get = lastname.get()
    email_get = email.get()
    username_get = username.get()
    password_get = password.get()

    register_user = "INSERT INTO userinfo (name, email, username, password) VALUES (%s, %s, %s, %s)"

    cursor.execute(register_user, (firstname_get + lastname_get, email_get, username_get, password_get))

    db.commit()

    notifications_table = "CREATE TABLE " + username_get + "notifications (notification VARCHAR(255), text VARCHAR(255))"

    cursor.execute(notifications_table)

    db.commit()

    first_notification = "INSERT INTO " + username_get + "notifications (notification, text) VALUES (%s, %s)"
    first_notification_msg = ("Registration Successful!", "Congratulations on signing up for Vote Voice! Hopefully this will serve as a platform for you to express yourself and make change on the level you choose!")
    cursor.execute(first_notification, first_notification_msg)

    db.commit()

    registration_status.config(text="Registration Success", fg="green")

#Verifying that the user has entered a password of a strong length
def verify_password():
    global password_get
    password_get = password.get()

    if len(password_get) <= 7:
        print(len(password_get))
        registration_password_entry.delete(0, END)
        registration_status.config(text="Please make your password strong and longer than 8 characters", fg="red")

    else:
        print(len(password_get))
        register_user()

#Verifying that the username entered is unique
def verify_username():
    global username_get
    username_get = username.get()

    username_tuple = (username_get,)

    username_taken = "SELECT name FROM userinfo WHERE username = %s"

    cursor.execute(username_taken, username_tuple)

    username_match = cursor.fetchall()

    if len(username_match) == 0:
        verify_password()

    else:
        print(len(username_match))
        registration_username_entry.delete(0, END)
        registration_password_entry.delete(0, END)
        registration_status.config(text="Username has been taken.", fg="red")

#Verifying the email by sending a test email to the address
def verify_email():
    email_get = email.get()

    sender_email = "votevoicenotifications@gmail.com"
    rec_email = email_get
    email_password = "<hack>cupertino2020"
    msg = MIMEText('Dear ' + firstname_get + " " + lastname_get + """, \n \n
    Congratulations on signing up for the Vote Voice application! \n
    The app will serve as a platform for you and members of your community to make the change you want to see. \n
    This email address will serve as a notification system for your account; please disable notifications and change your email if you would like. \n
    Sincerely,
    Sannath Mathapathi
    Vote Voice """)
    msg['Subject'] = 'Vote Voice Registration Success'
    msg['From'] = 'votevoicenotifications@gmail.com'
    msg['To'] = email_get

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, email_password)
        print("Login Success")
        server.sendmail(sender_email, rec_email, msg.as_string())
        print("Email has been sent to " + rec_email)

        server.quit()

        verify_username()

    except smtplib.SMTPRecipientsRefused:
        email_entry.delete(0, END)
        registration_status.config(text="Email Invalid.", fg="red")

#verifying that the name and last name were actually username_entered
def verify_name():
    global firstname_get
    firstname_get = firstname.get()

    if len(firstname_get) == 0:
        registration_status.config(text="Please fill out all required fields")

    else:
        global lastname_get
        lastname_get = lastname.get()
        if len(lastname_get) == 0:
            registration_status.config(text="Please fill out all required fields")
        else:
            verify_email()

#Opening registration screen
def open_registration():
    try:
        open_loginbutton.destroy()
        open_registrationbutton.destroy()
        usernamelabel.destroy()
        username_entry.destroy()
        passwordlabel.destroy()
        password_entry.destroy()
        loginbutton.destroy()
        loginstatus.destroy()
        change_register.destroy()

    except:
        print(" ")

    global firstname
    global lastname
    global email
    global username
    global password

    global firstname_entry
    global lastname_entry
    global email_entry
    global registration_username_entry
    global registration_password_entry

    firstname = StringVar()
    lastname = StringVar()
    email = StringVar()
    username = StringVar()
    password = StringVar()

    global instructionslabel
    instructionslabel = Label(window, text = "Please enter the following details to register.", font="none 12 bold", bg="white")
    instructionslabel.place(x=320, y=75)

    global firstnamelabel
    firstnamelabel = Label(window, text="First Name", font="none 12", bg="white")
    firstnamelabel.place(x=370, y=100)

    global firstname_entry
    firstname_entry = Entry(window, textvariable = firstname)
    firstname_entry.place(x=350, y=125)

    global lastnamelabel
    lastnamelabel = Label(window, text="Last Name", font="none 12", bg="white")
    lastnamelabel.place(x=370, y=150)

    global lastname_entry
    lastname_entry = Entry(window, textvariable = lastname)
    lastname_entry.place(x=350, y=175)

    global emaillabel
    emaillabel = Label(window, text="Email", font="none 12", bg="white")
    emaillabel.place(x=385, y=200)

    global email_entry
    email_entry = Entry(window, textvariable = email)
    email_entry.place(x=350, y=225)

    global registration_usernamelabel
    registration_usernamelabel = Label(window, text="Username", font="none 12", bg="white")
    registration_usernamelabel.place(x=510, y=100)

    global registration_username_entry
    registration_username_entry = Entry(window, textvariable = username)
    registration_username_entry.place(x=490, y=125)

    global registration_passwordlabel
    registration_passwordlabel = Label(window, text="Password", font="none 12", bg="white")
    registration_passwordlabel.place(x=510, y=150)

    global registration_password_entry
    registration_password_entry = Entry(window, textvariable = password)
    registration_password_entry.place(x=490, y=175)

    global registerbutton
    registerbutton = Button(window, text="Register", width=10, height=1, command=verify_name, bg="white")
    registerbutton.place(x=510, y=200)

    global change_login
    change_login = Button(window, text="Login", width=10, height=1, command=open_login, bg="white")
    change_login.place(x=510, y=235)

    global registration_status
    registration_status = Label(window, text=" ", bg="white")
    registration_status.place(x=390, y=265)

#Creating a window for the starting screen
window = Tk()
window.title("VoteVoice")
window.geometry('960x720')
window.resizable(width='False', height='False')

#Making the background image
global background_label
background_image = PhotoImage(file = "projectimages\\background.png")
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

logo = PhotoImage(file = "projectimages\\logo.png")
logo_label = Label(window, image=logo, bg="white")
logo_label.pack()

open_loginbutton = Button(text="Login", width=20, command=open_login)
open_loginbutton.pack(pady=15)
open_registrationbutton = Button(window, text="New User?", width=20, command=open_registration)
open_registrationbutton.pack()


window.mainloop()
