# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 16:45:30 2021

@author: aqib_a
"""

# OPERATOR VIEW

import sqlite3
from tkinter import *
from tkinter import ttk
import webbrowser

with sqlite3.connect("D:/workspaces/PSD/Project/bikeshare/Database/bikesharedatabase.db") as db:
    cursor = db.cursor()

cursor.executescript("""DROP TABLE IF EXISTS bike;
DROP TABLE IF EXISTS station;
DROP TABLE IF EXISTS rack;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS login_user;
DROP TABLE IF EXISTS login_role;
DROP TABLE IF EXISTS rental;
DROP TABLE IF EXISTS defect;
DROP TABLE IF EXISTS move_location;
DROP TABLE IF EXISTS track_location;
DROP TABLE IF EXISTS bike_status;
""")

cursor.executescript("""

create table if not exists bike
(
    id integer not null constraint bike_pk primary key autoincrement ,
    type         text    not null,
    created_time text default current_timestamp,
    updated_time text default current_timestamp,
    bike_number  text
);

create unique index bike_bike_number_uindex
    on bike (bike_number);

create table if not exists bike_status
(
    id             integer not null
        constraint bike_status_pk
            primary key autoincrement,
    bike_id        integer,
    rack_id        integer,
    is_available   integer,
    is_defect      integer,
    is_rented      integer,
    is_temp_parked integer,
    created_time   text default current_timestamp,
    updated_time   text default current_timestamp
);


create table if not exists customer
(
    id             integer not null
        constraint customer_pk
            primary key autoincrement,
    name           text,
    wallet_balance float,
    latitude       text,
    longitude      text,
    joining_date   text default current_timestamp,     
    created_time   text default current_timestamp,
    updated_time   text default current_timestamp
);

create table if not exists defect
(
    id                integer not null
        constraint defect_pk
            primary key autoincrement,
    bike_id           integer,
    defect_remarks    text,
    defect_found_time text,
    defect_status     text,
    repair_remarks    text,
    repair_time       text,
    repair_cost       float,
    rack_id           integer,
    operator_id       integer,
    created_time      text default current_timestamp,
    updated_time      text default current_timestamp
);

create table if not exists login_role
(
    id           integer not null constraint login_role_pk primary key autoincrement,
    role_name    text,
    created_time text default current_timestamp,
    updated_time text default current_timestamp
);

create table if not exists login_user
(
    id            integer not null  constraint login_user_pk primary key autoincrement,     
    user_name     text    not null,
    pwd           text,
    login_role_id integer,
    first_name    text,
    last_name     text,
    email         text,
    phone         text,
    user_status   text,
    customer_id   integer,
    created_time  text default current_timestamp,
    updated_time  text default current_timestamp
);

create unique index login_user_user_name_uindex
    on login_user (user_name);


create table if not exists move_location
(
    id              integer not null  constraint move_location_pk primary key autoincrement,        
    from_station_id integer,
    to_station_id   integer,
    from_rack_id    integer,
    to_rack_id      integer,
    created_time    text default current_timestamp,
    updated_time    text default current_timestamp
);

create table if not exists rack
(
    id           integer not null constraint rack_pk primary key autoincrement,
    station_id   integer,
    rack_number  integer,
    created_time text default current_timestamp,
    updated_time text default current_timestamp
);

create table if not exists rental
(
    id               integer not null 
         constraint rack_pk
            primary key autoincrement,
    customer_id      integer,
    bike_id          integer,
    start_time       datetime,
    start_station_id integer,
    start_rack_id    integer,
    end_time         datetime,
    end_station_id   integer,
    end_rack_id      integer,
    duration         integer,
    amount           float,
    rental_status    text,
    payment_status   text,
    feedback         text,
    created_time     datetime,
    updated_time     datetime
);

create table if not exists station
(
    id           integer not null
        constraint station_pk
            primary key autoincrement,
    latitude     text,
    rack_count   integer,
    longitude    text,
    station_name text,
    created_time text default current_timestamp,
    updated_time text default current_timestamp
);

