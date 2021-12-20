# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 16:40:49 2021

@author: Sakshi
"""

import sqlite3
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from datetime import timedelta, datetime

import PIL.Image
import sys
import subprocess
from tkinter import *
from tkinter import ttk

import tkcalendar
import pandas as pd
import numpy as np
import calendar
from tkinter.messagebox import *

import re


import warnings



warnings.filterwarnings("ignore")

# ------------Installing wordcloud------------

subprocess.check_call([sys.executable, "-m", "pip", "install", "wordcloud"])
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
# To generate word-cloud
# --------------------------------------------

# To remove 1 day from end_date

# Plot

sns.set()


class Manager:
    def __init__(self):
        with sqlite3.connect("bikesharedatabase.db") as conn:
            self.cursor = conn.cursor()
            self.conn = conn





    #================================================================================================================
    ######======================================== TAB - 1: STATION-WISE ============================================  
    #================================================================================================================

    #-----DISPLAY GRAPHS BASED ON DATE RANGE------->
    def date_range(self, start_date,end_date):
        global plot1,plot2,plot3,plot4
        if start_date<=end_date:
            
            #Remove time and only keep the date
            start_date=pd.to_datetime(start_date).date()
            end_date=pd.to_datetime(end_date).date()
            
            #Button for feedback
            feedback_btn=Button(self.tab1,text='Customer Feedback', bg='aquamarine', height = 1,width = 20, command=lambda: self.feedback(start_date,end_date))
            feedback_btn.place(x=200,y=10.4)
            
            
            #Remove date range button after use
            self.date1.place_forget()
            self.date2.place_forget()
            self.date_range_btn.place_forget()
            
            #Display date range chosen by the user
            self.chosen_date["fg"]="black"
            self.chosen_date["text"]="Chosen date-range: "+str(start_date)+" to "+str(end_date)
            
            #=================Bikes used per station for a given date range=================
            bikes_per_station = """SELECT s.station_name, count(*) as bike_rides FROM rental as r,station as s 
            WHERE r.start_station_id = s.id AND start_time BETWEEN ? AND ? group by s.station_name"""
            dataframe = pd.read_sql_query(bikes_per_station,self.conn, params=(start_date,end_date))
            ax1,bar1=self.set_plot(dataframe,self.tab1)
            if ax1==None:
                self.plot1.get_tk_widget().place_forget()
                self.error1.place(x=40,y=140,width=690,height=285)
                self.error1["text"]="No bikes at this station for the given date-time range"
            
            else:   
                self.error1.place_forget()
                plot1=bar1
                bar1.get_tk_widget().place(x=40,y=140,width=690,height=285)
                sns.barplot(data=dataframe, x='station_name', y='bike_rides', ax=ax1, color = "salmon")
                #Reduce the font size of x-axis label
                ax1.set_xticklabels(ax1.get_xmajorticklabels(), fontsize = 10)
                ax1.set(xlabel='Stations', ylabel='Number of bikes')
                ax1.set_title('Number of Bikes used per Station')
                
                
            #=========Revenue per station per bike for a given date time range==========
            revenue_per_station="""SELECT s.station_name, sum(amount) as Revenue, b.type FROM rental as r,station as s, bike as b
            WHERE r.start_station_id = s.id AND r.bike_id = b.id AND start_time BETWEEN ? AND ? group by s.station_name, b.type"""
            dataframe = pd.read_sql_query(revenue_per_station,self.conn, params=(start_date,end_date))
            ax1,bar1=self.set_plot(dataframe,self.tab1)
            if ax1==None:
                self.plot2.get_tk_widget().place_forget()
                self.error2.place(x=40,y=430,width=690,height=340)
                self.error2["text"]="No revenue generated at this station for the given date-time range"
            else:
                self.error2.place_forget()
                plot2=bar1
                bar1.get_tk_widget().place(x=40,y=430,width=690,height=340)
                sns.barplot(data=dataframe, x='station_name', y='Revenue', hue='type', ax=ax1,palette='pastel')
                #Reduce the font size of x-axis label
                ax1.set_xticklabels(ax1.get_xmajorticklabels(), fontsize = 9)
                ax1.set(xlabel='Stations', ylabel='Revenue (Pounds)')
                ax1.legend(title='Bike type')
                ax1.set_title('Revenue generated per Station')
            
            #=================Defects per station for a given date time range=================
            defects_per_station="""SELECT s.station_name, 
                CASE 
                WHEN defect_status= 'inprogress' THEN 'open'
                WHEN defect_status= 'open' THEN 'open'
                ELSE 'closed' END as def, count(*) as defects 
                FROM defect as d, station as s
                WHERE d.station_id=s.id AND defect_found_time BETWEEN ? AND ? 
                GROUP BY s.station_name,def"""
            dataframe = pd.read_sql_query(defects_per_station,self.conn, params=(start_date,end_date))
            #For defects per station, group by station and defect status 
            agg_df = dataframe.groupby(['station_name', 'def'])['defects'].sum().unstack().fillna(0)

            ax1,bar1=self.set_plot(dataframe,self.tab1)
            if ax1==None:
                self.plot3.get_tk_widget().place_forget()
                self.error3.place(x=780,y=140,width=690,height=285)
                self.error3["text"]="No defective bikes at this station for the given date-time range"
            else:
                self.error3.place_forget()
                plot3=bar1
                bar1.get_tk_widget().place(x=780,y=140,width=690,height=285)
                agg_df.plot(kind='bar', stacked=True, ax=ax1, alpha=0.6)
                #Rotate the x labels as they were verticle
                ax1.tick_params(axis='x', labelrotation=0)
                ax1.set(xlabel='Stations', ylabel='No. of defects raised (open/closed)')
                ax1.legend(labels=['Closed','Open'],title='Defect repair status')
                ax1.set_title('Defective bikes per Station')
                    
            #=================Expenditure per station for a given date time range=================
            expenditure_per_station="""SELECT s.station_name, sum(repair_cost) as cost, b.type 
                FROM defect as d, station as s, bike as b
                WHERE d.station_id=s.id AND d.bike_id=b.id AND defect_found_time BETWEEN ? AND ? 
                GROUP BY s.station_name, b.type"""
            dataframe = pd.read_sql_query(expenditure_per_station,self.conn, params=(start_date,end_date))
            ax1,bar1=self.set_plot(dataframe,self.tab1)
            if ax1==None:
                self.plot4.get_tk_widget().place_forget()
                self.error4.place(x=780,y=430,width=690,height=340)
                self.error4["text"]="No defective bikes at this station for the given date-time range"
            else:
                self.error4.place_forget()
                plot4=bar1
                bar1.get_tk_widget().place(x=780,y=430,width=690,height=340)
                sns.barplot(data=dataframe, x='station_name', y='cost', hue='type', ax=ax1,palette='pastel')
                #Reduce the font size of x-axis label
                ax1.set_xticklabels(ax1.get_xmajorticklabels(), fontsize = 9)
                ax1.set(xlabel='Stations', ylabel='Expenditure (Pounds)')
                ax1.legend(title='Bike type')
                ax1.set_title('Expenditure per Station')
                    
            #=================AGGREGATES=================
            text=""
            avg_duration="SELECT avg(duration) as avg from rental where start_time BETWEEN ? AND ?"
            dataframe = pd.read_sql_query(avg_duration,self.conn, params=(start_date,end_date))
            if dataframe.loc[0].at["avg"]!=None:
                text="Average journey duration: "+str(np.round(dataframe.loc[0].at["avg"],2))+" mins\n"
                
            total_bikes="SELECT count(*) as bikes from rental where start_time BETWEEN ? AND ?"
            dataframe = pd.read_sql_query(total_bikes,self.conn, params=(start_date,end_date))
            if dataframe.loc[0].at["bikes"]!=None:
                text+="Total number of rides taken: "+str(dataframe.loc[0].at["bikes"])+"\n"
                
            total_rev="SELECT sum(amount) as rev FROM rental WHERE start_time BETWEEN ? AND ?"
            dataframe = pd.read_sql_query(total_rev,self.conn, params=(start_date,end_date))
            if dataframe.loc[0].at["rev"]!=None:
                text+="Total revenue generated: "+str(np.round(dataframe.loc[0].at["rev"],2))+" pounds\n"
                
            active_bikes="SELECT count(*) as active from rental where end_time is NULL;"
            dataframe = pd.read_sql_query(active_bikes,self.conn)
            if dataframe.loc[0].at["active"]!=None:
                text+="Number of bikes that are currently active: "+str(dataframe.loc[0].at["active"])
            if text!="":
                self.agg_message1["text"]="In the given time period:\n"+text
                
        else:
            self.chosen_date["fg"]="red"
            self.chosen_date["text"]="Please make sure that the start date is smaller than end date."
            

    #------------ COMMON FUNCTION TO SET SUBPLOT --------->
    def set_plot(self, dataframe,tab):
        if len(dataframe)==0:
            return (None, None)
        else:
            figure = plt.Figure(figsize=(6,5), dpi=80)
            ax = figure.add_subplot(111)
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            bar = FigureCanvasTkAgg(figure, tab)
            return (ax,bar)

    #------ CALCULATE DATE RANGE FOR CURRENT DATE -------->
    def get_week(self, curr_date):
        start = curr_date - timedelta(days=curr_date.weekday())
        end = start + timedelta(days=6)
        self.date_range(start.strftime('%Y-%m-%d'),end.strftime('%Y-%m-%d'))

    def get_month(self, curr_date):
        #Convert to string to remove time
        curr_date=datetime.strftime(curr_date,"%x")
        #Convert back to datetime
        curr_date=pd.to_datetime(curr_date)
        #Extract first and last day of the month
        first_day_month = curr_date.replace(day = 1)
        #monthrange give number of days in a month
        last_day_month = curr_date.replace(day = calendar.monthrange(curr_date.year, curr_date.month)[1])
        #Send to date_range to fetch data from DB
        self.date_range(first_day_month,last_day_month)


    def get_quarter(self, curr_date):
        #12th month+1=13 which is not a month. So use month-1. Each quarter have 3 months. So divide by 3
        curr_quarter = int((curr_date.month - 1) / 3 + 1)
        #Finding start and end date in the quarter
        start_date = datetime(curr_date.year, (3 * curr_quarter) - 2, 1)
        if curr_quarter==4: 
        #For 4th Quarter, end_date will be 2021-01-01 minus 1 day = 2019-12-31. Hence we do year+1 = 2021-12-31 
            end_date = datetime(curr_date.year+1, (3 * curr_quarter)%12 + 1, 1)+timedelta(days=-1)
        else:
            end_date = datetime(curr_date.year, (3 * curr_quarter)%12 + 1, 1)+timedelta(days=-1)
        self.date_range(start_date,end_date)
        

    #Function to retrieve value from dropbox tab1  
    def find_date(self, *args):
        curr_date=datetime.today()
        if self.date_type.get()=="Custom Date Range":
            self.date1.place(x=380,y=50)
            self.date2.place(x=380,y=70)
            self.date_range_btn.place(x=380,y=90)
        elif self.date_type.get()=="Current Week":
            self.get_week(curr_date)
        elif self.date_type.get()=="Current Month":
            self.get_month(curr_date)
        elif self.date_type.get()=="Current Quarter":
            self.get_quarter(curr_date)
        elif self.date_type.get()=="Current Year":
            self.date_range(datetime(datetime.today().year, 1, 1),datetime(datetime.today().year, 12, 31))

    #================================================================================================================ 
    ######======================================== TAB - 2: TERM-WISE ===============================================       
    #================================================================================================================

    #--------- Find different terms  -------->
    def weekly(self, year):
        global plot5,plot6,plot7,plot8
        today=datetime.today()
        #Current week
        w_num=today.isocalendar()[1]
        #Last 10 weeks
        last_10_weeks=str(w_num-10)
        w_num=str(w_num)
        
        bikes_per_week = """SELECT strftime('%W', start_time) as week, strftime('%Y', start_time) as year, count(*) as bikes 
            FROM rental
            WHERE year=? AND week BETWEEN ? AND ? group by week"""
        dataframe = pd.read_sql_query(bikes_per_week,self.conn, params=(str(year),last_10_weeks,w_num))
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot5.get_tk_widget().place_forget()
            self.error5.place(x=40,y=140,width=690,height=285)
            self.error5["text"]="No bikes rented in last 10 weeks"
        else:
            self.error5.place_forget()
            plot5=bar2
            bar2.get_tk_widget().place(x=40,y=140,width=690,height=285)
            sns.lineplot(data=dataframe, x='week', y='bikes', ax=ax2, marker='o', color = "salmon")
            ax2.set(xlabel='Week Number', ylabel='Number of bikes')
            ax2.set_title('Number of Bikes in last 10 weeks')      
                
        #=========Revenue per 10 weeks ==========
        revenue_per_week="""SELECT strftime('%W', start_time) as week, strftime('%Y', r.start_time) as year, 
            b.type, sum(amount) as Revenue
            FROM rental as r, bike as b
            WHERE r.bike_id = b.id AND year=? AND week BETWEEN ? AND ? group by week, b.type"""
        dataframe = pd.read_sql_query(revenue_per_week,self.conn, params=(str(year),last_10_weeks,w_num))
        ax2, bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot6.get_tk_widget().place_forget()
            self.error6.place(x=40,y=430,width=690,height=340)
            self.error6["text"]="No revenue generated in last 10 weeks"
        else:
            self.error6.place_forget()
            plot6=bar2
            bar2.get_tk_widget().place(x=40,y=430,width=690,height=340)
            sns.lineplot(data=dataframe, x='week', y='Revenue', hue='type', ax=ax2, marker='o', palette='pastel')
            ax2.set(xlabel='Weeks', ylabel='Revenue(pounds)') 
            ax2.legend(title='Bike Type')
            ax2.set_title('Revenue generated in last 10 weeks')
        
        #================= Weekly defects ====================
        defects_per_week="""SELECT 
            CASE 
            WHEN defect_status= 'inprogress' THEN 'open'
            WHEN defect_status= 'open' THEN 'open'
            ELSE 'closed' END as def, 
            count(*) as defects, strftime('%W', defect_found_time) as week, strftime('%Y', defect_found_time) as year
            FROM defect as d, station as s
            WHERE d.station_id=s.id AND year=? AND week BETWEEN ? AND ?
            GROUP BY week, def"""
        dataframe = pd.read_sql_query(defects_per_week,self.conn, params=(str(year),last_10_weeks,w_num))
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        #For defects per quarter, group by quarter and defect status 
        agg_df = dataframe.groupby(['week', 'def'])['defects'].sum().unstack().fillna(0)

        if ax2==None:
            plot7.get_tk_widget().place_forget()
            self.error7.place(x=780,y=140,width=690,height=285)
            self.error7["text"]="No defective bikes in last 10 weeks"
        else:
            self.error7.place_forget()
            plot7=bar2
            bar2.get_tk_widget().place(x=780,y=140,width=690,height=285)
            agg_df.plot(kind='area', stacked=True, ax=ax2, alpha=0.7, cmap='icefire')
            ax2.set(xlabel='Weeks', ylabel='No. of defects raised (open/closed)')
            ax2.legend(labels=['Closed','Open'],title='Defect repair status')
            ax2.set_xticklabels(ax2.get_xmajorticklabels(), fontsize = 10)
            ax2.set_title('Defective bikes in last 10 weeks')
            
    #================= Expenditure per 10 weeks =================
        expenditure_per_week="""SELECT strftime('%W', defect_found_time) as week,
            sum(repair_cost) as cost, b.type, strftime('%Y', defect_found_time) as year 
            FROM defect as d, station as s, bike as b
            WHERE d.station_id=s.id AND d.bike_id=b.id AND year=? AND week BETWEEN ? AND ?
            GROUP BY week, b.type"""
        dataframe = pd.read_sql_query(expenditure_per_week,self.conn, params=(str(year),last_10_weeks,w_num))
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot8.get_tk_widget().place_forget()
            self.error8.place(x=780,y=430,width=690,height=340)
            self.error8["text"]="No defective bikes in last 10 weeks"
        else:
            self.error8.place_forget()
            plot8=bar2
            bar2.get_tk_widget().place(x=780,y=430,width=690,height=340)
            sns.lineplot(data=dataframe, x='week', y='cost', hue='type', ax=ax2,palette='pastel')
            ax2.set(xlabel='Weeks', ylabel='Expenditure (Pounds)')
            ax2.legend(title='Bike type')
            ax2.set_title('Expenditure in last 10 weeks')
        


    def monthly(self, year):
        global plot5,plot6,plot7,plot8
        month_num=['01','02','03','04','05','06','07','08','09','10','11','12']
        month_name=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']

        bikes_per_month = """SELECT strftime('%m', start_time) as month, strftime('%Y', start_time) as year, count(*) as bikes 
            FROM rental
            WHERE year=? group by month order by month"""
        dataframe = pd.read_sql_query(bikes_per_month,self.conn, params=(str(year),))
        #replace month number with month name
        dataframe['month']=dataframe['month'].replace(to_replace=month_num,value=month_name)
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot5.get_tk_widget().place_forget()
            self.error5.place(x=40,y=140,width=690,height=285)
            self.error5["text"]="No bikes rented this year"
        else:
            self.error5.place_forget()
            plot5=bar2
            bar2.get_tk_widget().place(x=40,y=140,width=690,height=285)
            sns.lineplot(data=dataframe, x='month', y='bikes', ax=ax2, marker='o', color = "salmon")
            ax2.set(xlabel='Months', ylabel='Number of bikes')
            ax2.set_title('Number of Bikes used per month')      
                
        #=========Revenue per month==========
        revenue_per_month="""SELECT strftime('%m', start_time) as month, strftime('%Y', r.start_time) as year, 
            b.type, sum(amount) as Revenue
            FROM rental as r, bike as b
            WHERE r.bike_id = b.id AND year=? group by month, b.type order by month"""
        dataframe = pd.read_sql_query(revenue_per_month,self.conn, params=(str(year),))
        #replace month number with month name
        dataframe['month']=dataframe['month'].replace(to_replace=month_num,value=month_name)
        ax2, bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot6.get_tk_widget().place_forget()
            self.error6.place(x=40,y=430,width=690,height=340)
            self.error6["text"]="No revenue generated this year"
        else:
            self.error6.place_forget()
            plot6=bar2
            bar2.get_tk_widget().place(x=40,y=430,width=690,height=340)
            sns.lineplot(data=dataframe, x='month', y='Revenue', hue='type', ax=ax2, marker='o', palette='pastel')
            ax2.set(xlabel='Months', ylabel='Revenue(pounds)') 
            ax2.legend(title='Bike Type')
            ax2.set_title('Revenue generated per month')
        
        #================= Monthly defects ====================
        defects_per_month="""SELECT 
            CASE 
            WHEN defect_status= 'inprogress' THEN 'open'
            WHEN defect_status= 'open' THEN 'open'
            ELSE 'closed' END as def_status, 
            count(*) as defects, strftime('%m', defect_found_time) as month, strftime('%Y', defect_found_time) as year
            FROM defect as d, station as s
            WHERE d.station_id=s.id AND year=? 
            GROUP BY month,def_status order by month"""
        dataframe = pd.read_sql_query(defects_per_month,self.conn, params=(str(year),))
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        #For defects per quarter, group by quarter and defect status 
        agg_df = dataframe.groupby(['month', 'def_status'])['defects'].sum().unstack().fillna(0)
        #Converting month numbers to names agg_df.index=month column
        agg_df.index=list(map(lambda p: month_name[int(p)-1], agg_df.index))

        if ax2==None:
            plot7.get_tk_widget().place_forget()
            self.error7.place(x=780,y=140,width=690,height=285)
            self.error7["text"]="No defective bikes for this year"
        else:
            self.error7.place_forget()
            plot7=bar2
            bar2.get_tk_widget().place(x=780,y=140,width=690,height=285)
            agg_df.plot(kind='area', stacked=True, ax=ax2, alpha=0.7, cmap='icefire')
            ax2.set(xlabel='Months', ylabel='No. of defects raised (open/closed)')
            ax2.legend(labels=['Closed','Open'],title='Defect repair status')
            ax2.set_xticklabels(ax2.get_xmajorticklabels(), fontsize = 9)
            ax2.set_title('Defective bikes per Month')
            
    #================= Expenditure per month =================
        expenditure_per_month="""SELECT strftime('%m', defect_found_time) as month,
            sum(repair_cost) as cost, b.type, strftime('%Y', defect_found_time) as year 
            FROM defect as d, station as s, bike as b
            WHERE d.station_id=s.id AND d.bike_id=b.id AND year=?
            GROUP BY month, b.type order by month"""
        dataframe = pd.read_sql_query(expenditure_per_month,self.conn, params=(str(year),))
        #replace month number with month name
        dataframe['month']=dataframe['month'].replace(to_replace=month_num,value=month_name)
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot8.get_tk_widget().place_forget()
            self.error8.place(x=780,y=430,width=690,height=340)
            self.error8["text"]="No defective bikes for this year"
        else:
            self.error8.place_forget()
            plot8=bar2
            bar2.get_tk_widget().place(x=780,y=430,width=690,height=340)
            sns.lineplot(data=dataframe, x='month', y='cost', hue='type', ax=ax2,palette='pastel')
            ax2.set(xlabel='Months', ylabel='Expenditure (Pounds)')
            ax2.legend(title='Bike type')
            ax2.set_title('Expenditure per Month')

    def quarterly(self, year): 
        global plot5,plot6,plot7,plot8
    #=================Bikes rented quarterly =================
        bikes_per_quarter = """SELECT  
        CASE 
        WHEN cast(strftime('%m', start_time) as integer) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN cast(strftime('%m', start_time) as integer) BETWEEN 4 and 6 THEN 'Q2'
        WHEN cast(strftime('%m', start_time) as integer) BETWEEN 7 and 9 THEN 'Q3'
        ELSE 'Q4' END as quarter, strftime('%Y', start_time) as year, count(*) as bikes FROM rental
        WHERE year=? group by quarter"""

        dataframe = pd.read_sql_query(bikes_per_quarter,self.conn, params=(str(year),))
        ax2, bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot5.get_tk_widget().place_forget()
            self.error5.place(x=40,y=140,width=690,height=285)
            self.error5["text"]="No bikes rented"
        else:
            self.error5.place_forget()
            plot5=bar2
            bar2.get_tk_widget().place(x=40,y=140,width=690,height=285)
            sns.lineplot(data=dataframe, x='quarter', y='bikes', ax=ax2, marker='o', color = "salmon")
            ax2.set(xlabel='Quarter', ylabel='No. of bikes') 
            #ax2.set_xticklabels(ax2.get_xmajorticklabels(), fontsize = 11)
            ax2.set_title('Number of Bikes used per quarter')
            
    #=========Revenue per quarter==========
        revenue_per_quarter="""SELECT  
        CASE 
        WHEN cast(strftime('%m', start_time) as integer) BETWEEN 1 AND 3 THEN 'Q1'
        WHEN cast(strftime('%m', start_time) as integer) BETWEEN 4 and 6 THEN 'Q2'
        WHEN cast(strftime('%m', start_time) as integer) BETWEEN 7 and 9 THEN 'Q3'
        ELSE 'Q4' END as quarter, strftime('%Y', r.start_time) as year, sum(amount) as Revenue, b.type FROM rental as r,station as s, bike as b
        WHERE year=? AND r.start_station_id = s.id AND r.bike_id = b.id group by quarter, b.type"""
        dataframe = pd.read_sql_query(revenue_per_quarter,self.conn, params=(str(year),))
        ax2, bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot6.get_tk_widget().place_forget()
            self.error6.place(x=40,y=430,width=690,height=340)
            self.error6["text"]="No revenue generated"
        else:
            self.error6.place_forget()
            plot6=bar2
            bar2.get_tk_widget().place(x=40,y=430,width=690,height=340)
            sns.lineplot(data=dataframe, x='quarter', y='Revenue', hue='type', ax=ax2, marker='o', palette='pastel')
            ax2.set(xlabel='Quarter', ylabel='Revenue(pounds)')
            ax2.legend(title='Bike Type')
            ax2.set_title('Revenue generated per quarter')

    #================= Quarterly defects ====================
        defects_per_quarter="""SELECT
            CASE 
            WHEN cast(strftime('%m', defect_found_time) as integer) BETWEEN 1 AND 3 THEN 'Q1'
            WHEN cast(strftime('%m', defect_found_time) as integer) BETWEEN 4 and 6 THEN 'Q2'
            WHEN cast(strftime('%m', defect_found_time) as integer) BETWEEN 7 and 9 THEN 'Q3'
            ELSE 'Q4' END as quarter, 
            CASE 
            WHEN defect_status= 'inprogress' THEN 'open'
            WHEN defect_status= 'open' THEN 'open'
            ELSE 'closed' END as def, 
            count(*) as defects, strftime('%Y', defect_found_time) as year
            FROM defect as d, station as s 
            WHERE d.station_id=s.id AND year=? 
            GROUP BY quarter, def"""
        dataframe = pd.read_sql_query(defects_per_quarter,self.conn, params=(str(year),))
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        #For defects per quarter, group by quarter and defect status 
        agg_df = dataframe.groupby(['quarter', 'def'])['defects'].sum().unstack().fillna(0)
        if ax2==None:
            plot7.get_tk_widget().place_forget()
            self.error7.place(x=780,y=140,width=690,height=285)
            self.error7["text"]="No defective bikes in this year"
        else:
            self.error7.place_forget()
            plot7=bar2
            bar2.get_tk_widget().place(x=780,y=140,width=690,height=285)
            agg_df.plot(kind='area', stacked=True, ax=ax2, alpha=0.7, cmap='icefire')
            ax2.set(xlabel='Quarter', ylabel='No. of defects raised (open/closed)')
            ax2.legend(labels=['Closed','Open'],title='Defect repair status')
            ax2.set_xticklabels(ax2.get_xmajorticklabels(), fontsize = 9)
            ax2.set_title('Defective bikes per Quarter')
                    
    #================= Expenditure per quarter =================
        expenditure_per_quarter="""SELECT 
            CASE 
            WHEN cast(strftime('%m', defect_found_time) as integer) BETWEEN 1 AND 3 THEN 'Q1'
            WHEN cast(strftime('%m', defect_found_time) as integer) BETWEEN 4 and 6 THEN 'Q2'
            WHEN cast(strftime('%m', defect_found_time) as integer) BETWEEN 7 and 9 THEN 'Q3'
            ELSE 'Q4' END as quarter, 
            sum(repair_cost) as cost, b.type, strftime('%Y', defect_found_time) as year 
            FROM defect as d, station as s, bike as b
            WHERE d.station_id=s.id AND d.bike_id=b.id AND year=?
            GROUP BY quarter, b.type"""
        dataframe = pd.read_sql_query(expenditure_per_quarter,self.conn, params=(str(year),))
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot8.get_tk_widget().place_forget()
            self.error8.place(x=780,y=430,width=690,height=340)
            self.error8["text"]="No defective bikes for this year"
        else:
            self.error8.place_forget()
            plot8=bar2
            bar2.get_tk_widget().place(x=780,y=430,width=690,height=340)
            sns.lineplot(data=dataframe, x='quarter', y='cost', hue='type', ax=ax2,palette='pastel')
            ax2.set(xlabel='Quarter', ylabel='Expenditure (Pounds)')
            ax2.legend(title='Bike type')
            ax2.set_title('Expenditure per Quarter')

    def yearly(self, ):
        global plot5,plot6,plot7,plot8
    #=================Bikes rented yearly =================
        bikes_per_year = "SELECT strftime('%Y', start_time) as year, count(*) as bikes FROM rental group by year"
        
        dataframe = pd.read_sql_query(bikes_per_year,self.conn)
        ax2, bar2=self.set_plot(dataframe,self.tab2)
        
        if ax2==None:
            plot5.get_tk_widget().place_forget()
            self.error5.place(x=40,y=140,width=690,height=285)
            self.error5["text"]="No bikes rented"
        else:
            self.error5.place_forget()
            plot5=bar2
            bar2.get_tk_widget().place(x=40,y=140,width=690,height=285)
            sns.lineplot(data=dataframe, x='year', y='bikes', ax=ax2, marker='o', color = "salmon")
            ax2.set(xlabel='Year', ylabel='Number of bikes')
            ax2.set_title('Number of Bikes used per year')
                
                
        #=========Revenue per year==========
        revenue_per_year="""SELECT strftime('%Y', r.start_time) as year, sum(amount) as Revenue, b.type 
            FROM rental as r,station as s, bike as b
            WHERE r.start_station_id = s.id AND r.bike_id = b.id group by year, b.type"""
        dataframe = pd.read_sql_query(revenue_per_year,self.conn)
        ax2, bar2= self.set_plot(dataframe,self.tab2)
        
        if ax2==None:
            plot6.get_tk_widget().place_forget()
            self.error6.place(x=40,y=430,width=690,height=340)
            self.error6["text"]="No revenue generated"
        else:
            self.error6.place_forget()
            plot6=bar2
            bar2.get_tk_widget().place(x=40,y=430,width=690,height=340)
            sns.lineplot(data=dataframe, x='year', y='Revenue', hue='type', ax=ax2, marker='o', palette='pastel')
            ax2.set(xlabel='Year', ylabel='Revenue(pounds)')    
            ax2.set_title('Revenue generated per year')
            
        #================= Monthly defects ====================
        defects_per_year="""SELECT 
            CASE 
            WHEN defect_status= 'inprogress' THEN 'open'
            WHEN defect_status= 'open' THEN 'open'
            ELSE 'closed' END as def, 
            count(*) as defects, strftime('%Y', defect_found_time) as year
            FROM defect as d, station as s 
            WHERE d.station_id=s.id 
            GROUP BY year,def"""
        dataframe = pd.read_sql_query(defects_per_year,self.conn)
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        #For defects per quarter, group by quarter and defect status 
        agg_df = dataframe.groupby(['year', 'def'])['defects'].sum().unstack().fillna(0)
        if ax2==None:
            plot7.get_tk_widget().place_forget()
            self.error7.place(x=780,y=140,width=690,height=285)
            self.error7["text"]="No defective bikes"
        else:
            self.error7.place_forget()
            plot7=bar2
            bar2.get_tk_widget().place(x=780,y=140,width=690,height=285)
            agg_df.plot(kind='area', stacked=True, ax=ax2, alpha=0.7, cmap='icefire')
            ax2.set(xlabel='Year', ylabel='No. of defects raised (open/closed)')
            ax2.legend(labels=['Closed','Open'],title='Defect repair status')
            ax2.set_xticklabels(ax2.get_xmajorticklabels(), fontsize = 9)
            ax2.set_title('Defective bikes per Year')
            
        #================= Yearly Expenditure =================
        expenditure_per_year="""SELECT strftime('%Y', defect_found_time) as year, 
            sum(repair_cost) as cost, b.type 
            FROM defect as d, station as s, bike as b
            WHERE d.station_id=s.id AND d.bike_id=b.id
            GROUP BY year, b.type"""
        dataframe = pd.read_sql_query(expenditure_per_year,self.conn)
        ax2,bar2=self.set_plot(dataframe,self.tab2)
        if ax2==None:
            plot8.get_tk_widget().place_forget()
            self.error8.place(x=780,y=430,width=690,height=340)
            self.error8["text"]="No defective bikes"
        else:
            self.error8.place_forget()
            plot8=bar2
            bar2.get_tk_widget().place(x=780,y=430,width=690,height=340)
            sns.lineplot(data=dataframe, x='year', y='cost', hue='type', ax=ax2,palette='pastel')
            ax2.set(xlabel='Year', ylabel='Expenditure (Pounds)')
            ax2.legend(title='Bike type')
            ax2.set_title('Expenditure per Year')
            
    #Function to retrieve value from dropbox in self.tab2  
    def find_term(self, *args):
        year=datetime.today().year
        if self.term_type.get()=="Weekly":
            self.weekly(year)
        elif self.term_type.get()=="Monthly":
            self.monthly(year)
        elif self.term_type.get()=="Quarterly":
            self.quarterly(year)
        elif self.term_type.get()=="Yearly":
            self.yearly()
        
        text = ""
        
        avg_duration="SELECT avg(duration) as avg from rental"
        dataframe = pd.read_sql_query(avg_duration,self.conn)
        if dataframe.loc[0].at["avg"]!=None:
            text="Average journey duration: "+str(np.round(dataframe.loc[0].at["avg"],2))+" mins\n"
        
        
        total_bikes="SELECT count(*) as bikes from rental"
        dataframe = pd.read_sql_query(total_bikes,self.conn)
        if dataframe.loc[0].at["bikes"]!=None:
            text+="Total number of rides taken till date: "+str(dataframe.loc[0].at["bikes"])+"\n"
                
        total_rev="SELECT sum(amount) as rev FROM rental"
        dataframe = pd.read_sql_query(total_rev,self.conn)
        if dataframe.loc[0].at["rev"]!=None:
            text+="Total revenue generated till date: "+str(np.round(dataframe.loc[0].at["rev"],2))+" pounds\n"
        
        if text!="":
            self.agg_message2["text"]= text
    
    #================================================================================================================ 
    ######======================================== TAB - 3: USER_TAB ===============================================       
    #================================================================================================================

    def user_details(self, ):
        user_status_query="""SELECT user_status, count(*) as status_count 
                            FROM login_user
                            WHERE login_role_id=1
                            GROUP BY user_status """
        
        cust_details = self.cursor.execute(user_status_query) 
        text=''
        total=0
        
        for rec in cust_details:
            if rec[0]=='active':
                text+="Number of active users: "+str(rec[1])+"\n"
            else:
                text+="Number of inactive users: "+str(rec[1])+"\n"
            total=total+rec[1]
            
        text="Total number of users: "+str(total)+"\n"+text
        self.user_det_label["text"]=text
        self.user_det_label.place(x=35, y=5)
        self.table_label1.place(x=35, y=62)
        
        user_query="""SELECT user_name, first_name, last_name, user_status 
        FROM login_user
        WHERE login_role_id=1 """
        user_list = self.cursor.execute(user_query)

        #User table frame
        self.user_frame.place(x=20, y=65, width=800, height=190)
        self.user_scroll.pack(side=RIGHT, fill=Y)
        self.user_tree.place(x=20, y=25, width=800, height=190)
        self.user_scroll.config(command = self.user_tree.yview)
        self.user_tree['columns'] = ("Username", "First Name", "Last Name", "Status")
        self.user_tree.column("#0", width = 0, stretch = NO)
        self.user_tree.column("Username", anchor=W, width=200)
        self.user_tree.column("First Name", anchor=W, width=200)
        self.user_tree.column("Last Name", anchor=W, width=200)
        self.user_tree.column("Status", anchor=W, width=200)
        self.user_tree.heading("#0",text = "", anchor = W)
        self.user_tree.heading("Username",text = "Username", anchor = W)
        self.user_tree.heading("First Name",text = "First Name", anchor = W)
        self.user_tree.heading("Last Name",text = "Last Name", anchor = W)
        self.user_tree.heading("Status",text = "Status", anchor = W)
        self.user_tree.tag_configure('evenrow', background = '#E2F0CB')
        self.user_tree.tag_configure('oddrow', background = '#B5EAD7')
        
        #populate user_list to user_tree
        global count
        count = 0
        for record in user_list:
            if count % 2 == 0:
                self.user_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1].upper(), record[2].upper(), record[3].upper()), tags=('evenrow',))
            else:
                self.user_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1].upper(), record[2].upper(), record[3].upper()), tags=('oddrow',))
            count +=1
        self.plot_user_growth(datetime.today().year)
    
        
    def plot_user_growth(self, year):
        global plot9
        today=datetime.today()
        #Current week
        w_num=today.isocalendar()[1]
        #Last 10 weeks
        last_10_weeks=str(w_num-10)
        w_num=str(w_num)
        customer_growth_query="""SELECT count(*) as customers, strftime('%W', joining_date) as weeks
                                FROM customer 
                                WHERE strftime('%Y', joining_date)=? AND weeks BETWEEN ? and ?
                                GROUP BY weeks"""
        dataframe = pd.read_sql_query(customer_growth_query,self.conn, params=(str(year),last_10_weeks,w_num))
        ax3, bar3=self.set_plot(dataframe,self.user_tab)
        if ax3==None:
            self.plot9.get_tk_widget().place_forget()
            self.error9.place(x=40,y=340,width=690,height=285)
            self.error9["text"]="No customers"
        else:
            self.error9.place_forget()
            plot9=bar3
            bar3.get_tk_widget().place(x=40,y=340,width=700,height=385)
            sns.lineplot(data=dataframe, x='weeks', y='customers', ax=ax3, marker='o', color = "salmon")
            ax3.set(xlabel='Week Number', ylabel='Number of Customers')
            ax3.set_title('Customer growth in past 10 weeks')
    
        
    def displayUserDetails(self, user_details_list):
        self.user_status_frame["text"] = "User Details of "+user_details_list[1]
        self.user_status_frame.place(x=1020, y=75, width=350, height=170)
        
        self.name_label["text"]="Name: "+user_details_list[2].upper()+" "+user_details_list[3].upper()
        self.name_label.pack()
        
        self.email_label["text"]="E-mail ID: "+user_details_list[4]
        self.email_label.pack()
        
        self.phone_label["text"]="Phone number: "+user_details_list[5]
        self.phone_label.pack()
        
        self.wallet_label["text"]="Wallet Balance: "+str(user_details_list[0])
        
        if user_details_list[0]<0:
            self.wallet_label["fg"]="red"  
        else:
            self.wallet_label["fg"]="green"
        
        self.wallet_label.pack()
        
        if user_details_list[-1]=="active":
            self.suspend_button1["text"]="Suspend User"
            self.suspend_button1["fg"]="green"
        else:
            self.suspend_button1["text"]="Activate User"
            self.suspend_button1["fg"]="red"
            
        self.suspend_button1.pack()

    #function to do tasks when click on a user record
    def selectUser(self, e):   
        #clear
        self.user_status_frame.place_forget()
        
        #hide user details
        self.suspend_button1.place_forget()
        self.status_label.place(x=10000, y=10000)
        self.name_label.place_forget()
        self.email_label.place_forget()
        self.phone_label.place_forget()
        self.wallet_label.place_forget()
        
        selected = self.user_tree.focus()
        values = self.user_tree.item(selected, 'values')
        selected_user_query="""SELECT c.wallet_balance, l.user_name, l.first_name, l.last_name, l.email, l.phone, l.user_status 
        FROM customer as c, login_user as l 
        WHERE c.id=l.customer_id and login_role_id=1 and l.user_name=?"""
        self.cursor.execute(selected_user_query,(values[0],))
        user_details_list = self.cursor.fetchall()
        if len(user_details_list) > 0:
            self.displayUserDetails(user_details_list[0])

    def suspend_user(self, ):
        selected = self.user_tree.focus()
        values = self.user_tree.item(selected, 'values')
        update_query="""UPDATE login_user 
                        SET user_status=? 
                        WHERE user_name=? """
                        
        if values[3]=='ACTIVE':
            status="inactive"
            self.status_label["text"]="Suspended!"
            self.status_label["fg"]= "red"
            
        else:
            status="active"
            self.status_label["text"]="Activated!"
            self.status_label["fg"]= "green"
            
            
        self.cursor.execute(update_query,(status,values[0]))
        self.conn.commit()
        self.clearUserTree(self.user_tree)
        self.user_details()
        self.suspend_button1.event_generate("<ButtonRelease-1>")
        self.status_label.pack()
        self.suspend_button1.place(x=10000, y=10000) #Crude


    #function to clear user tree
    def clearUserTree(self, user_tree):
        #Clear the treeview list items
        for item in user_tree.get_children():
            user_tree.delete(item)
    
    #================================================================================================================ 
    ######======================================== TAB - 4: OPERATOR_TAB ===============================================       
    #================================================================================================================

    def operator_details(self, ):
        oper_status_query="""SELECT user_status, count(*) as status_count 
                            FROM login_user 
                            WHERE login_role_id=2
                            GROUP BY user_status """
        
        oper_details = self.cursor.execute(oper_status_query) 
        text1=''
        total=0
        
        
        for rec in oper_details:
            if rec[0]=='active':
                text1+="Number of active operators: "+str(rec[1])+"\n"
            else:
                text1+="Number of inactive operators: "+str(rec[1])+"\n"
            total=total+rec[1]
            
        text1="Total number of operators: "+str(total)+"\n"+text1

        self.oper_det_label1["text"]=text1
        self.oper_det_label1.place(x=35, y=5)
        self.table_label2.place(x=35, y=62)
        
        oper_query="SELECT * from OPER_VIEW"
        oper_list = self.cursor.execute(oper_query).fetchall()
        

        
        #User table frame
        self.oper_frame.place(x=20, y=65, width=820, height=190)
        self.oper_scroll.pack(side=RIGHT, fill=Y)
        self.oper_tree.place(x=20, y=25, width=840, height=190)
        self.oper_scroll.config(command = self.oper_tree.yview)
        self.oper_tree['columns'] = ("Username", "First Name", "Last Name","No. of Bikes Repaired","No. of Bike Repairs in Progress", "Status")
        self.oper_tree.column("#0", width = 0, stretch = NO)
        self.oper_tree.column("Username", anchor=W, width=120)
        self.oper_tree.column("First Name", anchor=W, width=120)
        self.oper_tree.column("Last Name", anchor=W, width=120)
        self.oper_tree.column("No. of Bikes Repaired", anchor=W, width=150)
        self.oper_tree.column("No. of Bike Repairs in Progress", anchor=W, width=190)
        self.oper_tree.column("Status", anchor=W, width=160)
        self.oper_tree.heading("#0",text = "", anchor = W)
        self.oper_tree.heading("Username",text = "Username", anchor = W)
        self.oper_tree.heading("First Name",text = "First Name", anchor = W)
        self.oper_tree.heading("Last Name",text = "Last Name", anchor = W)
        self.oper_tree.heading("No. of Bikes Repaired",text = "No. of Bikes Repaired", anchor = W)
        self.oper_tree.heading("No. of Bike Repairs in Progress",text = "No. of Bike Repairs in Progress", anchor = W)
        self.oper_tree.heading("Status",text = "Status", anchor = W)
        self.oper_tree.tag_configure('evenrow', background = '#E2F0CB')
        self.oper_tree.tag_configure('oddrow', background = '#B5EAD7')
        
        #populate oper_list to uper_tree
        count = 0
        for record in oper_list:
            if count % 2 == 0:
                self.oper_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1].upper(), record[2].upper(), record[4], record[5], record[3].upper()), tags=('evenrow',))
            else:
                self.oper_tree.insert(parent='', index = 'end', iid = count, text = '', values = (record[0], record[1].upper(), record[2].upper(), record[4], record[5], record[3].upper()), tags=('oddrow',))
            count +=1
        self.plot_oper_defect()
    
    #Display the graph for number of defects repaired by each operator
    def plot_oper_defect(self, ):
        global plot10
        oper_defect_query="""SELECT l.user_name, count(*) as defects, defect_status
                                FROM defect as d, login_user as l
                                WHERE d.operator_id=l.id and login_role_id=2
                                GROUP BY d.operator_id, defect_status"""
        dataframe = pd.read_sql_query(oper_defect_query,self.conn)
        ax3, bar3=self.set_plot(dataframe,self.oper_tab)
        if ax3==None:
            self.plot10.get_tk_widget().place_forget()
            self.error10.place(x=40,y=340,width=690,height=285)
            self.error10["text"]="No defects or operators"
        else:
            self.error10.place_forget()
            plot10=bar3
            bar3.get_tk_widget().place(x=40,y=340,width=700,height=385)
            sns.barplot(data=dataframe, x='user_name', y='defects', hue='defect_status', ax=ax3, palette='pastel')
            ax3.set(xlabel='Operators', ylabel='Number of Defects') 
            ax3.set_title('Number of defects repaired/open per operator')

        #Display selected operator's details and suspend button
    def displayOperDetails(self, oper_details_list):
        self.oper_status_frame["text"] = "Details of operator: "+oper_details_list[1]
        self.oper_status_frame.place(x=1020, y=75, width=350, height=170)
        print(oper_details_list)
        self.name_label1["text"]="Name: "+oper_details_list[1].upper()+" "+oper_details_list[2].upper()
        self.name_label1.pack()
        
        self.email_label1["text"]="E-mail ID: "+oper_details_list[3]
        self.email_label1.pack()
        
        self.phone_label1["text"]="Phone number: "+oper_details_list[4]
        self.phone_label1.pack()
        
        if oper_details_list[-1]=="active":
            self.suspend_button2["text"]="Suspend Operator"
            self.suspend_button2["fg"]="green"
        else:
            self.suspend_button2["text"]="Activate Operator"
            self.suspend_button2["fg"]="red"
            
        self.suspend_button2.pack()

    #Fetching operator details for the selected operator
    def selectOper(self, event):   
        #clear
        self.oper_status_frame.place_forget()
        #hide user details
        self.suspend_button2.place_forget()
        self.status_label1.place(x=10000, y=10000)
        self.name_label1.place_forget()
        self.email_label1.place_forget()
        self.phone_label1.place_forget()
        
        selected = self.oper_tree.focus()
        values = self.oper_tree.item(selected, 'values')
        selected_oper_query="""SELECT l.user_name, l.first_name, l.last_name, l.email, l.phone, l.user_status 
        FROM login_user as l 
        WHERE login_role_id=2 and l.user_name=?"""
        self.cursor.execute(selected_oper_query,(values[0],))
        oper_details_list = self.cursor.fetchall()
        if len(oper_details_list) > 0:
            self.displayOperDetails(oper_details_list[0])

    def suspend_oper(self, ):
        selected = self.oper_tree.focus()
        values = self.oper_tree.item(selected, 'values')
        update_query="""UPDATE login_user 
                        SET user_status=? 
                        WHERE user_name=? """
            
        if values[5]=='ACTIVE':
            status="inactive"
            self.status_label1["text"]="Suspended!"
            self.status_label1["fg"]= "red"
            
        else:
            status="active"
            self.status_label1["text"]="Activated!"
            self.status_label1["fg"]= "green"
            
            
        self.cursor.execute(update_query,(status,values[0]))
        self.conn.commit()
        self.clearUserTree(self.oper_tree)
        self.operator_details()
        self.suspend_button2.event_generate("<ButtonRelease-2>")
        self.status_label1.pack()
        self.suspend_button2.place(x=10000, y=10000) #Crude
    
    #================================================================================================================
    ####======================================= Landing Page for Tab 1 & self.Tab2 =======================================
    #================================================================================================================
    def display_landing_pages(self, ):  
        self.weekly(datetime.today().year)
        self.get_week(datetime.today().now())
        text = ""
        
        avg_duration="SELECT avg(duration) as avg from rental"
        dataframe = pd.read_sql_query(avg_duration,self.conn)
        if dataframe.loc[0].at["avg"]!=None:
            text="Average journey duration: "+str(np.round(dataframe.loc[0].at["avg"],2))+" mins\n"
            
        total_bikes="SELECT count(*) as bikes from rental"
        dataframe = pd.read_sql_query(total_bikes,self.conn)
        if dataframe.loc[0].at["bikes"]!=None:
            text+="Total number of rides taken till date: "+str(dataframe.loc[0].at["bikes"])+"\n"
                        
        total_rev="SELECT sum(amount) as rev FROM rental"
        dataframe = pd.read_sql_query(total_rev,self.conn)
        if dataframe.loc[0].at["rev"]!=None:
            text+="Total revenue generated till date: "+str(np.round(dataframe.loc[0].at["rev"],2))+" pounds\n"
                
        if text!="":
            self.agg_message2["text"]= text
        
    #================================================================================================================
    ####======================================= WORDCLOUD - CUSTOMER FEEDBACK =======================================
    #================================================================================================================
    def feedback(self, start_date,end_date):

        feedback= """SELECT feedback from rental WHERE start_time BETWEEN ? AND ?"""
        self.cursor.execute(feedback,(start_date,end_date))
                
        all_feedbacks=[]
        records = self.cursor.fetchall()
                
        if len(records)>0:
            all_feedbacks=" ".join(val[0] for val in records if val[0] != None)
                
            #update stopwords
            stopwords = set(STOPWORDS)
            stopwords.update(['bike','bicycle','App','Interface','Overall'])
                    
            #Open the image whose shape the wordcloud will take
            bike_img = np.array(PIL.Image.open("resources/img/bike.png"))
                    
            words_present = re.findall("[a-zA-Z]+", all_feedbacks)

            if not words_present:
                print("No feedback words to generate wordcloud")
                showinfo(title  = "Info", message= "No feedback words to generate wordcloud")
                return None


            feedback_window = Toplevel()
            feedback_window.title('Customer feedback for given time period')
            canvas = Canvas(feedback_window, height=1000, width=1500)
            canvas.pack()
                    
            wordcloud= WordCloud(stopwords=stopwords, background_color="white", max_words=1000, mask=bike_img).generate(all_feedbacks)           
            plt.figure(figsize=[20,10])
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
                    
            #store to file
            plt.savefig("resources/img/bike_wordcloud.png", format="png")
            #plt.show()
            img=PhotoImage(file="resources/img/bike_wordcloud.png")
            caption=Label(feedback_window,image=img)
            caption.image=img
            caption.place(x=5,y=5)
        else:
            print("No feedback for this time period")


    def manager_logout_handler(self):
        print("logging out of manager view!")
        self.conn.close()
        self.window.destroy()
        self.logout_handler()

    #================================================================================================================
    #================================================================================================================

    def launch_manager_window(self, user_id, role_id, logout_handler):
        self.logout_handler = logout_handler
        self.user_id = user_id
        self.role_id = role_id
        # ------tkinter part ----->
        self.window = Tk()
        self.window.title('Reports')
        self.window.geometry("1500x800")
        self.f = Figure(figsize=(4,2))



        # Creating tabs
        allTabs = ttk.Notebook(self.window)

        self.tab1 = Frame(allTabs)
        self.tab2 = Frame(allTabs)
        self.user_tab = Frame(allTabs)
        self.oper_tab = Frame(allTabs)

        allTabs.add(self.tab1, text='Station-wise Reports')
        allTabs.add(self.tab2, text='Term-wise Reports')
        allTabs.add(self.user_tab, text='User Details')
        allTabs.add(self.oper_tab, text='Operator Details')
        allTabs.pack(expand=1, fill="both")

        logout_button = Button(allTabs, command = self.manager_logout_handler,  fg = "black", height = 2, width = 15)
        logout_button.place(x = 1250, y = 22.4)
        logout_button["text"] = "Logout"
        logout_button["fg"] = "white"
        logout_button["bg"] = "#4091c2"

        # ============= DROPBOX ==============
        # -----Dropbox for date selection ----->
        OptionList1 = [
            "Custom Date Range",
            "Current Week",
            "Current Month",
            "Current Quarter",
            "Current Year"
        ]

        self.date_type = StringVar(self.tab1)
        self.date_type.set("Select a date-range from this dropdown to view the graphs")

        opt1 = OptionMenu(self.tab1, self.date_type, *OptionList1)
        opt1.config(bg='olive drab')
        opt1.place(x=360, y=7)

        # To trace the change in dropdown box's value. w = write mode
        self.date_type.trace("w", self.find_date)

        # -----Dropbox for term selection ----->
        OptionList2 = [
            "Weekly",
            "Monthly",
            "Quarterly",
            "Yearly"
        ]

        self.term_type = StringVar(self.tab2)

        self.term_type.set("Weekly")

        opt2 = OptionMenu(self.tab2, self.term_type, *OptionList2)
        opt2.config(bg='olive drab')
        opt2.place(x=360, y=7)

        # To trace the change in dropdown box's value. w = write mode
        self.term_type.trace("w", self.find_term)

        # =====================================
        # -------- Tkinter Widgets ----------->
        # =====================================

        # =============== Widgets for Tab1 ==========================
        self.chosen_date = Label(self.tab1, text="", font=('Helvetica Bold', 18))
        self.chosen_date.place(x=500, y=45)

        self.error1 = Label(self.tab1, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot1 = FigureCanvasTkAgg(self.f)
        self.error2 = Label(self.tab1, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot2 = FigureCanvasTkAgg(self.f)
        self.error3 = Label(self.tab1, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot3 = FigureCanvasTkAgg(self.f)
        self.error4 = Label(self.tab1, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot4 = FigureCanvasTkAgg(self.f)

        self.agg_message1 = Label(self.tab1, text="", font=('Times', 14))
        self.agg_message1["justify"] = "left"
        self.agg_message1.place(x=40, y=50)

        # Date picker
        self.date1 = tkcalendar.DateEntry(self.tab1)
        self.date2 = tkcalendar.DateEntry(self.tab1)
        self.date_range_btn = Button(self.tab1, text='Select date', height=2, width=10, command=lambda: self.date_range(self.date1.get_date(), self.date2.get_date()))

        # =============================================================
        # ================= Widgets for self.Tab2 ==========================
        self.error5 = Label(self.tab2, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot5 = FigureCanvasTkAgg(self.f)
        self.error6 = Label(self.tab2, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot6 = FigureCanvasTkAgg(self.f)
        self.error7 = Label(self.tab2, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot7 = FigureCanvasTkAgg(self.f)
        self.error8 = Label(self.tab2, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot8 = FigureCanvasTkAgg(self.f)

        self.agg_message2 = Label(self.tab2, text="", font=('Times', 14))
        self.agg_message2["justify"] = "left"
        self.agg_message2.place(x=40, y=50)

        self.label2 = Label(self.tab2, text="Select a range from this dropdown to view the graphs:", font=('Times', 12), bg='#FFE599')
        self.label2.place(x=23, y=12)

        # =============================================================
        # ================ Widgets for User Tab =======================

        # Display all users in a table
        self.user_status_frame = LabelFrame(self.user_tab)
        self.user_frame = Frame(self.user_tab)
        self.user_scroll = Scrollbar(self.user_frame)
        self.user_tree = ttk.Treeview(self.user_frame, yscrollcommand=self.user_scroll.set, selectmode="extended")

        # ttk style configurations
        style = ttk.Style()
        # style.theme_use('aqua')
        style.configure("Treeview", background="#0c88cc",
                        foreground="black",
                        rowheight=35, fieldbackground="0c88cc"
                        )
        style.map('Treeview', background=[('selected', "#0c88cc")], foreground=[('selected', "white")], font=[('selected', ("Helvetica", 16))])

        self.user_det_label = Label(self.user_tab, font=('Helvetica Bold', 12), justify=LEFT)
        self.name_label = Label(self.user_status_frame)
        self.email_label = Label(self.user_status_frame)
        self.phone_label = Label(self.user_status_frame)
        self.wallet_label = Label(self.user_status_frame)
        self.status_label = Label(self.user_status_frame)
        # suspend button
        self.suspend_button1 = Button(self.user_status_frame,
                                 command=self.suspend_user,
                                 height=2, width=15)

        self.error9 = Label(self.user_tab, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot9 = FigureCanvasTkAgg(self.f)

        self.table_label1 = Label(self.user_tab, text="Select a user from the table below to see their details:", font=('Times', 11), bg='#FFE599')

        self.user_details()
        self.user_tree.bind("<ButtonRelease-1>", self.selectUser)

        # =============================================================
        # ================ Widgets for Oper Tab =======================

        # Display all operators in a table
        self.oper_status_frame = LabelFrame(self.oper_tab)
        self.oper_frame = Frame(self.oper_tab)
        self.oper_scroll = Scrollbar(self.oper_frame)
        self.oper_tree = ttk.Treeview(self.oper_frame, yscrollcommand=self.oper_scroll.set, selectmode="extended")

        self.oper_det_label1 = Label(self.oper_tab, font=('Helvetica Bold', 12), justify=LEFT)
        self.name_label1 = Label(self.oper_status_frame)
        self.email_label1 = Label(self.oper_status_frame)
        self.phone_label1 = Label(self.oper_status_frame)
        self.status_label1 = Label(self.oper_status_frame)
        # suspend button
        self.suspend_button2 = Button(self.oper_status_frame,
                                 command=self.suspend_oper,
                                 height=2, width=15)

        self.error10 = Label(self.oper_tab, text="", font=('Helvetica Bold', 14), bg="black", fg="red")
        self.plot10 = FigureCanvasTkAgg(self.f)

        self.table_label2 = Label(self.oper_tab, text="Select an operator from the table below to see their details:", font=('Times', 11), bg='#FFE599')

        self.operator_details()
        self.oper_tree.bind("<ButtonRelease-1>", self.selectOper)

        # Display landing page
        self.display_landing_pages()

        self.window.mainloop()
        self.conn.close()


