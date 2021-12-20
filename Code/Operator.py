"""
@author Akib
"""

from tkinter import *
from tkinter import ttk

import tkinter as tk

import warnings

warnings.filterwarnings("ignore")
import webbrowser
import sqlite3

import time

class Operator:
    def __init__(self):
        with sqlite3.connect("bikesharedatabase.db") as db:
            self.cursor = db.cursor()
            self.db = db
            #self.parent = parent

    # TODO: 
        # 1. Implement bike_move_details()
        # 2. Implement move



    # ==================================================================================
    # Tkinter widget functions:
    # ==================================================================================

    # 1. Function to load data from table track_location onto bike track tab:
    def bike_location_details(self):
        bike_location_query="""SELECT bike_number, latitude, longitude 
                            FROM v_bike_status"""
        
        bike_location_details = self.cursor.execute(bike_location_query) 

        # User table frame
        self.bike_track_frame.place(x=20, y=55, width=800, height=190)
        self.bike_track_scroll.pack(side=RIGHT, fill=Y)
        self.bike_track_tree.place(x=20, y=25, width=800, height=190)
        self.bike_track_scroll.config(command = self.bike_track_tree.yview)
        self.bike_track_tree['columns'] = ("Bike Number", "Latitude", "Longitude")
        self.bike_track_tree.column("#0", width = 0, stretch = NO)
        self.bike_track_tree.column("Bike Number", anchor=W, width=200)
        self.bike_track_tree.column("Latitude", anchor=W, width=200)
        self.bike_track_tree.column("Longitude", anchor=W, width=200)
        self.bike_track_tree.heading("#0", text = "", anchor = W)
        self.bike_track_tree.heading("Bike Number", text = "Bike Number", anchor = W)
        self.bike_track_tree.heading("Latitude", text = "Latitude", anchor = W)
        self.bike_track_tree.heading("Longitude", text = "Longitude", anchor = W)
        self.bike_track_tree.tag_configure('evenrow', background = '#E2F0CB')
        self.bike_track_tree.tag_configure('oddrow', background = '#B5EAD7')
        
        # Populate bike_track_tree with bike_location_details
        global count
        count = 0
        for record in bike_location_details:
            if count % 2 == 0:
                self.bike_track_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1].upper(), record[2].upper()), tags=('evenrow',))
            else:
                self.bike_track_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1].upper(), record[2].upper()), tags=('oddrow',))
            count +=1

    # Function to use data from the selected entry in the track_location table:
    def select_track_bike(self, e):   
        self.track_button["text"] = "Track Location"
        self.track_button["fg"] = "white"
        self.track_button["bg"] = "#4091c2"

        self.track_button_frame.place(x = 1020, y = 75, width = 350, height = 170)
        self.track_button.place(x = 1020, y = 500)    
        self.track_button.pack()

    # Function to load the Google Maps webpage when the "Track Bike" button is pressed for a selected bike:
    def track_location(self):
        selected = self.bike_track_tree.focus()
        values = self.bike_track_tree.item(selected, 'values')
        # Generate URL to load location on maps:
        latitude = values[1]
        longitude = values[2]

        webbrowser.open('https://maps.google.com/?q=' + str(latitude) + ',' + str(longitude))

    # Function to load data from table defect onto the repair tab:
    def bike_repair_details(self):
        bike_repair_query = """select b.bike_number, s.station_name, d.defect_remarks, d.defect_found_time, d.defect_status, d.id from 
        (select * from defect) d
        left join 
        (select * from bike) b
        on d.bike_id = b.id
        left join
        (select * from station) s
        on d.station_id = s.id
        ORDER BY d.defect_status DESC"""
        
        bike_repair_details = self.cursor.execute(bike_repair_query) 
        
        # User table frame
        self.bike_repair_frame.place(x = 20, y = 55, width = 1000, height = 190)
        self.bike_repair_scroll.pack(side = RIGHT, fill = Y)
        self.bike_repair_tree.place(x = 20, y = 25, width = 1000, height = 190)
        self.bike_repair_scroll.config(command = self.bike_repair_tree.yview)
        self.bike_repair_tree['columns'] = ("Bike Number", "Station Name", "Defect Remarks", "Defect Found Time", "Defect Status", "Defect ID")
        self.bike_repair_tree.column("#0", width = 0, stretch = NO)
        self.bike_repair_tree.column("Bike Number", anchor = W, width = 200)
        self.bike_repair_tree.column("Station Name", anchor = W, width = 200)
        self.bike_repair_tree.column("Defect Remarks", anchor = W, width = 200)
        self.bike_repair_tree.column("Defect Found Time", anchor = W, width = 200)
        self.bike_repair_tree.column("Defect Status", anchor = W, width = 200)
        self.bike_repair_tree.column("Defect ID", anchor = W, width = 200)
        self.bike_repair_tree.heading("#0", text = "", anchor = W)
        self.bike_repair_tree.heading("Bike Number", text = "Bike Number", anchor = W)
        self.bike_repair_tree.heading("Station Name", text = "Station Name", anchor = W)
        self.bike_repair_tree.heading("Defect Remarks", text = "Defect Remarks", anchor = W)
        self.bike_repair_tree.heading("Defect Found Time", text = "Defect Found Time", anchor = W)
        self.bike_repair_tree.heading("Defect Status", text = "Defect Status", anchor = W)
        self.bike_repair_tree.heading("Defect ID", text = "Defect ID", anchor = W)
        self.bike_repair_tree.tag_configure('evenrow', background = '#E2F0CB')
        self.bike_repair_tree.tag_configure('oddrow', background = '#B5EAD7')
        
        # Populate bike_track_tree with bike_location_details
        global count
        count = 0
        for record in bike_repair_details:
            if count % 2 == 0:
                self.bike_repair_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
            else:
                self.bike_repair_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
            count +=1

    # Function to select a bike in the table on the repair tab and extract its values: 
    def select_repair_bike(self, e):
        selected = self.bike_repair_tree.focus()
        values = self.bike_repair_tree.item(selected, 'values')
        self.repair_button["fg"] = "white"
        
        current_d_id = values[5]
        
        print("Current defect id: ", current_d_id)
        # Generate URL to load location on maps:
        defect_status = values[4]
        print("Current defect status: ", defect_status)
        
        if defect_status == "open":
            # Button should have "in-progress" functionality
            self.repair_button["text"] = "Start Repair" 
            self.repair_button_frame.place(x = 1020, y = 75, width = 350, height = 170)
            self.repair_button.config(fg='white')
            self.repair_button.place(x = 1020, y = 500)    
            self.repair_button.pack()
        elif defect_status == "inprogress":
            self.repair_button["text"] = "Close Repair"
            self.repair_button_frame.place(x = 1020, y = 75, width = 350, height = 170)
            self.repair_button.config(fg='white')
            self.repair_button.place(x = 1020, y = 500)    
            self.repair_button.pack()
        elif defect_status == "closed":
            self.repair_button.place_forget()
            self.repair_button.place(x = 10000, y = 10000)

    # Function to make changes to table defect once the repair button is pressed for a selected bike:
    def repair(self):
        selected = self.bike_repair_tree.focus()
        values = self.bike_repair_tree.item(selected, 'values')
        current_status = values[4]
        current_d_id = values[5]

        if current_status == "open":
            inprogress_query = """UPDATE defect
                SET defect_status=?
                WHERE id=?"""
            self.cursor.execute(inprogress_query, ("inprogress", current_d_id))
            self.db.commit()

        elif current_status == "inprogress":
            current_status = "closed"
            self.popupwin(values)
            
        elif current_status == "closed":
            self.repair_button["text"] = ""
            self.repair_button.forget_place()
            self.repair_button.forget_pack()

        self.clear_bike_repair_tree()
        self.bike_repair_details()
        self.repair_button.event_generate("<ButtonRelease-1>")

    #Define a function to close the popup window
    def close_win(self, top):
        top.destroy()

    def insert_val(self, top, val1, val2, values):
        top.destroy()
        current_d_id = values[5]

        closed_query = """UPDATE defect
        SET defect_status=?, repair_cost=?, repair_remarks=?
        WHERE id=?"""
        
        update_bike_status_query = """UPDATE bike_status
        SET is_defect=?
        WHERE id=?"""
        
        self.cursor.execute(closed_query, ("closed", val1, val2, current_d_id))
        self.cursor.execute(update_bike_status_query, (0, values[0]))
        self.db.commit()

        self.clear_bike_repair_tree()
        self.bike_repair_details()
        self.repair_button_frame.place(x = 1000000, y = 1000000)

        self.repair_button.event_generate("<ButtonRelease-1>")

    #Define a function to open the Popup Dialogue
    def popupwin(self, values):
        #Create a Toplevel window
        top = Toplevel(self.window)
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
        button= Button(top, text="Submit", command = lambda:self.insert_val(top, entry.get(), entry2.get(), values))
        button.place(x = 170, y = 150)

    # Function to clear the data in the repair tab's table such that newly updated data can be loaded:
    def clear_bike_repair_tree(self):
        for item in self.bike_repair_tree.get_children():
            self.bike_repair_tree.delete(item)


    # Function to load move bike details on the move bike tab:
    def bike_move_details(self):
        # Get data from the bike_status table:
        bike_move_details = self.cursor.execute("SELECT bike_id, type, bike_number, station_name, station_id from v_bike_status") 
        
        # User table frame
        self.bike_move_frame.place(x = 20, y = 55, width = 1000, height = 190)
        self.bike_move_scroll.pack(side = RIGHT, fill = Y)
        self.bike_move_tree.place(x = 20, y = 25, width = 1000, height = 190)
        self.bike_move_scroll.config(command = self.bike_move_tree.yview)
        self.bike_move_tree['columns'] = ("Bike ID", "Bike Type", "Bike Number", "Station Name", "Station ID")
        self.bike_move_tree.column("#0", width = 0, stretch = NO)
        self.bike_move_tree.column("Bike ID", anchor = W, width = 200)
        self.bike_move_tree.column("Bike Type", anchor = W, width = 200)
        self.bike_move_tree.column("Bike Number", anchor = W, width = 200)
        self.bike_move_tree.column("Station Name", anchor = W, width = 200)
        self.bike_move_tree.column("Station ID", anchor = W, width = 200)
        self.bike_move_tree.heading("#0", text = "", anchor = W)
        self.bike_move_tree.heading("Bike ID", text = "Bike ID", anchor = W)
        self.bike_move_tree.heading("Bike Type", text = "Bike Type", anchor = W)
        self.bike_move_tree.heading("Bike Number", text = "Bike Number", anchor = W)
        self.bike_move_tree.heading("Station Name", text = "Station Name", anchor = W)
        self.bike_move_tree.heading("Station ID", text = "Station ID", anchor = W)
        self.bike_move_tree.tag_configure('evenrow', background = '#E2F0CB')
        self.bike_move_tree.tag_configure('oddrow', background = '#B5EAD7')
        
        # Populate bike_track_tree with bike_location_details
        global count
        count = 0
        for record in bike_move_details:
            if count % 2 == 0:
                self.bike_move_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
               self.bike_move_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            count +=1




    def refresh(self, new_list):
        self.target_station_type.set("Select Target Station")
        self.opt1['menu'].delete(0, 'end')

        for each in new_list:
            self.opt1['menu'].add_command(label = each, command = tk._setit(self.target_station_type, each))


    def select_move_bike(self, e):
        self.cursor.execute("select station_id, station_name, available_rack_count from v_available_bike_rack")
        available_rack_details =  self.cursor.fetchall()

        # Get the current selected row:
        selected = self.bike_move_tree.focus()
        values = self.bike_move_tree.item(selected, 'values')

        current_station_id = values[4]
        initial_station_id = current_station_id
        current_bike_id = values[0]


        dropdown_list = []

        # Check if this station_id has any available racks:
        for each in available_rack_details:
            if each[0] != int(current_station_id) and each[2] > 0:
                # Populate list with this element:
                dropdown_list.append(each[1])

        self.opt1.pack_forget()
        self.refresh(dropdown_list)
        self.opt1.place(x = 850,y = 500)
        self.opt1.pack()
        self.move_button.pack_forget()
        #To trace the change in dropdown box's value. w = write mode
        self.target_station_type.trace("w", self.find_term)


    #Function to retrieve value from dropbox in tab2  
    def find_term(self, *args):
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

        self.move_button.pack_forget()
        self.move_button["text"] = "Move Bike"
        self.move_button["fg"] = "white"
        self.move_button.place(x = 1020, y = 550)
        self.move_button.pack()

    def move(self):
        # Update bike_status, move_location
        # In bike_status, change station_id for given bike_id
        # In move_location, add an entry with bike_id, initial_station_id, final_station_id, and current_system_time
        
        selected = self.bike_move_tree.focus()
        values = self.bike_move_tree.item(selected, 'values')
        current_bike_id = values[0]
        current_station_id = values[4]
        final_station_name = self.target_station_type.get()
        final_station_id = -1
        
        self.cursor.execute("select station_name, station_id from v_available_bike_rack")
        station_data = self.cursor.fetchall()

        for each in station_data:
            if each[0] == final_station_name:
                final_station_id = each[1]
                break
        
        if final_station_id != -1:
            bike_status_query = ('''UPDATE bike_status   
                    SET station_id=?
                    WHERE bike_id=?;''')
            self.cursor.execute(bike_status_query, (final_station_id, current_bike_id))

            move_location_query = ('''INSERT INTO move_location (from_station_id, to_station_id, created_time) 
            VALUES(?, ?, ?);''')
            self.cursor.execute(move_location_query, (current_station_id, final_station_id, time.strftime(r"%Y-%m-%d %H:%M:%S", time.localtime())))
            self.db.commit()

            self.clear_bike_move_tree()
            self.bike_move_details()
            self.move_button.event_generate("<ButtonRelease-1>")
            self.move_button.pack_forget()
            self.opt1.pack_forget()

        # Refresh the move_bike TreeView

    def clear_bike_move_tree(self):
        for item in self.bike_move_tree.get_children():
            self.bike_move_tree.delete(item)

    def operator_logout_handler(self):
        self.db.close()
        self.window.destroy()
        self.logout_handler()
        
    def launch_operator_window(self, user_id, role_id, logout_handler):
        self.logout_handler = logout_handler
        self.user_id = user_id
        self.role_id = role_id
        self.window = Tk()
        self.window.title('Operator View')
        self.window.geometry("1500x800")

        # Creating tabs:
        allTabs = ttk.Notebook(self.window)

        track_tab = Frame(allTabs)
        repair_tab = Frame(allTabs)
        move_tab = Frame(allTabs)

        allTabs.add(track_tab, text = "Track Bike")
        allTabs.add(repair_tab, text = "Repair Bike")
        allTabs.add(move_tab, text = "Move Bike")
        allTabs.pack(expand = 1, fill = "both")

        logout_button = Button(self.window, command = self.operator_logout_handler,  fg = "black", height = 2, width = 15)
        logout_button.place(x = 1138, y = 50)
        logout_button["text"] = "Logout"
        logout_button["fg"] = "white"
        logout_button["bg"] = "#4091c2"

        # 1. Display bike coordinates in table:
        self.track_button_frame = LabelFrame(track_tab)
        self.bike_track_frame = Frame(track_tab)
        self.bike_track_scroll = Scrollbar(self.bike_track_frame)
        self.bike_track_tree = ttk.Treeview(self.bike_track_frame, yscrollcommand = self.bike_track_scroll.set, selectmode = "extended")

        # 2. Display bike information from defect table:
        self.repair_button_frame = LabelFrame(repair_tab)
        self.bike_repair_frame = Frame(repair_tab)
        self.bike_repair_scroll = Scrollbar(self.bike_repair_frame)
        self.bike_repair_tree = ttk.Treeview(self.bike_repair_frame, yscrollcommand = self.bike_repair_scroll.set, selectmode = "extended")

        # 3. Display information of all bikes in bike_status, along with a dropdown that shows only relevant target stations for a selected bike:
        self.move_button_frame = LabelFrame(move_tab)
        self.bike_move_frame = Frame(move_tab)
        self.bike_move_scroll = Scrollbar(self.bike_move_frame)
        self.bike_move_tree = ttk.Treeview(self.bike_move_frame, yscrollcommand = self.bike_move_scroll.set, selectmode = "extended")

        # ttk style configurations:
        style = ttk.Style()
        style.configure("Treeview", background = "#0c88cc", foreground = "black", rowheight = 35, fieldbackground = "#0c88cc")
        style.map("Treeview", background = [("selected", "#0c88cc")], foreground = [("selected", "white")], font = [("selected", ("Helvetica", 16))])

        dropdown_list = [0]
        self.target_station_type = StringVar(move_tab)
        self.target_station_type.set("Select Target Station")
        self.move_button_frame.place(x = 1020, y = 75, width = 350, height = 170)
        self.opt1 = OptionMenu(self.move_button_frame, self.target_station_type, *dropdown_list)

        self.track_button = Button(self.track_button_frame, command = self.track_location, bg = "#4091c2", fg = "black", height = 2, width = 15)
        self.repair_button = Button(self.repair_button_frame, command = self.repair, bg = "#4091c2", fg = "black", height = 2, width = 15)
        self.move_button = Button(self.move_button_frame, command = self.move, bg = "#4091c2", fg = "black", height =  2, width = 15)

        self.bike_track_tree.bind("<ButtonRelease-1>", self.select_track_bike)
        self.bike_repair_tree.bind("<ButtonRelease-1>", self.select_repair_bike)
        self.bike_move_tree.bind("<ButtonRelease-1>", self.select_move_bike)

        self.bike_location_details()
        self.bike_repair_details()
        self.bike_move_details()

        self.window.mainloop()
        self.db.close()

