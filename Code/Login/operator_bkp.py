from tkinter import *
from tkinter import ttk

import tkinter as tk

import warnings

from numpy import select
warnings.filterwarnings("ignore")
import webbrowser
import sqlite3

import time

# ==================================================================================
# Database initialization: 
# ==================================================================================
conn = sqlite3.connect("bikesharedatabase.db")

with conn as db:
    cursor = db.cursor()

# ==================================================================================
# Tkinter:
# ==================================================================================
window = Tk()
window.title('Operator View')
window.geometry("1500x800")

# Creating tabs:
allTabs = ttk.Notebook(window)

track_tab = Frame(allTabs)
repair_tab = Frame(allTabs)
move_tab = Frame(allTabs)

allTabs.add(track_tab, text = "Track Bike")
allTabs.add(repair_tab, text = "Repair Bike")
allTabs.add(move_tab, text = "Move Bike")
allTabs.pack(expand = 1, fill = "both")

# 1. Display bike coordinates in table:
track_button_frame = LabelFrame(track_tab)
bike_track_frame = Frame(track_tab)
bike_track_scroll = Scrollbar(bike_track_frame)
bike_track_tree = ttk.Treeview(bike_track_frame, yscrollcommand = bike_track_scroll.set, selectmode = "extended")

# 2. Display bike information from defect table:
repair_button_frame = LabelFrame(repair_tab)
bike_repair_frame = Frame(repair_tab)
bike_repair_scroll = Scrollbar(bike_repair_frame)
bike_repair_tree = ttk.Treeview(bike_repair_frame, yscrollcommand = bike_repair_scroll.set, selectmode = "extended")

# 3. Display information of all bikes in bike_status, along with a dropdown that shows only relevant target stations for a selected bike:
move_button_frame = LabelFrame(move_tab)
bike_move_frame = Frame(move_tab)
bike_move_scroll = Scrollbar(bike_move_frame)
bike_move_tree = ttk.Treeview(bike_move_frame, yscrollcommand = bike_move_scroll.set, selectmode = "extended")

# ttk style configurations:
style = ttk.Style()
style.configure("Treeview", background = "0c88cc", foreground = "black", rowheight = 35, fieldbackground = "0c88cc")
style.map("Treeview", background = [("selected", "#0c88cc")], foreground = [("selected", "white")], font = [("selected", ("Helvetica", 16))])



# TODO: 
# 1. Implement bike_move_details()
# 2. Implement move



# ==================================================================================
# Tkinter widget functions:
# ==================================================================================

# 1. Function to load data from table track_location onto bike track tab:
def bike_location_details():
    bike_location_query="""SELECT bike_id, latitude, longitude 
                        FROM track_location"""
    
    bike_location_details = cursor.execute(bike_location_query) 

    # User table frame
    bike_track_frame.place(x=20, y=55, width=800, height=190)
    bike_track_scroll.pack(side=RIGHT, fill=Y)
    bike_track_tree.place(x=20, y=25, width=800, height=190)
    bike_track_scroll.config(command = bike_track_tree.yview)
    bike_track_tree['columns'] = ("Bike ID", "Latitude", "Longitude")
    bike_track_tree.column("#0", width = 0, stretch = NO)
    bike_track_tree.column("Bike ID", anchor=W, width=200)
    bike_track_tree.column("Latitude", anchor=W, width=200)
    bike_track_tree.column("Longitude", anchor=W, width=200)
    bike_track_tree.heading("#0", text = "", anchor = W)
    bike_track_tree.heading("Bike ID", text = "Bike ID", anchor = W)
    bike_track_tree.heading("Latitude", text = "Latitude", anchor = W)
    bike_track_tree.heading("Longitude", text = "Longitude", anchor = W)
    bike_track_tree.tag_configure('evenrow', background = '#E2F0CB')
    bike_track_tree.tag_configure('oddrow', background = '#B5EAD7')
    
    # Populate bike_track_tree with bike_location_details
    global count
    count = 0
    for record in bike_location_details:
        if count % 2 == 0:
            bike_track_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1].upper(), record[2].upper()), tags=('evenrow',))
        else:
            bike_track_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1].upper(), record[2].upper()), tags=('oddrow',))
        count +=1

