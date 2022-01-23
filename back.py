import math
import sqlite3
import datetime
from datetime import date

conn=sqlite3.connect('data.sqlite')
c=conn.cursor()

prev_app=''


class APPLIANCE():
    def __init__(self,name,wattage):
        self.wattage=wattage
        self.name=name
    def calc_energy(self,time): #in minutes
        return round((float(self.wattage)*float(time)*60)*(1/3600000),3) #in KWh

class TRIP():
    def __init__(self,name,co2):
        self.name=name
        self.co2=co2 #CO2 per km
    def carbon_output(self,distance):
        return float(self.co2)*float(distance)*1000 #in g

class POWER_CARBON():
    def __init__(self,name,efficiency):
        self.name=name
        self.efficiency=efficiency #CO2 grams per kilowatt hour
    def carbon_output(self,energy): #in kwh
        return((round(float(energy)*float(self.efficiency),3))) #in grams





def lin_search(obj,list):
    for i in range(len(list)):
        if list[i].name==obj:
            return(i)

def trip_co2(car,distance):
    global totall
    global conn
    global prev_app
    totall+=(float(trips_list[lin_search(car,trips_list)].carbon_output(distance)))
    c.execute("""UPDATE Total
                SET val= """+str(totall)+";")
    conn.commit()
    score_calc()

    prev_action(str('You used a '+str(car)+' for '+str(distance)+' kilometers and that created '+str(round(trips_list[lin_search(car,trips_list)].carbon_output(distance),3))+' grams of carbon'))

    return (trips_list[lin_search(car,trips_list)].carbon_output(distance))

def prev_action(ins):
    c.execute("""INSERT INTO Track (Logs) 
                VALUES('"""+str(ins)+"""')""")
    conn.commit()
    set_prev()

def set_prev():
    global prev_app
    prev_app=[]
    c.execute("""SELECT Logs
            FROM Track """)
    tempval=c.fetchall()
    for i in range(len(tempval)):
        prev_app.append(tempval[i][0])

def reset():
    global totall
    global prev_app
    c.execute("""UPDATE Total
                SET val = 0 """)
    conn.commit()
    c.execute("""UPDATE Total
                SET Start = 1 """)
    conn.commit()

    c.execute("""DELETE FROM Track""")
    set_prev()

    totall=0

    cd = datetime.date.today()

    cd = str(cd)

    cdstr = ''

    for i in range(len(cd)):
        if cd[i] == '-':
            cdstr += ","
        else:
            cdstr += cd[i]

    c.execute("""UPDATE Total
                SET Time_Start = '""" + cdstr + """'""")
    conn.commit()
    numOfDays()
    score_calc()
    count_setup(0)



def app_co2(app,time):
    global totall
    global conn
    global prev_app
    global country

    totall+=(float(countries_list[lin_search(country,countries_list)].carbon_output(appliances_list[lin_search(app,appliances_list)].calc_energy(time))))
    c.execute("""UPDATE Total
                SET val ="""+str(totall)+";")
    conn.commit()
    score_calc()
    prev_action(str('You used the '+app+' for '+time+' minutes, this used '+str(round(appliances_list[lin_search(app,appliances_list)].calc_energy(time),3))+' kiloWatts of energy and created '+str(countries_list[lin_search(country,countries_list)].carbon_output(appliances_list[lin_search(app,appliances_list)].calc_energy(time)))+' grams of carbon'))
    return(countries_list[lin_search(country,countries_list)].carbon_output(appliances_list[lin_search(app,appliances_list)].calc_energy(time)))


countries_list=[]
appliances_list=[]
trips_list=[]
score=0
country=''

c.execute("""SELECT Country
            FROM Total""")
country=str(c.fetchall()[0][0])

cd=datetime.date.today()

cd=str(cd)

cdstr=''

for i in range(len(cd)):
    if cd[i]=='-':
        cdstr+=","
    else:
        cdstr+=cd[i]




c.execute("""SELECT Start 
        FROM Total""")
tempval=c.fetchall()

if str(tempval[0][0])=='0':
    c.execute("""UPDATE Total
                SET Start = 1 """)
    conn.commit()
    c.execute("""UPDATE Total
                SET Time_Start = '"""+cdstr+"""'""")
    conn.commit()


c.execute("""SELECT Time_Start 
        FROM Total""")
tempval=c.fetchall()[0][0]
tempval.split(",")

Start_Time = date(int(tempval.split(",")[0]),int(tempval.split(",")[1]),int(tempval.split(",")[2]),)
e = datetime.datetime.now()




c.execute("""SELECT *
            FROM Total""")
tempval=c.fetchall()
totall=float(tempval[0][0])

def numOfDays():
    global day_num
    global Start_Time
    date2 = date(e.year, e.month, e.day)
    day_num = str(int(1+float(str((date2 - Start_Time).days))))



def score_calc():
    global score
    global day_num
    global totall
    score = (1000/((float(totall)+1)/(float(day_num)))*float(day_num)**1.8)


c.execute("""SELECT *
            FROM Countries""")
tempval=c.fetchall()
for i in range(len(tempval)):
    countries_list.append(POWER_CARBON(tempval[i][0],tempval[i][1]))

c.execute("""SELECT *
          FROM appliances""")
tempval=c.fetchall()
for i in range(len(tempval)):
    appliances_list.append(APPLIANCE(tempval[i][0],tempval[i][1]))

c.execute("""SELECT *
          FROM Travel""")
tempval=c.fetchall()
for i in range(len(tempval)):
    trips_list.append(TRIP(tempval[i][0],tempval[i][1]))

numOfDays()
score_calc()




prev_app=[]
c.execute("""SELECT Logs 
            FROM Track""")
tempval=c.fetchall()
for i in range(len(tempval)):
    prev_app.append(tempval[i][0])

c.execute("""SELECT Country
        FROM Total """)
tempval=c.fetchall()[0][0]
if str(tempval)=='0':
    count_setup(1)






