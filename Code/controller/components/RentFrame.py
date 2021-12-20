#import packages
from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
import sqlite3
import time
import datetime

class RentFr:


    def __init__(self, parent, user_id, user_full_name, customer_id):
        # connect to sqlite db
        with sqlite3.connect("bikesharedatabase.db") as db:
            self.cursor = db.cursor()
            self.db = db
        self.user_id = user_id
        self.user_full_name = user_full_name
        self.customer_id = customer_id



                #tkinter window configurations
        self.window = Frame(parent.notebook, width=800, height=800, bg='white')
        self.frame = self.window
        
        
        
        #ttk style configurations
        # style = ttk.Style()
        # style.theme_use('aqua')
        # style.configure("Treeview", background="#0c88cc", 
        #                 foreground="black",
        #                 rowheight=35
        #                 ,fieldbackground="0c88cc"
        #                 )
        # style.map('Treeview', background=[('selected', "#0c88cc")], foreground=[('selected', "white")], font=[('selected', ("Helvetica",20))])

        #font for text in bottons
        self.myFont = font.Font(family='Helvetica', size=16, weight='bold')
      

        #call function to initialise
        self.station_frame, self.station_scroll, self.station_tree, self.bike_frame, self.bike_scroll, self.bike_tree, self.return_station_frame, self.return_station_scroll, self.return_station_tree, self.rent_button, self.rental_status_frame, self.return_button, self.return_button2, self.return_button3, self.greeting_label_frame, self.greeting_label, self.greeting_label_frame2, self.greeting_label2, self.bike_list_label_frame_a, self.bike_list_label_a, self.bike_list_label_frame_na, self.bike_list_label_na, self.rental_progress_frame, self.rental_progress_label, self.from_station_entry, self.low_balance_frame, self.low_balance_label = self.windowInitialization()

        #call function getStationList
        self.station_list = self.getStationList()

        #get active rental details
        self.active_rental = self.getActiveRental()

        print(self.active_rental)
        print(len(self.active_rental))

        #call function to populate station list
        self.populateStationList(self.station_list)
                
        
        if len(self.active_rental) > 0:
            self.populateRentalStatus(self.active_rental)
            self.enjoyRideLabel()

        else:
        #    print("inside else")
            self.goodMorningLabel()

                
            
                
        #call selectStation function upon click on station record   
        self.station_tree.bind("<ButtonRelease-1>", self.selectStation)  

        #call selectBike function upon click on bike record
        self.bike_tree.bind("<ButtonRelease-1>", self.selectBike)

        #call selectReturnStation upon click on station to return
        self.return_station_tree.bind("<ButtonRelease-1>", self.selectReturnStation)

        #to init timer
        #hour,minute,second,hourLabel,minuteLabel,secondLabel = timerInit() 





        # function to run at the beginning to do inital jobs


    def refresh_data(self):
        self.goodMorningLabel()

    def __del__(self):
        self.db.close()


    def windowInitialization(self):

        #station table frame
        station_frame = Frame(self.window, width = 300, height = 300)
        station_scroll = ttk.Scrollbar(station_frame)
        station_scroll.pack(side=RIGHT, fill=BOTH)
        station_tree= ttk.Treeview(station_frame, yscrollcommand=station_scroll.set, selectmode = "extended")
        

        #bike table frame
        bike_frame = Frame(self.window)
        bike_scroll = ttk.Scrollbar(bike_frame)
        bike_tree = ttk.Treeview(bike_frame, yscrollcommand=bike_scroll.set, selectmode = "extended")
        
        
        #rent button
        rent_button = Button(self.window, text="Click to Start Rental", 
                    command = self.startBikeRental, 
                    bg = 'white', fg = 'blue', 
                    height = 2, width = 15)
        
        rent_button['font'] = self.myFont
        
        #rental status frame
        rental_status_frame = LabelFrame(self.window, text = "Rental Status")
        
        #return station frame
        return_station_frame = Frame(self.window, width = 260, height = 300)
        return_station_scroll = ttk.Scrollbar(return_station_frame)
        return_station_scroll.pack(side=RIGHT, fill=BOTH)
        return_station_tree= ttk.Treeview(return_station_frame, yscrollcommand=return_station_scroll.set, selectmode = "extended")
        
        
        #return buttons
        return_button = Button(rental_status_frame, text="Click to Return Bike", command = self.showReturnStationList, 
                            height = 4, width = 25)
        return_button['font'] = self.myFont
        
        return_button2 = Button(rental_status_frame, text="Select a station to return ⏩",  
                            height = 4, width = 25)
        return_button2['font'] = self.myFont
        
        return_button3 = Button(rental_status_frame, text="Click to confirm return", command = self.returnBike,
                                bg = 'white', fg = 'blue', 
                            height = 4, width = 25)
        return_button3['font'] = self.myFont
        
        
        #different label frames and corresponding labels
        
        #TODO - Replace hard coded user name with user name from session
        #self.user_full_name = "K Macmillan"
        
        #TODO - Replace hard coded customer IDC= 1 with customer ID from session
        customer_id = 2
        
        
        greeting_label_frame = LabelFrame(self.window, text = "Hey "+self.user_full_name+", ")
        
        now = datetime.datetime.now()
        
        wallet_balance = self.getWalletBalace()
        
        #to display different greetings based on time of the day
        if now.hour >= 5 and now.hour <= 11:
            greeting_label = Label(greeting_label_frame, text="Good Morning! 🌞 \n\nYour wallet balance is: £ "+str(wallet_balance)+". Select a station below to view available bikes.")
        elif now.hour >= 12 and now.hour <= 16:
            greeting_label = Label(greeting_label_frame, text="Good Afternoon! ☀️ \n\nYour wallet balance is: £ "+str(wallet_balance)+". Select a station below to view available bikes.")
        elif now.hour >= 17 and now.hour <= 20:
            greeting_label = Label(greeting_label_frame, text="Good Evening! 🌅 \n\nYour wallet balance is: £ "+str(wallet_balance)+". Select a station below to view available bikes.")
        else:
            greeting_label = Label(greeting_label_frame, text="Its a lovely night! 🌙 \n\nYour wallet balance is: £ "+str(wallet_balance)+". Select a station below to view available bikes.")
        
        greeting_label_frame2 = LabelFrame(self.window, text = "Hey "+self.user_full_name+", ")
        greeting_label2 = Label(greeting_label_frame2, text="\nEnjoy your ride! 🚴‍♀️")
        
        bike_list_label_frame_a = LabelFrame(self.window, text = "Bikes are available 😀")
        bike_list_label_a = Label(bike_list_label_frame_a, text="\nSelect a bike below and start your rental 👍")
        
        bike_list_label_frame_na = LabelFrame(self.window, text = "Bikes are not available 🙁")
        bike_list_label_na = Label(bike_list_label_frame_na, text="Looks like all of our bikes are rented out at this station! \n\n Please select a different station or try again later ⏳")           

        rental_progress_frame = LabelFrame(self.window, text = "Rental is in progress")
        rental_progress_label = Label(rental_progress_frame, text="Your rental is in progress. Enjoy and drive safely 😊. \n To return 🚲, press Return Bike and select the station. ")           

        low_balance_frame = LabelFrame(self.window, text = "Low Wallet Balance 🙁")
        low_balance_label = Label(low_balance_frame, text="Your wallet balance is less than zero. Please recharge to continue 😊")           


        from_station_entry = Label(rental_status_frame)
        
        return station_frame, station_scroll, station_tree, bike_frame, bike_scroll, bike_tree, return_station_frame, return_station_scroll, return_station_tree, rent_button, rental_status_frame, return_button, return_button2, return_button3, greeting_label_frame, greeting_label, greeting_label_frame2, greeting_label2, bike_list_label_frame_a, bike_list_label_a, bike_list_label_frame_na, bike_list_label_na, rental_progress_frame, rental_progress_label, from_station_entry, low_balance_frame, low_balance_label
    
    
    
        
    #function to get station list, available bikes, available racks from db    
    def getStationList(self):
    #    print("inside getStationList")
        self.cursor.execute("""SELECT station_name, 
        case 
        when available_bike_count == 0 then '🙁 No bikes' 
        when available_bike_count == 1 then '🚲'
        when available_bike_count == 2 then '🚲🚲' 
        when available_bike_count == 3 then '🚲🚲🚲'
        when available_bike_count == 4 then '🚲🚲🚲🚲' 
        when available_bike_count == 5 then '🚲🚲🚲🚲🚲' 

        when available_bike_count > 5 then available_bike_count||' bikes 😇' 
        end as available_bikes, 
        CASE 
        when available_rack_count < 0 then '🙁 No racks' 
        when available_rack_count == 0 then '🙁 No racks' 
        when available_rack_count == 1 then available_rack_count||'/'||rack_count||' rack' 
        when available_rack_count > 1 then available_rack_count||'/'||rack_count||' racks'
        end as available_racks,
        station_id
        FROM v_available_bike_rack 
        order by available_bike_count desc, available_rack_count desc
        limit 10;""")
        station_list = self.cursor.fetchall()
    #    print("station_list: ", station_list)
        return station_list

    #function to get the active rental from db
    def getActiveRental(self):
    #    print("inside getActiveRental")
        active_rental = []
        
        
        #customer_id from session
        self.cursor.execute("""select b.type, b.bike_number, s.station_name, s.latitude , s.longitude, 
        strftime('%H:%M on %d-', r.start_time)||
        substr('JanFebMarAprMayJunJulAugSepOctNovDec', 1 + 3*strftime('%m', date(r.start_time)), -3) as start_time               
        , r.rental_status, r.bike_id, r.start_station_id
        from rental r 
        left join bike b
        on r.bike_id = b.id 
        left join station s 
        on s.id = r.start_station_id 
        where r.customer_id = ?
        and lower(rental_status) == 'ongoing'
        ;""", (self.customer_id, ))
        active_rental = self.cursor.fetchall()
    #    print("active rental count: ",len(active_rental))
        return active_rental

    #function to populate station list to station tree
    def populateStationList(self,station_list):
        #station table frame
        self.station_frame.place(x = 10, y = 100, width = 720, height = 240)
        self.station_scroll.pack(side=RIGHT, fill=Y)
        self.station_tree.pack()
        self.station_scroll.config(command = self.station_tree.yview)
        self.station_tree['columns'] = ("Station", "Bikes", "Racks")
        self.station_tree.column("#0", width = 0, stretch = NO)
        self.station_tree.column("Station", anchor=W, width=240)
        self.station_tree.column("Bikes", anchor=CENTER, width=240)
        self.station_tree.column("Racks", anchor=CENTER, width=240)
        self.station_tree.heading("#0",text = "", anchor = W)
        self.station_tree.heading("Station",text = "Station", anchor = W)
        self.station_tree.heading("Bikes",text = "Bikes", anchor = W)
        self.station_tree.heading("Racks",text = "Racks", anchor = W)
        self.station_tree.tag_configure('evenrow', background = '#E2F0CB')
        self.station_tree.tag_configure('oddrow', background = '#B5EAD7')
        
        #populate station_list to station_tree
        global count
        count = 0
        for record in station_list:
    #        print("record: ", record)
            if count % 2 == 0:
                self.station_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.station_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count +=1
            
    #function to do tasks when click on a station record
    def selectStation(self,e):   
    #    print("inside selectStation")

        #clear bike tree
        self.clearBikeTree()
        self.bike_frame.place_forget()
        self.hideLowWalletLabel()
        #hide rent button
        self.rent_button.place_forget()
        selected = self.station_tree.focus()
        values = self.station_tree.item(selected, 'values')
    #    print("selectStation: ",values)
    #    print("selectStation: ",values[3])
        selected_station_query="""select station_name, type, bike_number, station_id, bike_id from v_bike_status 
        where
        is_defect = 0 AND 
        is_available = 1 AND 
        is_rented = 0 AND 
        station_id =?
        order by bike_number"""
        self.cursor.execute(selected_station_query,(values[3],))
        bike_list = self.cursor.fetchall()
    #    print("bike_list: ")
    #    print(bike_list)
    #    print("length of bike list: ",len(bike_list))
        active_rental = self.getActiveRental()
    #    print("length of active rental: ",len(active_rental))

        if len(active_rental) == 0:
        #    print("inside first if")
            if len(bike_list) > 0:
                self.bikeAvailableLabel()
                self.populateBikeList(bike_list)
            #    print("to populate bike list")
            else:
                self.bikeNotAvailableLabel()
        else:
            print(active_rental)

        
    #function to populate bike list in bike_tree        
    def populateBikeList(self,bike_list):
        self.bike_frame.place(x = 10, y = 430, width = 720, height = 240)
        self.bike_scroll.pack(side=RIGHT, fill=Y)
        self.bike_tree.pack()
        self.bike_scroll.config(command = self.bike_tree.yview)
        self.bike_tree['columns'] = ("Station","Type", "BikeNum")
        self.bike_tree.column("#0", width = 0, stretch = NO)
        self.bike_tree.column("Station", anchor=W, width=240)
        self.bike_tree.column("Type", anchor=CENTER, width=240)
        self.bike_tree.column("BikeNum", anchor=CENTER, width=240)
        self.bike_tree.heading("#0",text = "", anchor = W)
        self.bike_tree.heading("Station",text = "Station", anchor = W)
        self.bike_tree.heading("Type",text = "Type", anchor = W)
        self.bike_tree.heading("BikeNum",text = "BikeNum", anchor = W)
        self.bike_tree.tag_configure('evenrow', background = '#E2F0CB')
        self.bike_tree.tag_configure('oddrow', background = '#B5EAD7')
        
        #populate bike records from db to bike table frame
        count = 0
        for record in bike_list:
            if count % 2 == 0:
                self.bike_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                self.bike_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            count +=1
        

    #function to call when select a bike record in bike_tree
    def selectBike(self,e): 
    #    print("inside selectBike")
        selected = self.bike_tree.focus()
        values = self.bike_tree.item(selected, 'values')
    #    print("selected_bike: ", values)
        wallet_balance = self.getWalletBalace()
        self.hideLowWalletLabel()
        if wallet_balance <= 0.0:
        #    print("balance less than -10")
            self.lowWalletLabel()
        else:
            self.rent_button.place(x = 800, y = 300, width = 400, height = 200)
        
    #function to get the wallet balance of customer    
    def getWalletBalace(self):
    #    print("inside getWalletBalace")
        wallet_balance = []
        
        get_wallet_balance_query = """select wallet_balance
                    from customer where id = ?
                    limit 1;"""
        self.cursor.execute(get_wallet_balance_query, (self.customer_id, ))

        wallet_balance = self.cursor.fetchall()
    #    print("wallet_balance: ",wallet_balance[0][0])
        return wallet_balance[0][0]  
        
        
    #function to call when click on start rental button
    def startBikeRental(self): 
        print("inside startBikeRental")
        selected = self.bike_tree.focus()
        values = self.bike_tree.item(selected, 'values')

    #    print("selected bike: ",values)

        insert_rental_query="""insert into rental(customer_id, bike_id, start_time, start_station_id, rental_status)
        values(?, ?, datetime('now', 'localtime'), ?, 'ongoing')"""
        
        #customer_id from session
        self.cursor.execute(insert_rental_query, (self.customer_id, values[4], values[3]))
        
        update_bike_status_query="""update bike_status set is_rented = 1, is_available = 0 where bike_id = ?"""
        self.cursor.execute(update_bike_status_query, (values[4],))
        
        self.db.commit()
        self.rent_button.place_forget()
        #call function getStationList
        station_list = []
        station_list = self.getStationList()
        self.clearStationTree()
        self.station_frame.place_forget()
        self.populateStationList(station_list)
        bike_list = []
        self.clearBikeTree()
        self.bike_tree.pack_forget()

    #    startTimer()
        
        #get active rental details
        active_rental = self.getActiveRental()
                
        if len(active_rental) > 0:
    #    #    print("inside if len activerental > 0")
            self.populateRentalStatus(active_rental)
            self.enjoyRideLabel()
        else:
    #    #    print("inside else")
            self.goodMorningLabel()

    #function to display enjoy ride label
    def enjoyRideLabel(self):
    #    print("inside enjoyRideLabel")
        self.bike_list_label_a.grid_forget() 
        self.bike_list_label_frame_a.place_forget()
        self.bike_list_label_na.grid_forget() 
        self.bike_list_label_frame_na.place_forget()
        self.greeting_label.grid_forget()
        self.greeting_label_frame.place_forget()
        self.greeting_label_frame2.place(x=10, y=10, width = 720, height = 90) 
        self.greeting_label2.grid(column=0, row=0, sticky=W, padx=5, pady=5)
        
    #functino to greet user    
    def goodMorningLabel(self):
    #    print("inside goodMorningLabel")
        self.greeting_label_frame2.place_forget()
        self.greeting_label2.grid_forget()
        
        now = datetime.datetime.now()
        wallet_balance = self.getWalletBalace()
        
        #to display different greetings based on time of the day
        if now.hour >= 5 and now.hour <= 11:
            greeting_label = Label(self.greeting_label_frame, text="Good Morning! 🌞 \n\nYour wallet balance is: £ "+str(wallet_balance)+". Select a station below to view available bikes.")
        elif now.hour >= 12 and now.hour <= 16:
            greeting_label = Label(self.greeting_label_frame, text="Good Afternoon! ☀️ \n\nYour wallet balance is: £ "+str(wallet_balance)+". Select a station below to view available bikes.")
        elif now.hour >= 17 and now.hour <= 20:
            greeting_label = Label(self.greeting_label_frame, text="Good Evening! 🌅 \n\nYour wallet balance is: £ "+str(wallet_balance)+". Select a station below to view available bikes.")
        else:
            greeting_label = Label(self.greeting_label_frame, text="Its a lovely night! 🌙 \n\nYour wallet balance is: £ "+str(wallet_balance)+". Select a station below to view available bikes.")

        self.greeting_label_frame.place(x=10, y=10, width = 720, height = 90) 
        greeting_label.grid(column=0, row=0, sticky=W, padx=5, pady=5)
        

    #function to show labels when bikes are available in a station
    def bikeAvailableLabel(self):
    #    print("inside bikeAvailableLabel")
       self.bike_list_label_frame_na.place_forget()
       self.bike_list_label_na.grid_forget()
       self.bike_list_label_frame_a.place(x=10, y=340, width = 720, height = 90)
       self.bike_list_label_a.grid(column=0, row=0, sticky=W, padx=5, pady=5)
        
    #function to show label when bikes are not available in a station    
    def bikeNotAvailableLabel(self):
    #    print("inside bikeNotAvailableLabel")
       self.bike_list_label_frame_a.place_forget()
       self.bike_list_label_a.grid_forget()
       self.bike_list_label_frame_na.place(x=10, y=340, width = 720, height = 90)
       self.bike_list_label_na.grid(column=0, row=0, sticky=W, padx=5, pady=5)
        
    #function to show lable when wallet amount is low    
    def lowWalletLabel(self):
    #    print("inside lowWalletLabel")
    #    low_balance_frame.place(x=730, y=450, width = 680, height = 90)
        self.low_balance_frame.place(x = 10, y = 430, width = 720, height = 240)
        self.low_balance_label.grid(column=0, row=0, sticky=W, padx=5, pady=15)   

    #function to hide label for low amount in wallet
    def hideLowWalletLabel(self):
    #    print("inside lowWalletLabel")
        self.low_balance_frame.place_forget()
        self.low_balance_label.grid_forget()

    #function to clear bike_bike tree
    def clearBikeTree(self):
        #Clear the treeview list items
        for item in self.bike_tree.get_children():
            self.bike_tree.delete(item)
        
    #function to clear station tree
    def clearStationTree(self):
        #Clear the treeview list items
        for item in self.station_tree.get_children():
            self.station_tree.delete(item)
        
    #function to clear return station tree
    def clearReturnStationTree(self):
        #Clear the treeview list items
        for item in self.return_station_tree.get_children():
            self.return_station_tree.delete(item)
        

    #function to populate active rental status        
    def populateRentalStatus(self,active_rental):
    #    print("inside populateRentalStatus")
    #    print(active_rental[0])
    #    print(active_rental[0][0])
        
        
        self.rental_progress_frame.place(x=730, y=10, width = 690, height = 90)
        self.rental_progress_label.grid(column=0, row=0, sticky=W, padx=5, pady=5)
        
        self.rental_status_frame.place(x=730, y=100, width = 690, height = 300)  

        #bike type
        bike_type_label = Label(self.rental_status_frame, text="Bike type:")
        bike_type_label.grid(column=0, row=0, sticky=W, padx=5, pady=5)
        
        bike_type_entry = Label(self.rental_status_frame, text = active_rental[0][0])
        bike_type_entry.grid(column=1, row=0, sticky=E, padx=5, pady=5)
        
        # bike num
        bike_number_label = Label(self.rental_status_frame, text="Bike number:")
        bike_number_label.grid(column=0, row=1, sticky=W, padx=5, pady=5)
        
        bike_number_entry = Label(self.rental_status_frame, text = active_rental[0][1])
        bike_number_entry.grid(column=1, row=1, sticky=E, padx=5, pady=5)
        
        
        # start station
        from_station_label = Label(self.rental_status_frame, text="Started from:")
        from_station_label.grid(column=0, row=2, sticky=W, padx=5, pady=5)
        
        self.from_station_entry["text"] = active_rental[0][2]
        self.from_station_entry.grid(column=1, row=2, sticky=E, padx=5, pady=5)
        
        # start time
        from_time_label = Label(self.rental_status_frame, text="Started at:")
        from_time_label.grid(column=0, row=3, sticky=W, padx=5, pady=5)
        
        from_time_entry = Label(self.rental_status_frame, text = active_rental[0][5])
        from_time_entry.grid(column=1, row=3, sticky=E, padx=5, pady=5)
        
        # rent status
        rent_status_label = Label(self.rental_status_frame, text="Rental status:")
        rent_status_label.grid(column=0, row=4, sticky=W, padx=5, pady=5)
        
        rent_status_entry = Label(self.rental_status_frame, text = active_rental[0][6])
        rent_status_entry.grid(column=1, row=4, sticky=E, padx=5, pady=5)
        
        # return button
        self.return_button.grid(column=1, row=7, sticky=E, padx=5, pady=5)
        

    #function to show station list for return
    def showReturnStationList(self):
    #    print("inside showReturnStationList")
        self.return_button2.grid(column=1, row=7, sticky=E, padx=5, pady=5)
        station_list = []
        station_list = self.getStationList()
    #    clearStationTree()
    #    station_frame.place_forget()
        self.populateReturnStationList(station_list)


    #function to populate return station list to return station tree
    def populateReturnStationList(self,station_list):
        #return station table frame
    #    return_station_frame.place(x = 900, y = 400, width = 300, height = 240)
        self.return_station_frame.place( x = 1110, y = 130, width = 300, height = 240)
    #    return_station_scroll.pack(side=RIGHT, fill=Y)
        self.return_station_tree.pack()
    #    return_station_scroll.config(command = return_station_tree.yview)
        self.return_station_tree['columns'] = ("Station")
        self.return_station_tree.column("#0", width = 1, stretch = NO)
        self.return_station_tree.column("Station", anchor=CENTER, width=300)
        self.return_station_tree.heading("#0",text = "", anchor = W)
        self.return_station_tree.heading("Station",text = "Select return station", anchor = W)
        self.return_station_tree.tag_configure('evenrow', background = 'ivory2')
        self.return_station_tree.tag_configure('oddrow', background = 'ivory3')
        
        #populate station_list to return station_tree
        global count
        count = 0
        for record in station_list:
        #    print("record: ", record)
            if count % 2 == 0:
                self.return_station_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3]), tags=('evenrow',))
            else:
                self.return_station_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1], record[2], record[3]), tags=('oddrow',))
            count +=1
            
    #function to call when return station is selected from the list
    def selectReturnStation(self,e):
    #    print("inside selectReturnStation")
        selected = self.return_station_tree.focus()
        values = self.return_station_tree.item(selected, 'values')
    #    print("selectStation: ",values)
        self.return_button3.grid(column=1, row=7, sticky=E, padx=5, pady=5)
    
    #function to call when returning a bike
    def returnBike(self):
    #    print("inside returnBike")   
        selected = self.return_station_tree.focus()
        values = self.return_station_tree.item(selected, 'values')
    #    print("selectStation: ",values)
    #    print("stationID:", values)
        
        #customer_id from session
        self.cursor.execute("""SELECT id, bike_id, start_station_id from rental
                    where customer_id = ? and lower(rental_status) = 'ongoing'
                    order by id desc
                    limit 1;""", (self.customer_id, ))
        ongoing_ride = self.cursor.fetchall()
        
    #    print("ongoing_ride: ", ongoing_ride)
    #    print(ongoing_ride[0])

        return_bike_query_bike_status ="""update bike_status set station_id = ?, is_available = 1 , is_rented = 0 
        where bike_id = ?
        """
        self.cursor.execute(return_bike_query_bike_status, (values[3], ongoing_ride[0][1], ) )
        self.db.commit()
        
        return_bike_query_rental_endtime ="""update rental set end_time = datetime('now', 'localtime')
        where id = ?"""
        self.cursor.execute(return_bike_query_rental_endtime, (ongoing_ride[0][0], ))
        self.db.commit()
        
        return_bike_query_rental ="""update rental set 
        end_station_id = ?, 
        duration = ( ROUND((JULIANDAY(end_time) - JULIANDAY(start_time)) * 86400) ), 
        amount =  ROUND( (ROUND((JULIANDAY(end_time) - JULIANDAY(start_time)) * 86400)  )/ 6000, 2 ) , 
        rental_status = 'complete', payment_status = 'calculated', feedback = ''
        where id = ?"""
        self.cursor.execute(return_bike_query_rental, (values[3], ongoing_ride[0][0],  ) )
        self.db.commit()
        
        return_bike_query_payment ="""update customer  
        set wallet_balance  = wallet_balance -
        (select CASE WHEN amount IS NULL THEN 0 ELSE amount END from rental r 
        where r.id = ? )
        where id = ?  """
        
        #customer_id from session
        self.cursor.execute(return_bike_query_payment, (ongoing_ride[0][0], self.customer_id, ) )
        self.db.commit()
        
        return_bike_query_paid ="""update rental set 
        payment_status = 'paid' 
        where id = ? and payment_status = 'calculated'"""
        self.cursor.execute(return_bike_query_paid, (ongoing_ride[0][0], ) )
        self.db.commit()
        
        self.rental_status_frame.place_forget()
        self.rental_progress_frame.place_forget()
        self.rental_progress_label.grid_forget()
        self.from_station_entry.grid_forget()
        
        station_list = []
        station_list = self.getStationList()
        self.clearStationTree()
        self.station_frame.place_forget()
        self.return_station_frame.place_forget()
        self.populateStationList(station_list)
        self.goodMorningLabel()
        self.return_button.grid_forget()
        self.return_button2.grid_forget()
        self.return_button3.grid_forget()
        self.clearReturnStationTree()
    #    print("after return")
        self.openRideSummary()
        
    def openRideSummary(self):
        
        rideSummary = Toplevel(self.window)
        rideSummary.title("Your Ride Summary")
        rideSummary.geometry("710x400") 
        Label(rideSummary, text="Bike returned successfully ✌️ ").place(x=250, y=15)
        last_rental = self.getLastRental()
        ride_summary_frame = LabelFrame(rideSummary, text = "Last Ride Summary").place(x=10, y=60, width = 690, height = 300) 
        
        
        
        #bike type
        Label(rideSummary, text="Bike Type: ").place(x = 20, y = 100 )
        Label(rideSummary, text=last_rental[0][1] ).place(x = 120, y = 100 )
        
        #bike num
        Label(rideSummary, text="Bike Number: ").place(x = 20, y = 130 )
        Label(rideSummary, text=last_rental[0][2] ).place(x = 120, y = 130 )
        
        #from station
        Label(rideSummary, text="From Station: ").place(x = 20, y = 160 )
        Label(rideSummary, text=last_rental[0][3] ).place(x = 120, y = 160 )
        
        #ride start time
        Label(rideSummary, text="Ride Started: ").place(x = 20, y = 190 )
        Label(rideSummary, text=last_rental[0][4] ).place(x = 120, y = 190 )
        
        #to station
        Label(rideSummary, text="To Station: ").place(x = 20, y = 220 )
        Label(rideSummary, text=last_rental[0][6] ).place(x = 120, y = 220 )
        
        #ride end time
        Label(rideSummary, text="Ride Ended: ").place(x = 20, y = 250 )
        Label(rideSummary, text=last_rental[0][7] ).place(x = 120, y = 250 )
        
        #duration in minutes
        Label(rideSummary, text="Duration(mins): ").place(x = 20, y = 280 )
        Label(rideSummary, text=last_rental[0][8] ).place(x = 120, y = 280 )
        
        #Amount
        Label(rideSummary, text="Amount: ").place(x = 20, y = 310 )
        Label(rideSummary, text=last_rental[0][9] ).place(x = 120, y = 310 )
        
        #feedback
        feedback_label = Label(rideSummary, text="How was your ride.. Enter your feedback here:").place(x = 350, y = 100 )
        feedback_entry = Entry(rideSummary, bd =5)
        feedback_entry.place(x = 350, y = 130, width = 300, height = 50 )
        
        feedback_button = Button(rideSummary, text="Submit Feedback",
                        command=lambda: [self.updateFeedback(feedback_entry.get(), last_rental[0][0], rideSummary)], height = 4, width = 28).place(x = 350, y = 180 )
        
    
    #function to update feedback in the database 
    def updateFeedback(self,feedback_entry, rental_id, rideSummary):
    #    print("inside updateFeedback")
    #    print(feedback_entry)
    #    print(rental_id)
        
        update_feedback_query ="""update rental 
        set feedback  = ? 
        where id = ?  """
        self.cursor.execute(update_feedback_query, (feedback_entry,rental_id,) )
        self.db.commit()
        
        rideSummary.destroy()
        
        
    #function to get the last rental record from db    
    def getLastRental(self):
    #    print("inside getLastRental")
        last_rental = []
        
        #customer_id from session
        self.cursor.execute("""select r.id, b.type, b.bike_number, s.station_name start_station,
        strftime('%H:%M on %d-', r.start_time)||
        substr('JanFebMarAprMayJunJulAugSepOctNovDec', 1 + 3*strftime('%m', date(r.start_time)), -3) as start_time,
        r.rental_status, s2.station_name end_station,
        strftime('%H:%M on %d-', r.end_time)||
        substr('JanFebMarAprMayJunJulAugSepOctNovDec', 1 + 3*strftime('%m', date(r.end_time)), -3) as end_time,
        (r.duration)/60 as duration, r.amount, r.rental_status, r.payment_status, r.feedback 
        from rental r 
        left join bike b
        on r.bike_id = b.id 
        left join station s 
        on s.id = r.start_station_id 
        left join station s2 
        on s2.id = r.end_station_id 
        where r.customer_id = ?
        order by r.id desc 
        limit 1
        ;""", (self.customer_id, ))
        last_rental = self.cursor.fetchall()
    #    print("last rental: ",last_rental)
        return last_rental  
        