# Function to use data from the selected entry in the track_location table:
def select_track_bike(e):   
    track_button["text"] = "Track Location"
    track_button["fg"] = "green"
    
    track_button_frame.place(x = 1020, y = 75, width = 350, height = 170)
    track_button.place(x = 1020, y = 500)    
    track_button.pack()

# Function to load the Google Maps webpage when the "Track Bike" button is pressed for a selected bike:
def track_location():
    selected = bike_track_tree.focus()
    values = bike_track_tree.item(selected, 'values')
    # Generate URL to load location on maps:
    latitude = values[1]
    longitude = values[2]

    webbrowser.open('https://maps.google.com/?q=' + str(latitude) + ',' + str(longitude))

# Function to load data from table defect onto the repair tab:
def bike_repair_details():
    bike_repair_query = """select b.bike_number, s.station_name, d.defect_remarks, d.defect_found_time, d.defect_status, d.id from 
    (select * from defect) d
    left join 
    (select * from bike) b
    on d.bike_id = b.id
    left join
    (select * from station) s
    on d.station_id = s.id
    ORDER BY d.defect_status DESC"""
    
    bike_repair_details = cursor.execute(bike_repair_query) 
    
    # User table frame
    bike_repair_frame.place(x = 20, y = 55, width = 1000, height = 190)
    bike_repair_scroll.pack(side = RIGHT, fill = Y)
    bike_repair_tree.place(x = 20, y = 25, width = 1000, height = 190)
    bike_repair_scroll.config(command = bike_repair_tree.yview)
    bike_repair_tree['columns'] = ("Bike Number", "Station Name", "Defect Remarks", "Defect Found Time", "Defect Status", "Defect ID")
    bike_repair_tree.column("#0", width = 0, stretch = NO)
    bike_repair_tree.column("Bike Number", anchor = W, width = 200)
    bike_repair_tree.column("Station Name", anchor = W, width = 200)
    bike_repair_tree.column("Defect Remarks", anchor = W, width = 200)
    bike_repair_tree.column("Defect Found Time", anchor = W, width = 200)
    bike_repair_tree.column("Defect Status", anchor = W, width = 200)
    bike_repair_tree.column("Defect ID", anchor = W, width = 200)
    bike_repair_tree.heading("#0", text = "", anchor = W)
    bike_repair_tree.heading("Bike Number", text = "Bike Number", anchor = W)
    bike_repair_tree.heading("Station Name", text = "Station Name", anchor = W)
    bike_repair_tree.heading("Defect Remarks", text = "Defect Remarks", anchor = W)
    bike_repair_tree.heading("Defect Found Time", text = "Defect Found Time", anchor = W)
    bike_repair_tree.heading("Defect Status", text = "Defect Status", anchor = W)
    bike_repair_tree.heading("Defect ID", text = "Defect ID", anchor = W)
    bike_repair_tree.tag_configure('evenrow', background = '#E2F0CB')
    bike_repair_tree.tag_configure('oddrow', background = '#B5EAD7')
    
    # Populate bike_track_tree with bike_location_details
    global count
    count = 0
    for record in bike_repair_details:
        if count % 2 == 0:
            bike_repair_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
        else:
            bike_repair_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
        count +=1

# Function to select a bike in the table on the repair tab and extract its values: 
def select_repair_bike(e):
    selected = bike_repair_tree.focus()
    values = bike_repair_tree.item(selected, 'values')
    repair_button["fg"] = "green"
    
    current_d_id = values[5]
    
    print("Current defect id: ", current_d_id)
    # Generate URL to load location on maps:
    defect_status = values[4]
    print("Current defect status: ", defect_status)
    
    if defect_status == "open":
        # Button should have "in-progress" functionality
        repair_button["text"] = "Start Repair" 
        repair_button_frame.place(x = 1020, y = 75, width = 350, height = 170)
        repair_button.config(fg='black')
        repair_button.place(x = 1020, y = 500)    
        repair_button.pack()
    elif defect_status == "inprogress":
        repair_button["text"] = "Close Repair"
        repair_button_frame.place(x = 1020, y = 75, width = 350, height = 170)
        repair_button.config(fg='black')
        repair_button.place(x = 1020, y = 500)    
        repair_button.pack()
    elif defect_status == "closed":
        repair_button.place_forget()
        repair_button.place(x = 10000, y = 10000)