create table if not exists track_location
(
    id           integer not null
        constraint track_location_pk
            primary key autoincrement,
    bike_id      integer,
    track_time   integer,
    latitude     text,
    longitude    text,
    created_time text default current_timestamp,
    updated_time text default current_timestamp
);
""")

cursor.executescript(""" INSERT INTO login_role (role_name) VALUES
                                       ('customer'),
                                       ('operator'),
                                       ('manager');

INSERT INTO defect (id, bike_id) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO bike (type, bike_number) VALUES
('SMARTbike 1.0', '54321'),
('SMARTbike 1.0', '54322'),
('SMARTbike 2.0', '54323'),
('SMARTbike 2.0', '54324'),
('eSMARTbike 2.0', '54325'),
('eSMARTbike 2.0', '54326'),
('SMARTbike 1.0', '64321'),
('SMARTbike 1.0', '64322'),
('SMARTbike 2.0', '64323'),
('SMARTbike 2.0', '64324'),
('eSMARTbike 2.0', '64325'),
('eSMARTbike 2.0', '64326');


INSERT INTO bike_status (bike_id, rack_id, is_available, is_defect, is_rented, is_temp_parked) VALUES
(1, 1, 1, 1, 0, 0),
(2, 2, 1, 1, 0, 0),
(3, 6, 1, 1, 0, 0),
(4, 7, 1, 1, 0, 0),
(5, 12, 1, 1, 0, 0),
(6, 13, 1, 1, 0, 0);

INSERT INTO station (latitude, longitude, station_name)
VALUES
    ('55.86', '-4.25', 'St Enoch'),
    ('56.86', '-5.25', 'University of Glasgow'),
    ('57.86', '-6.25', 'Clyde Arc'),
    ('58.86', '-7.25', 'Buchanan View'),
    ('59.86', '-8.25', 'University of Strathclyde'),
    ('60.86', '-9.25', 'Finnieston');

INSERT INTO rack (station_id, rack_number)
VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 1),
    (3, 2),
    (3, 3),
    (3, 4),
    (3, 5),
    (3, 6),
    (3, 7),
    (4, 1),
    (4, 2),
    (4, 3),
    (4, 4),
    (4, 5),
    (4, 6),
    (4, 7),
    (4, 8),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 5),
    (5, 6),
    (5, 7),
    (5, 8),
    (5, 9),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 5),
    (6, 6),
    (6, 7),
    (6, 8),
    (6, 9),
    (6, 10);

INSERT INTO customer (name, wallet_balance)
VALUES
    ('Sandhya', 10),
    ('Sakshi',  10),
    ('Aquib',  10),
    ('Bipin',  10),
    ('Harry',  10),
    ('Jiabei', 10);

INSERT INTO rental (customer_id, bike_id, start_time, start_station_id, 
                    start_rack_id, end_time, end_station_id, end_rack_id,
                    duration, amount, rental_status, payment_status, feedback)
VALUES
     (2, 54325, '2021-10-04 16:03:05.000', 2, 
      3, '2021-10-04 16:03:16.000', null, null, null, 'Complete', 'unpaid', null, null),
     (1, 54326, '2021-10-04 16:17:11.000', 3, 
      6, null, null, null, null, null, 'Ongoing', 'unpaid', null);

INSERT INTO track_location (id, bike_id, latitude, longitude) VALUES
    (1, 1, -10.8544921875, 49.82380908513249),
    (2, 2, -10.8544921875, 59.478568831926395),
    (3, 3, 2.021484375, 59.478568831926395),
    (4, 4, 2.021484375, 49.82380908513249);