# Function to make changes to table defect once the repair button is pressed for a selected bike:
def repair():
    selected = bike_repair_tree.focus()
    values = bike_repair_tree.item(selected, 'values')
    current_status = values[4]
    current_d_id = values[5]

    if current_status == "open":
        inprogress_query = """UPDATE defect
            SET defect_status=?
            WHERE id=?"""
        cursor.execute(inprogress_query, ("inprogress", current_d_id))
        conn.commit()

    elif current_status == "inprogress":
        current_status = "closed"
        popupwin(values)
        
    elif current_status == "closed":
        repair_button["text"] = ""
        repair_button.forget_place()
        repair_button.forget_pack()

    clear_bike_repair_tree()
    bike_repair_details()
    repair_button.event_generate("<ButtonRelease-1>")

#Define a function to close the popup window
def close_win(top):
   top.destroy()

def insert_val(top, val1, val2, values):
    top.destroy()
    current_d_id = values[5]

    closed_query = """UPDATE defect
    SET defect_status=?, repair_cost=?, repair_remarks=?
    WHERE id=?"""
    
    update_bike_status_query = """UPDATE bike_status
    SET is_defect=?
    WHERE id=?"""
    
    cursor.execute(closed_query, ("closed", val1, val2, current_d_id))
    cursor.execute(update_bike_status_query, (0, values[0]))
    conn.commit()

    clear_bike_repair_tree()
    bike_repair_details()
    repair_button_frame.place(x = 1000000, y = 1000000)

    repair_button.event_generate("<ButtonRelease-1>")

#Define a function to open the Popup Dialogue
def popupwin(values):
    #Create a Toplevel window
    top = Toplevel(window)
    top.geometry("750x250")

    #Create an Entry Widget in the Toplevel window
    entry_label_text = StringVar()
    entry_label_text.set("Repair Cost")
    entry_label = Label(top, textvariable = entry_label_text, height = 1)
    entry2_label_text = StringVar()
    entry2_label_text.set("Repair Remarks")
    entry2_label = Label(top, textvariable = entry2_label_text, height = 1)
    entry= Entry(top, width = 25)
    entry2 = Entry(top, width = 25)
    entry_label.place(x = 10, y = 10)
    entry2_label.place(x = 10, y = 70)
    entry.place(x = 200, y = 10)
    entry2.place(x = 200, y = 70)


    #Create a Button Widget in the Toplevel Window
    button= Button(top, text="Submit", command = lambda:insert_val(top, entry.get(), entry2.get(), values))
    button.place(x = 170, y = 150)

# Function to clear the data in the repair tab's table such that newly updated data can be loaded:
def clear_bike_repair_tree():
    for item in bike_repair_tree.get_children():
        bike_repair_tree.delete(item)


# Function to load move bike details on the move bike tab:
def bike_move_details():
    # Get data from the bike_status table:
    bike_move_details = cursor.execute("SELECT bike_id, type, bike_number, station_name, station_id from v_bike_status") 
    
    # User table frame
    bike_move_frame.place(x = 20, y = 55, width = 1000, height = 190)
    bike_move_scroll.pack(side = RIGHT, fill = Y)
    bike_move_tree.place(x = 20, y = 25, width = 1000, height = 190)
    bike_move_scroll.config(command = bike_move_tree.yview)
    bike_move_tree['columns'] = ("Bike ID", "Bike Type", "Bike Number", "Station Name", "Station ID")
    bike_move_tree.column("#0", width = 0, stretch = NO)
    bike_move_tree.column("Bike ID", anchor = W, width = 200)
    bike_move_tree.column("Bike Type", anchor = W, width = 200)
    bike_move_tree.column("Bike Number", anchor = W, width = 200)
    bike_move_tree.column("Station Name", anchor = W, width = 200)
    bike_move_tree.column("Station ID", anchor = W, width = 200)
    bike_move_tree.heading("#0", text = "", anchor = W)
    bike_move_tree.heading("Bike ID", text = "Bike ID", anchor = W)
    bike_move_tree.heading("Bike Type", text = "Bike Type", anchor = W)
    bike_move_tree.heading("Bike Number", text = "Bike Number", anchor = W)
    bike_move_tree.heading("Station Name", text = "Station Name", anchor = W)
    bike_move_tree.heading("Station ID", text = "Station ID", anchor = W)
    bike_move_tree.tag_configure('evenrow', background = '#E2F0CB')
    bike_move_tree.tag_configure('oddrow', background = '#B5EAD7')
    
    # Populate bike_track_tree with bike_location_details
    global count
    count = 0
    for record in bike_move_details:
        if count % 2 == 0:
            bike_move_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
        else:
            bike_move_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
        count +=1

dropdown_list = [0]
target_station_type = StringVar(move_tab)
target_station_type.set("Select Target Station")
move_button_frame.place(x = 1020, y = 75, width = 350, height = 170)
opt1 = OptionMenu(move_button_frame, target_station_type, *dropdown_list)


def refresh(new_list):
    target_station_type.set("Select Target Station")
    opt1['menu'].delete(0, 'end')

    for each in new_list:
        opt1['menu'].add_command(label = each, command = tk._setit(target_station_type, each))


def select_move_bike(e):
    cursor.execute("select station_id, station_name, available_rack_count from v_available_bike_rack")
    available_rack_details =  cursor.fetchall()

    # Get the current selected row:
    selected = bike_move_tree.focus()
    values = bike_move_tree.item(selected, 'values')

    current_station_id = values[4]
    initial_station_id = current_station_id
    current_bike_id = values[0]


    dropdown_list = []

    # Check if this station_id has any available racks:
    for each in available_rack_details:
        if each[0] != int(current_station_id) and each[2] > 0:
            # Populate list with this element:
            dropdown_list.append(each[1])

    opt1.pack_forget()
    refresh(dropdown_list)
    opt1.place(x = 1020,y = 500)
    opt1.pack()

    #To trace the change in dropdown box's value. w = write mode
    target_station_type.trace("w", find_term)


#Function to retrieve value from dropbox in tab2  
def find_term(*args):
    # target_station_type.get() gets the data in the dropdown
    # target_station = target_station_type.get()

    # cursor.execute("select station_name, station_id from v_available_bike_rack")
    # station_data = cursor.fetchall()

    # print(station_data)

    # # Get the id of target station:
    # current_id = -1
    # for each in station_data:
    #     if each[0] == target_station:
    #         print(each)
    #         current_id = each[1]
    #         break
    
    # if current_id == -1:
    #     print("Couldn't find station id for given station in database.")

    # final_station_id = current_id

    move_button.pack_forget()
    move_button["text"] = "Move Bike"
    move_button["fg"] = "black"
    move_button.place(x = 1020, y = 550)
    move_button.pack()

def move():
    # Update bike_status, move_location
    # In bike_status, change station_id for given bike_id
    # In move_location, add an entry with bike_id, initial_station_id, final_station_id, and current_system_time
    
    selected = bike_move_tree.focus()
    values = bike_move_tree.item(selected, 'values')
    current_bike_id = values[0]
    current_station_id = values[4]
    final_station_name = target_station_type.get()
    final_station_id = -1
    
    cursor.execute("select station_name, station_id from v_available_bike_rack")
    station_data = cursor.fetchall()

    for each in station_data:
        if each[0] == final_station_name:
            final_station_id = each[1]
            break
    
    if final_station_id != -1:
        bike_status_query = ('''UPDATE bike_status   
                SET station_id=?
                WHERE bike_id=?;''')
        cursor.execute(bike_status_query, (final_station_id, current_bike_id))

        move_location_query = ('''INSERT INTO move_location (from_station_id, to_station_id, created_time) 
        VALUES(?, ?, ?);''')
        cursor.execute(move_location_query, (current_station_id, final_station_id, time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())))
        conn.commit()

        clear_bike_move_tree()
        bike_move_details()
        move_button.event_generate("<ButtonRelease-1>")

    # Refresh the move_bike TreeView

def clear_bike_move_tree():
    for item in bike_move_tree.get_children():
        bike_move_tree.delete(item)


track_button = Button(track_button_frame, command = track_location, bg = "blue", fg = "black", height = 2, width = 15)
repair_button = Button(repair_button_frame, command = repair, bg = "blue", fg = "black", height = 2, width = 15)
move_button = Button(move_button_frame, command = move, bg = "blue", fg = "black", height =  2, width = 15)

bike_track_tree.bind("<ButtonRelease-1>", select_track_bike)
bike_repair_tree.bind("<ButtonRelease-1>", select_repair_bike)
bike_move_tree.bind("<ButtonRelease-1>", select_move_bike)

bike_location_details()
bike_repair_details()
bike_move_details()

window.mainloop()
db.close()