INSERT INTO login_user (user_name, pwd, login_role_id,first_name,last_name,email,phone,customer_id,user_status)
VALUES
    ('sandhya', 'sandhya', 1,'sandhya','velati','sandhya@gmail.com', 7788991111,1,'active'),
    ('sakshi', 'sakshi', 2,'sakshi','jain','sakshi@gmail.com', 7788992222,2,'active'),
    ('aqib', 'aqib', 1,'aqib','ahmed','aquib@gmail.com', 7788993333,3,'active'),
    ('bipin', 'bipin', 2,'bipin','steephen','bipin@gmail.com', 7788994444,4,'active'),
    ('harry', 'harry',1,'harry','jones','harry@gmail.com', 7788995555,5,'active'),
    ('jiabei', 'jiabei',1,'jiabei','zhu','Jiabei@gmail.com', 7788996666,6,'active');""")

db.commit()
print("===================================displaying bike data=========================================:")
cursor.execute("SELECT * FROM bike;")
for x in cursor.fetchall():
    print(x)
print("===================================isplaying station data:======================================")
cursor.execute("SELECT * FROM station;")
for x in cursor.fetchall():
    print(x)
print("===================================displaying rack data:=======================================")
cursor.execute("SELECT * FROM rack;")
for x in cursor.fetchall():
    print(x)
print("===================================displaying customer data:===================================")
cursor.execute("SELECT * FROM customer ;")
for x in cursor.fetchall():
    print(x)
print("===================================displaying login_user data:===================================")
cursor.execute("SELECT * FROM login_user ;")
for x in cursor.fetchall():
    print(x)
print("===================================displaying login_role data:===================================")
cursor.execute("SELECT * FROM login_role ;")
for x in cursor.fetchall():
    print(x)
print("===================================displaying rental data:===================================")
cursor.execute("SELECT * FROM rental ;")

for x in cursor.fetchall():
    print(x)

bike_id = ""

# Temporary operator_id, change this when using with login.py:
operator_id = 1234

if __name__ == "__main__":

    def track_bike(b_id):
        for row1 in cursor.execute("SELECT latitude FROM track_location WHERE ID = ?", [b_id]):
            latitude = row1[0]
            break
        else:
            latitude = -1
        for row2 in cursor.execute("SELECT longitude FROM track_location WHERE ID = ?", [b_id]):
            longitude = row2[0]
            break
        else:
            longitude = -1

        if latitude == -1 or longitude == -1:
            output_str = "Coordinates not found for bike with given id."
            tab1_output_label['text'] = output_str
        else:
            output_str = "Coordinates loaded from database, launching webpage."
            tab1_output_label['text'] = output_str
            webbrowser.open('https://maps.google.com/?q=' + latitude + ',' + longitude)  # Go to example.com


    def repair_bike(b_id):
        for row in cursor.execute("SELECT is_defect FROM bike_status WHERE ID = ?", [b_id]):
            defect_status = row[0]
            break
        else:
            defect_status = -1  # not found

        if defect_status == -1:
            output_str = "Bike with id not found in database."
        elif defect_status == 0:
            output_str = "Bike does not need to be repaired."
        elif defect_status == 1:
            cursor.execute('''UPDATE bike_status   
            SET is_defect=0
            WHERE bike_id=''' + b_id + ''';''')
            cursor.execute('''UPDATE defect   
            SET defect_status="closed", operator_id=''' + str(operator_id) +
                           ''' WHERE bike_id=''' + b_id + ''';''')

            output_str = "Bike with id " + b_id + " repaired successfully."
        else:
            output_str = "Error occurred while trying to repair bike."

        tab2_output_label['text'] = output_str


    def move_bike(b_id, start_station, end_station, start_rack, end_rack):

        # Add this data to move_location
        cursor.execute(
            "INSERT INTO move_location (from_station_id, to_station_id, from_rack_id, to_rack_id) VALUES( " + start_station + ", " + end_station + ", " + start_rack + ", " + end_rack + ");")

        # Update bike_status
        # Find bike_id using rack_id
        update_query = "UPDATE bike_status SET rack_id = " + end_rack + " WHERE rack_id=" + start_rack + ";"
        cursor.execute(update_query)

        tab3_output_label['text'] = "Moved bike successfully."


    def tab3_reset():
        tab3_bike_number_entry.delete(0, END)
        tab3_start_entry.delete(0, END)
        tab3_end_entry.delete(0, END)
        tab3_start_rack_entry.delete(0, END)
        tab3_end_rack_entry.delete(0, END)


    window = Tk()
    window.title('Operator View')
    window.geometry("1500x800")

    # Creating tabs
    allTabs = ttk.Notebook(window)
    tab1 = Frame(allTabs)
    tab2 = Frame(allTabs)
    tab3 = Frame(allTabs)
    allTabs.add(tab1, text='Track Bike')
    allTabs.add(tab2, text='Repair Bike')
    allTabs.add(tab3, text='Move Bike')
    allTabs.pack(expand=1, fill="both")

    # Tab 1 Widgets:
    tab1_bike_number_label = Label(tab1, text="Enter bike id: ")
    tab1_bike_number_label.place(x=360, y=100, width=100, height=25)

    tab1_bike_number_entry = Entry(tab1, text=0)
    tab1_bike_number_entry.place(x=500, y=100, width=200, height=25)
    tab1_bike_number_entry.focus()

    tab1_get_bike_number_button = Button(tab1, text="Track Bike", fg='#f00',
                                         command=lambda: track_bike(tab1_bike_number_entry.get()))
    tab1_get_bike_number_button.place(x=400, y=150, width=100, height=25)

    tab1_reset_button = Button(tab1, text="Reset", fg='#f00', command=lambda: tab1_bike_number_entry.delete(0, END))
    tab1_reset_button.place(x=500, y=150, width=100, height=25)

    tab1_output_label = Label(tab1, text="")
    tab1_output_label.place(x=400, y=200, width=1000, height=100)

    # Tab 2 Widgets:
    tab2_bike_number_label = Label(tab2, text="Enter bike id: ")
    tab2_bike_number_label.place(x=360, y=100, width=100, height=25)

    tab2_bike_number_entry = Entry(tab2, text=0)
    tab2_bike_number_entry.place(x=500, y=100, width=200, height=25)
    tab2_bike_number_entry.focus()

    tab2_get_bike_number_button = Button(tab2, text="Repair Bike",
                                         command=lambda: repair_bike(tab2_bike_number_entry.get()))
    tab2_get_bike_number_button.place(x=400, y=150, width=100, height=25)

    tab2_reset_button = Button(tab2, text="Reset", command=lambda: tab2_bike_number_entry.delete(0, END))
    tab2_reset_button.place(x=500, y=150, width=100, height=25)

    tab2_output_label = Label(tab2, text="")
    tab2_output_label.place(x=400, y=200, width=1000, height=100)

    # Tab 3 Widgets:
    tab3_bike_number_label = Label(tab3, text="Enter bike id: ")
    tab3_bike_number_label.place(x=360, y=100, width=150, height=25)

    tab3_bike_number_entry = Entry(tab3, text="")
    tab3_bike_number_entry.place(x=500, y=100, width=200, height=25)
    tab3_bike_number_entry.focus()

    tab3_start_label = Label(tab3, text="Enter start station: ")
    tab3_start_label.place(x=360, y=150, width=150, height=25)

    tab3_start_entry = Entry(tab3, text="")
    tab3_start_entry.place(x=500, y=150, width=200, height=25)

    tab3_end_label = Label(tab3, text="Enter end station: ")
    tab3_end_label.place(x=360, y=200, width=150, height=25)

    tab3_end_entry = Entry(tab3, text="")
    tab3_end_entry.place(x=500, y=200, width=200, height=25)

    tab3_start_rack_label = Label(tab3, text="Enter start rack: ")
    tab3_start_rack_label.place(x=360, y=250, width=150, height=25)

    tab3_start_rack_entry = Entry(tab3, text="")
    tab3_start_rack_entry.place(x=500, y=250, width=200, height=25)

    tab3_end_rack_label = Label(tab3, text="Enter end rack: ")
    tab3_end_rack_label.place(x=360, y=300, width=150, height=25)

    tab3_end_rack_entry = Entry(tab3, text="")
    tab3_end_rack_entry.place(x=500, y=300, width=200, height=25)

    tab3_output_label = Label(tab3, text="")
    tab3_output_label.place(x=400, y=350, width=1000, height=100)

    tab3_move_button = Button(tab3, text="Move Bike",
                              command=lambda: move_bike(tab3_bike_number_entry.get(), tab3_start_entry.get(),
                                                        tab3_end_entry.get(), tab3_start_rack_entry.get(),
                                                        tab3_end_rack_entry.get()))
    tab3_move_button.place(x=400, y=400, width=100, height=25)

    tab3_reset_button = Button(tab3, text="Reset", command=lambda: tab3_reset())
    tab3_reset_button.place(x=500, y=400, width=100, height=25)

    # =============================================================
    window.mainloop()

    db.close()
