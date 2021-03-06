import psycopg2
from psycopg2 import Error
import psycopg2.extras
from flask import request
from scipy.integrate import odeint
import numpy as np
import datetime

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from zoneinfo import ZoneInfo
import time

app = Flask(__name__)

def bulk_query(bulk_query):
    connection = psycopg2.connect(user="mwtnjzht",
                                password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                host="john.db.elephantsql.com",
                                port="5432",
                                database="mwtnjzht")
    cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute(bulk_query)
    connection.commit()
    cursor.close()
    connection.close()

def query(query_string):
    try:
        connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")
        cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cursor.execute(query_string)
        record = cursor.fetchall()
        return record

    except (Exception, Error) as error:
        return []
    finally:
        if (connection):
            cursor.close()
            connection.close()

def insert(id, insert_string):
    connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")

    connection.autocommit = True
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO initialvalue VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'" + str(id) + "')", insert_string)
 
    connection.commit()
    connection.close()

def insertcalulate(insert_string):
    connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")

    connection.autocommit = True
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO updatesomenode VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", insert_string)
    


    
    connection.commit()
    connection.close()

def insertcal(s,v1,v2,i,r,h,d,m,timestamp,date):
    connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")

    connection.autocommit = True
    # cursor = connection.cursor()
    # cursor.executemany("INSERT INTO calculatemodel VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", insert_string)

    sql_string = "INSERT INTO calculatemodel (s, v1, v2, i, r, h, d, m, timestamp, date) VALUES( \'" + str(s) + "\',\'" + str(v1) + "\', \'" + str(v2) + "\',  \'" + str(i) + "\',  \'" + str(r) + "\',  \'" + str(h) + "\',  \'" + str(d) + "\',  \'" + str(m) + "\', \'" + str(timestamp) + "\' ,\'" + str(date) + "\');"
    print(sql_string)
 
    connection.commit()
    connection.close()

def updatecal(s,v1,v2,i,r,h,d,m,timestamp,date):
    connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")

    connection.autocommit = True
    cursor = connection.cursor()
    sql = ''' update  calculatemodel  set
          s = %s, v1 = %s, v2 = %s, i = %s, r = %s, h = %s, d = %s, m = %s, timestamp = %s
        where date = %s;'''
  
    cursor.execute(sql,(s,v1,v2,i,r,h,d,m,timestamp,date))
 
    connection.commit()
    connection.close()

def updatecalculate(s,v1,v2,i,r,h,d,m,timestamp,date):
    connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")

    connection.autocommit = True
    cursor = connection.cursor()
    sql = ''' update  updatesomenode  set
          s = %s, v1 = %s, v2 = %s, i = %s, r = %s, h = %s, d = %s, m = %s, timestamp = %s
        where date = %s;'''
  
    cursor.execute(sql,(s,v1,v2,i,r,h,d,m,timestamp,date))
    string = "UPDATE updatesomenode SET s = \'" + str(s) + "\',v1 = \'" + str(v1) + "\', v2 = \'" + str(v2) + "\', i = \'" + str(i) + "\', r = \'" + str(r) + "\', h = \'" + str(h) + "\', d = \'" + str(d) + "\', m = \'" + str(m) + "\', timestamp =\'" + str(timestamp) + "\' WHERE date = \'" + str(date) + "\';"
    print(string)
 
    connection.commit()
    connection.close()    

def update_query(id,s,v1,v2,i,r,h,d,m,timestamp,date):
    query_string = "UPDATE updatesomenode SET s = \'" + str(s) + "\',v1 = \'" + str(v1) + "\', v2 = \'" + str(v2) + "\', i = \'" + str(i) + "\', r = \'" + str(r) + "\', h = \'" + str(h) + "\', d = \'" + str(d) + "\', m = \'" + str(m) + "\', timestamp =\'" + str(timestamp) + "\' WHERE date = \'" + str(date) + "\' AND id = '" + str(id) + "';"
    return query_string

def insert_query(s,v1,v2,i,r,h,d,m,timestamp,date):
    sql_string = "INSERT INTO calculatemodel (s, v1, v2, i, r, h, d, m, timestamp, date) VALUES( \'" + str(s) + "\',\'" + str(v1) + "\', \'" + str(v2) + "\',  \'" + str(i) + "\',  \'" + str(r) + "\',  \'" + str(h) + "\',  \'" + str(d) + "\',  \'" + str(m) + "\', \'" + str(timestamp) + "\' ,\'" + str(date) + "\');"
    return  sql_string

def check_if_id_already_exist(id):
    check_previous = query("SELECT * FROM public.idlist WHERE id = '" + str(id) + "';")

    if (len(check_previous) == 0): 
        return False
    else:
        return True

def setlock(lock):
    connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")

    connection.autocommit = True
    cursor = connection.cursor()
    sql = ''' update  threadlock  set
          lock = %s'''
  
    cursor.execute(sql,(lock))
 
    connection.commit()
    connection.close()    

def monthToMonthName(month):
    if (month == 1):
        return "January"
    
    if (month == 2):
        return "February"
    
    if (month == 3):
        return "March"
    
    if (month == 4):
        return "April"
    
    if (month == 5):
        return "May"
    
    if (month == 6):
        return "June"
    
    if (month == 7):
        return "July"
    
    if (month == 8):
        return "August"
    
    if (month == 9):
        return "September"
    
    if (month == 10):
        return "October"
    
    if (month == 11):
        return "November"
    
    return "December"

@app.route("/coviddata/day")
@cross_origin()
def day():
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")
    
    s = 66186727
    i = 0
    result = []
    
    while i < len(dailycase_data):
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
            
        sus = s - (vaccine_data[i]["vaccines1"] + dailycase_data[i]["infected"] + dailycase_data[i]["recovery1"] + dailycase_data[i]["hospital"] + dailycase_data[i]["deaths"])
        # query("UPDATE dailycase SET susceptible = \'" + str(sus) + "\' WHERE date = \'" + date_string + "\';")
        # print("UPDATE dailycase SET susceptible = \'" + str(sus) + "\' WHERE date = \'" + date_string + "\';")
        result.append({
            "name": str(dailycase_data[i]["name"]),
            "Susceptible": int(sus),
            "Infected": int(dailycase_data[i]["infected"]) - int(dailycase_data[i]["recovery1"]),
            # "Recovery": int(dailycase_data[i]["recovery"]),
            "Hospital": int(dailycase_data[i]["hospital"]),
            "Deaths": int(dailycase_data[i]["deaths"]),
            "Vaccine1": int(vaccine_data[i]["vaccines1"]) - int(vaccine_data[i]["vaccines2"]),
            "Vaccine2": int(vaccine_data[i]["vaccines2"]) - int(vaccine_data[i]["vaccines3"]),
            "Maintenance":int(dailycase_data[i]["recovery1"])+int(vaccine_data[i]["vaccines3"]),
            # "Vaccines3": vaccine_data[i]["vaccines3"]
        })
            
        i = i + 1  
        
    return jsonify({
        "data": result
    })
    
@app.route("/coviddata/week")
@cross_origin()
def week():
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible as susceptible FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")

    i = 0
    day = 1
    month = 1
    week = 1
    
    year = -1
    
    infected = 0
    recovery = 0
    hospital = 0
    deaths = 0
    vaccines1 = 0
    vaccines2 = 0
    susceptible = 0
    recovery1 = 0
    vaccines3 = 0
    maintenance = 0
    # s = 463307089
    # sus = 0

    infectedm = 0
    vaccines1m = 0
    vaccines2m = 0
    
    result = []
    
    while i < len(dailycase_data):
        
        pass_condition = False
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
        if (i == 0):
            year = splited_date_string[0]
        
        if (int(splited_date_string[2]) != day):
            
            pass_condition = True
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                # "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
                "Year": str(year)
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            susceptible = 0
            recovery1 = 0
            vaccines3 = 0
            maintenance = 0

            infectedm = 0
            vaccines1m = 0
            vaccines2m = 0
          
            day = 1
            month = month + 1
            week = 1

        if (splited_date_string[0] != year):
            month = 1
            year = splited_date_string[0]
        
        
        if ((day % 7) != 0):

            infectedm = infectedm + int(dailycase_data[i]["infected"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            infected = infectedm - recovery1

            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])

            vaccines1m = vaccines1m + int(vaccine_data[i]["vaccines1"])
            vaccines2m = vaccines2m + int(vaccine_data[i]["vaccines2"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            vaccines1 = vaccines1m - vaccines2m

            vaccines2 = vaccines2m - vaccines3
            maintenance = vaccines3 + recovery1

            day = day + 1
            
        else:

            pass_condition = True
            
            infectedm = infectedm + int(dailycase_data[i]["infected"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            infected = infectedm - recovery1

            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])

            vaccines1m = vaccines1m + int(vaccine_data[i]["vaccines1"])
            vaccines2m = vaccines2m + int(vaccine_data[i]["vaccines2"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            vaccines1 = vaccines1m - vaccines2m

            vaccines2 = vaccines2m - vaccines3
            maintenance = vaccines3 + recovery1
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                # "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
                "Year": str(year)
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            susceptible = 0
            recovery1 = 0
            vaccines3 = 0
            maintenance = 0

            infectedm = 0
            vaccines1m = 0
            vaccines2m = 0

            week = week + 1
            day = day + 1
            
        if (i == len(dailycase_data) - 1 and not pass_condition):
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                # "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
                "Year": str(year)
            })
            
        i = i + 1        
    
    return jsonify({
        "data": result
    })
    
@app.route("/coviddata/month")
@cross_origin()
def month():
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible as susceptible FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")
    
    i = 0
    month = 1
    
    year = -1
    
    infected = 0
    recovery = 0
    hospital = 0
    deaths = 0
    vaccines1 = 0
    vaccines2 = 0
    susceptible = 0
    recovery1 = 0
    vaccines3 = 0
    maintenance = 0
    
    infectedm = 0
    vaccines1m = 0
    vaccines2m = 0
    
    result = []
    
    while i < len(dailycase_data):
        
        pass_condition = False
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
            
        if (i == 0):
            year = splited_date_string[0]
                  
        if (int(splited_date_string[1]) != month):
                
            pass_condition = True
                     
            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                # "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            susceptible = 0
            recovery1 = 0
            vaccines3 = 0
            maintenance = 0

            infectedm = 0
            vaccines1m = 0
            vaccines2m = 0
            
            infectedm = infectedm + int(dailycase_data[i]["infected"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            infected = infectedm - recovery1

            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])

            vaccines1m = vaccines1m + int(vaccine_data[i]["vaccines1"])
            vaccines2m = vaccines2m + int(vaccine_data[i]["vaccines2"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            vaccines1 = vaccines1m - vaccines2m

            vaccines2 = vaccines2m - vaccines3
            maintenance = vaccines3 + recovery1
            
            if (splited_date_string[0] != year):
                month = 1
                year = splited_date_string[0]
            else:
                month = month + 1
            
        else:
            infectedm = infectedm + int(dailycase_data[i]["infected"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            infected = infectedm - recovery1

            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])

            vaccines1m = vaccines1m + int(vaccine_data[i]["vaccines1"])
            vaccines2m = vaccines2m + int(vaccine_data[i]["vaccines2"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            vaccines1 = vaccines1m - vaccines2m

            vaccines2 = vaccines2m - vaccines3
            maintenance = vaccines3 + recovery1
            
            
        if (i == len(dailycase_data) - 1 and not pass_condition):

            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                # "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
            })
    
        i = i + 1
    
    return jsonify({
        "data": result
    })

beta = 1
zetas = 1
zetah = 1
omega1= 1
omega2= 1
omega3= 1
epsilon1= 1
epsilon2= 1
mu= 1
alpha= 1
lambdas= 1
lambdah= 1
length=1

def odes(x, t):

    # assign each ODE to a vector element
    S = x[0];
    V1 = x[1];
    V2 = x[2];
    I = x[3];
    R = x[4];
    H = x[5];
    M = x[6];

    # define each ODE
    dSdt = - beta*S*I - omega1*S - mu*S
    dV1dt = omega1*S - omega2*V1 - beta*(1-epsilon1)*V1*I - mu*V1
    dV2dt = omega2*V1 - omega3*V2 - beta*(1-epsilon2)*V2*I - mu*V2
    dMdt = omega3*V2 + R - beta*(1-epsilon2)*M*I - mu*M
    dIdt = beta*S*I + beta*(1-epsilon1)*V1*I + beta*(1-epsilon2)*V2*I + beta*(1-epsilon2)*M*I - alpha*I -lambdas*I - zetas*I
    dHdt = alpha*I - lambdah*I - zetah*H
    dRdt = lambdas*I + lambdah*H -R
    dDdt = zetas*I +zetah*H

    return[dSdt,dV1dt,dV2dt,dIdt,dRdt,dHdt,dMdt,dDdt]    
 
@app.route("/covidmodel/<id>" , methods=['PUT','GET'])
@cross_origin()
def input_request(id):

    if (check_if_id_already_exist(id) == False):
        return "false"

    global beta
    global zetas
    global zetah 
    global omega1
    global omega2
    global omega3
    global epsilon1
    global epsilon2
    global mu
    global alpha
    global lambdas
    global lambdah

    if request.method == 'PUT':

        start = request.get_json()["start_date"]
        beta = request.get_json()["beta"]
        zetas = request.get_json()["zetas"]
        zetah = request.get_json()["zetah"]
        omega1= request.get_json()["omega1"]
        omega2= request.get_json()["omega2"]
        omega3= request.get_json()["omega3"]
        epsilon1= request.get_json()["epsilon1"]
        epsilon2= request.get_json()["epsilon2"]
        mu= request.get_json()["mu"]
        alpha= request.get_json()["alpha"]
        lambdas= request.get_json()["lambdas"]
        lambdah= request.get_json()["lambdah"]

        beta = float(beta)
        zetas = float(zetas)
        zetah = float(zetah)
        omega1= float( omega1)
        omega2= float(omega2)
        omega3= float( omega3)
        epsilon1= float(epsilon1)
        epsilon2= float(epsilon2)
        mu= float(mu)
        alpha= float(alpha)
        lambdas= float(lambdas)
        lambdah= float(lambdah)

        date_start = datetime.datetime.strptime(start, "%Y-%m-%d")

        dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible  FROM dailycase WHERE date = \'" + start + "\' ORDER BY date ASC;")
        vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata WHERE date = \'" + start + "\' ORDER BY date ASC;")

        x0 = [int(dailycase_data[0]["susceptible"]),int(vaccine_data[0]["vaccines1"]) - int(vaccine_data[0]["vaccines2"]),int(vaccine_data[0]["vaccines2"]) - int(vaccine_data[0]["vaccines3"]),int(dailycase_data[0]["infected"]) - int(dailycase_data[0]["recovery1"]),int(dailycase_data[0]["recovery"]),int(dailycase_data[0]["hospital"]),int(dailycase_data[0]["recovery1"]) + int(vaccine_data[0]["vaccines3"]),int(dailycase_data[0]["deaths"])]
        # x0=[int(dailycase_data[0]["susceptible"]),int(calculate_data[0]["vaccines1"]) - int(calculate_data[0]["vaccines2"]),int(calculate_data[0]["vaccines2"]) - int(vaccine_data[0]["vaccines3"]),int(calculate_data[0]["infected"]) - int(dailycase_data[0]["recovery1"]),int(dailycase_data[0]["recovery"]),int(dailycase_data[0]["hospital"]),int(dailycase_data[0]["recovery1"]) + int(vaccine_data[0]["vaccines3"]),int(dailycase_data[0]["deaths"])]
        
        length = 16
        t = np.linspace(0, length - 1, length)
        output = odeint(odes,x0,t)

        i = 0
        result = []

        update_query_string = ""
        

        for i in range(length):  

            date_1 = date_start + datetime.timedelta(days=i)
            date_string = str(date_1)
            splited_date_string = date_string.split(sep = " ")
            
            result.append({
                "name": str(splited_date_string[0]), 
                "Susceptible": float(output[i][0]),
                "Infected": float(output[i][3]),
                "Recovery": float(output[i][4]),
                "Hospital": float(output[i][5]),
                "Deaths": float(output[i][7]),
                "Vaccine1": float(output[i][1]),
                "Vaccine2": float(output[i][2]),
                "Maintenance": float(output[i][6]),
                # "test": str(dailycase_data[i]["name"])
            })
            update_query_string = update_query_string + update_query(id, float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
            
        bulk_query(update_query_string)   
        json = (beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah, datetime.datetime.now(ZoneInfo('Asia/Bangkok')), start)
        insert(id, [json])

        print("sucess")
        
        
        initialresult = [] 
        initialresult.append({
            "name": str(start),
            "beta": float(beta),
            "zetas": float(zetas),
            "zetah": float(zetah),
            "omega1": float(omega1),
            "omega2": float(omega2),
            "omega3": float(omega3),
            "epsilon1": float(epsilon1),
            "epsilon2": float(epsilon2),
            "mu": float(mu),
            "alpha": float(alpha),
            "lambdas": float(lambdas),
            "lambdah": float(lambdah),
        })

        return jsonify({
            "initial_value": initialresult
        })

    else:
        all_data = query("SELECT name, beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah FROM initialvalue WHERE id = '" + str(id) + "' ORDER BY date DESC;")

        i = 0
        result = []

        already = set()
    
        while i < len(all_data):
            if str((all_data[i]["name"])) in already:
                i = i + 1 
                continue
            else:
                already.add(str((all_data[i]["name"])))
                result.append({
                    "name": str((all_data[i]["name"])),
                    "beta": float(all_data[i]["beta"]),
                    "zetas": float(all_data[i]["zetas"]),
                    "zetah": float(all_data[i]["zetah"]),
                    "omega1": float(all_data[i]["omega1"]),
                    "omega2": float(all_data[i]["omega2"]),
                    "omega3": float(all_data[i]["omega3"]),
                    "epsilon1": float(all_data[i]["epsilon1"]),
                    "epsilon2": float(all_data[i]["epsilon2"]),
                    "mu": float(all_data[i]["mu"]),
                    "alpha": float(all_data[i]["alpha"]),
                    "lambdas": float(all_data[i]["lambdas"]),
                    "lambdah": float(all_data[i]["lambdah"]),
                })

            i = i + 1 
                
        return jsonify({
            "initial_default": result,
        })

@app.route("/covidmodel/getdefault")
@cross_origin()
def get_default():
    all_data = query("SELECT name, beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah FROM public.default;")

    i = 0
    result = []

    while i < len(all_data):
        result.append({
            "name": str((all_data[i]["name"])),
            "beta": float(all_data[i]["beta"]),
            "zetas": float(all_data[i]["zetas"]),
            "zetah": float(all_data[i]["zetah"]),
            "omega1": float(all_data[i]["omega1"]),
            "omega2": float(all_data[i]["omega2"]),
            "omega3": float(all_data[i]["omega3"]),
            "epsilon1": float(all_data[i]["epsilon1"]),
            "epsilon2": float(all_data[i]["epsilon2"]),
            "mu": float(all_data[i]["mu"]),
            "alpha": float(all_data[i]["alpha"]),
            "lambdas": float(all_data[i]["lambdas"]),
            "lambdah": float(all_data[i]["lambdah"]),
        })

        i = i + 1 
            
    return jsonify({
        "initial_default": result
    })


# @app.route("/eiei")
# @cross_origin()
# def eieie():

#     default_values = query("SELECT * FROM public.default")
#     for i in default_values:
        
#         break
#     return generate_insert_query(i)

def generate_insert_query(id, data):
    sql_string = "INSERT INTO initialvalue (id, beta, zetas, zetah, omega1,omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdah, lambdas, date, name) VALUES('" + str(id) + "', \'" + str(data['beta']) + "\',\'" + str(data['zetas']) + "\', \'" + str(data['zetah']) + "\',  \'" + str(data['omega1']) + "\',  \'" + str(data['omega2']) + "\',  \'" + str(data['omega3']) + "\',  \'" + str(data['epsilon1']) + "\',  \'" + str(data['epsilon2']) + "\', \'" + str(data['mu']) + "\' ,\'" + str(data['alpha']) + "\',\'" + str(data['lambdah']) + "\',\'" + str(data['lambdas']) + "\',\'" + str(datetime.datetime.now(ZoneInfo('Asia/Bangkok'))) + "\',\'" + str(data['name']) + "\');"
    return sql_string
   
@app.route("/covidmodel/reset/<id>")
@cross_origin()
def input_reset(id):

    if (check_if_id_already_exist(id) == False):
        return "false"

    initial_query_string = ""
    
    default_values = query("SELECT * FROM public.default")

    for i in default_values:
        initial_query_string = initial_query_string + generate_insert_query(id, i)

    bulk_query(initial_query_string)

    global beta
    global zetas
    global zetah 
    global omega1
    global omega2
    global omega3
    global epsilon1
    global epsilon2
    global mu
    global alpha
    global lambdas
    global lambdah

    all_data = query("SELECT name, beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah FROM public.default ORDER BY name ASC;")
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible  FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")

    i = 0
    j = 0

    dailycase = len(dailycase_data)
    default = len(all_data)

    bulk_update_string = ""

    for i in range(dailycase):
        for j in range(default):
        
            if str(all_data[j]["name"]) == str(dailycase_data[i]["name"]) and str(all_data[j]["name"]) == str(vaccine_data[i]["name"]):
                start = str(all_data[j]["name"])
                beta = float(all_data[j]["beta"])
                zetas = float(all_data[j]["zetas"])
                zetah = float(all_data[j]["zetah"])
                omega1 = float(all_data[j]["omega1"])
                omega2 = float(all_data[j]["omega2"])
                omega3 = float(all_data[j]["omega3"])
                epsilon1 = float(all_data[j]["epsilon1"])
                epsilon2 = float(all_data[j]["epsilon2"])
                mu = float(all_data[j]["mu"])
                alpha = float(all_data[j]["alpha"])
                lambdas = float(all_data[j]["lambdas"])
                lambdah = float(all_data[j]["lambdah"])

                
                x0=[int(dailycase_data[i]["susceptible"]),int(vaccine_data[i]["vaccines1"]) - int(vaccine_data[i]["vaccines2"]),int(vaccine_data[i]["vaccines2"]) - int(vaccine_data[i]["vaccines3"]),int(dailycase_data[i]["infected"]) - int(dailycase_data[i]["recovery1"]),int(dailycase_data[i]["recovery"]),int(dailycase_data[i]["hospital"]),int(dailycase_data[i]["recovery1"]) + int(vaccine_data[i]["vaccines3"]),int(dailycase_data[i]["deaths"])]

                length = 16
                t = np.linspace(0, length - 1, length)
                output = odeint(odes,x0,t)

                i = 0
                result = [] 
                
                date_start = datetime.datetime.strptime(start, "%Y-%m-%d")   

                for i in range(length):  

                    date_1 = date_start + datetime.timedelta(days=i)
                    date_string = str(date_1)
                    splited_date_string = date_string.split(sep = " ")
                    
                    result.append({
                        "name": str(splited_date_string[0]), 
                        "Susceptible": float(output[i][0]),
                        "Infected": float(output[i][3]),
                        "Recovery": float(output[i][4]),
                        "Hospital": float(output[i][5]),
                        "Deaths": float(output[i][7]),
                        "Vaccine1": float(output[i][1]),
                        "Vaccine2": float(output[i][2]),
                        "Maintenance": float(output[i][6]),
                        # "test": str(dailycase_data[i]["name"])
                    })

                    # result1 = (float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    result1 = (float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    bulk_update_string = bulk_update_string + update_query(id, float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    # model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM calculatemodel WHERE date = '" + date_string + "';")
                    
                    # if len(model_data) != 0:
                    #     # updatecal(int(output[i][0]),int(output[i][1]),int(output[i][2]),int(output[i][3]),int(output[i][4]),int(output[i][5]),int(output[i][7]),int(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    #     bulk_update_string = bulk_update_string + update_query(float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    # else:
                    #     bulk_insert_string = bulk_insert_string + insert_query(float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
    print ("calculate sucess")
    bulk_query(bulk_update_string)
    return "reset success"

@app.route("/createuserid")
@cross_origin()
def createuserid():
    connection = psycopg2.connect(user="mwtnjzht",
                                password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                host="john.db.elephantsql.com",
                                port="5432",
                                database="mwtnjzht")
    cursor = connection.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    cursor.execute("INSERT INTO public.idlist (date) VALUES(now()) RETURNING id;")
    id = cursor.fetchone()["id"]
    connection.commit()
    
    cursor.close()
    connection.close()

    initial_query_string = ""
    
    default_values = query("SELECT * FROM public.default")

    for i in default_values:
        initial_query_string = initial_query_string + generate_insert_query(id, i)

    bulk_query(initial_query_string)

    global beta
    global zetas
    global zetah 
    global omega1
    global omega2
    global omega3
    global epsilon1
    global epsilon2
    global mu
    global alpha
    global lambdas
    global lambdah

    all_data = query("SELECT name, beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah FROM public.default ORDER BY name ASC;")
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible  FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")

    i = 0
    j = 0

    dailycase = len(dailycase_data)
    default = len(all_data)

    bulk_update_string = ""

    for i in range(dailycase):
        for j in range(default):
        
            if str(all_data[j]["name"]) == str(dailycase_data[i]["name"]) and str(all_data[j]["name"]) == str(vaccine_data[i]["name"]):
                start = str(all_data[j]["name"])
                beta = float(all_data[j]["beta"])
                zetas = float(all_data[j]["zetas"])
                zetah = float(all_data[j]["zetah"])
                omega1 = float(all_data[j]["omega1"])
                omega2 = float(all_data[j]["omega2"])
                omega3 = float(all_data[j]["omega3"])
                epsilon1 = float(all_data[j]["epsilon1"])
                epsilon2 = float(all_data[j]["epsilon2"])
                mu = float(all_data[j]["mu"])
                alpha = float(all_data[j]["alpha"])
                lambdas = float(all_data[j]["lambdas"])
                lambdah = float(all_data[j]["lambdah"])

                
                x0=[int(dailycase_data[i]["susceptible"]),int(vaccine_data[i]["vaccines1"]) - int(vaccine_data[i]["vaccines2"]),int(vaccine_data[i]["vaccines2"]) - int(vaccine_data[i]["vaccines3"]),int(dailycase_data[i]["infected"]) - int(dailycase_data[i]["recovery1"]),int(dailycase_data[i]["recovery"]),int(dailycase_data[i]["hospital"]),int(dailycase_data[i]["recovery1"]) + int(vaccine_data[i]["vaccines3"]),int(dailycase_data[i]["deaths"])]

                length = 16
                t = np.linspace(0, length - 1, length)
                output = odeint(odes,x0,t)

                i = 0
                result = [] 
                
                date_start = datetime.datetime.strptime(start, "%Y-%m-%d")   

                for i in range(length):  

                    date_1 = date_start + datetime.timedelta(days=i)
                    date_string = str(date_1)
                    splited_date_string = date_string.split(sep = " ")
                    
                    result.append({
                        "name": str(splited_date_string[0]), 
                        "Susceptible": float(output[i][0]),
                        "Infected": float(output[i][3]),
                        "Recovery": float(output[i][4]),
                        "Hospital": float(output[i][5]),
                        "Deaths": float(output[i][7]),
                        "Vaccine1": float(output[i][1]),
                        "Vaccine2": float(output[i][2]),
                        "Maintenance": float(output[i][6]),
                        # "test": str(dailycase_data[i]["name"])
                    })

                    # result1 = (float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    result1 = (float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    bulk_update_string = bulk_update_string + update_query(id, float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    # model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM calculatemodel WHERE date = '" + date_string + "';")
                    
                    # if len(model_data) != 0:
                    #     # updatecal(int(output[i][0]),int(output[i][1]),int(output[i][2]),int(output[i][3]),int(output[i][4]),int(output[i][5]),int(output[i][7]),int(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    #     bulk_update_string = bulk_update_string + update_query(float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
                    # else:
                    #     bulk_insert_string = bulk_insert_string + insert_query(float(output[i][0]),float(output[i][1]),float(output[i][2]),float(output[i][3]),float(output[i][4]),float(output[i][5]),float(output[i][7]),float(output[i][6]),datetime.datetime.now(ZoneInfo('Asia/Bangkok')),str(splited_date_string[0]))
    print ("successfully added initial values")
    bulk_query(bulk_update_string)

    return jsonify({
        "id": id
    })

@app.route("/deleteuserid")
@cross_origin()
def deleteuserid():
    from datetime import datetime, timedelta, tzinfo
    id_list = query("SELECT * FROM idlist")
    remove_list = []

    for each in id_list:

        current_time = datetime.utcnow() + timedelta(hours=-10)
        if each["date"].replace(tzinfo=None) <= current_time:
            remove_list.append(each["id"])

    for each_id in remove_list:
        bulk_query("DELETE FROM public.idlist WHERE id = '" + str(each_id) + "';DELETE FROM public.initialvalue WHERE id = '" + str(each_id) + "';DELETE FROM public.updatesomenode WHERE id = '" + str(each_id) + "';")

    return jsonify(remove_list)

def insert_if_not_already_in_table(id):
    check_previous = query("SELECT * FROM updatesomenode WHERE id = '" + str(id) + "';")

    if (len(check_previous) == 0):
        query_string = ""
        result = query("SELECT * FROM calculatemodel")

        for each in result:
            kkk = "null" if each["timestamp"] == None else ("'" + str(each["timestamp"]) + "'")
            query_string += "INSERT INTO public.updatesomenode(s, v1, v2, i, r, h, d, m, \"timestamp\", date, id) VALUES ('" + str(each["s"]) + "', '" + str(each["v1"]) + "', '" + str(each["v2"]) + "', '" + str(each["i"]) + "', '" + str(each["r"]) + "', '" + str(each["h"]) + "', '" + str(each["d"]) + "', '" + str(each["m"]) + "', " + kkk + ", '" + str(each["date"]) + "', '" + str(id) + "');"
        
        bulk_query(query_string)
        print("First time " + str(id))
    

    


@app.route("/covidmodel/day/<id>")
@cross_origin()
def modelday(id):

    if (check_if_id_already_exist(id) == False):
        return "false"

    insert_if_not_already_in_table(id)
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM updatesomenode WHERE id = '" + str(id) + "' ORDER BY date ASC;")
    
    
    i = 0
    result = []
    
    while i < len(model_data):
        
        result.append({
            "name": str(model_data[i]["name"]),
            "Susceptible": int(model_data[i]["susceptible"]),
            "Infected": int(model_data[i]["infected"]),
            # "Recovery": int(model_data[i]["recovery"]),
            "Hospital": int(model_data[i]["hospital"]),
            "Deaths": int(model_data[i]["deaths"]),
            "Vaccine1": int(model_data[i]["vaccines1"]),
            "Vaccine2": int(model_data[i]["vaccines2"]),
            "Maintenance": int(model_data[i]["maintenance"]),
        })
            
        i = i + 1  
        
    return jsonify({
        "data": result
    })

@app.route("/covidmodel/month/<id>")
@cross_origin()
def modelmonth(id):

    if (check_if_id_already_exist(id) == False):
        return "false"

    insert_if_not_already_in_table(id)
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM updatesomenode WHERE id = '" + str(id) + "' ORDER BY date ASC;")
   
    i = 0
    month = 1
    
    year = -1
    
    infected = 0
    recovery = 0
    hospital = 0
    deaths = 0
    vaccines1 = 0
    vaccines2 = 0
    susceptible = 0
    maintenance = 0
    
    result = []
    
    while i < len(model_data):
        
        pass_condition = False
        
        date_string = str(model_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
            
        if (i == 0):
            year = splited_date_string[0]
                  
        if (int(splited_date_string[1]) != month):
                
            pass_condition = True

            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                # "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            susceptible = 0
            maintenance = 0
            
            infected = infected + int(model_data[i]["infected"])
            recovery = recovery + int(model_data[i]["recovery"])
            hospital = hospital + int(model_data[i]["hospital"])
            deaths = deaths + int(model_data[i]["deaths"])
            vaccines1 = vaccines1 + int(model_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(model_data[i]["susceptible"])
            maintenance = maintenance + int(model_data[i]["maintenance"])
            
            if (splited_date_string[0] != year):
                month = 1
                year = splited_date_string[0]
            else:
                month = month + 1
            
        else:
            infected = infected + int(model_data[i]["infected"])
            recovery = recovery + int(model_data[i]["recovery"])
            hospital = hospital + int(model_data[i]["hospital"])
            deaths = deaths + int(model_data[i]["deaths"])
            vaccines1 = vaccines1 + int(model_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(model_data[i]["susceptible"])
            maintenance = maintenance + int(model_data[i]["maintenance"])
            
            
        if (i == len(model_data) - 1 and not pass_condition):

            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                # "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
            })
    
        i = i + 1
    
    return jsonify({
        "data": result
    })

@app.route("/vsdata/day/<id>")
@cross_origin()
def vsday(id):

    if (check_if_id_already_exist(id) == False):
        return "false"
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")
    
    insert_if_not_already_in_table(id)
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM updatesomenode WHERE id = '" + str(id) + "' ORDER BY date ASC;")
   
    i = 0
    result = []
    
    while i < len(dailycase_data):
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
        result.append({
            "name": str(dailycase_data[i]["name"]),
            "SusceptibleRawData": int(dailycase_data[i]["susceptible"]),
            "SusceptibleModelData": int(model_data[i]["susceptible"]),
            "InfectionRawData": int(dailycase_data[i]["infected"]) - int(dailycase_data[i]["recovery1"]),
            "InfectionModelData": int(model_data[i]["infected"]),
            # "RecoveryRawData": int(dailycase_data[i]["recovery"]),
            # "RecoveryModelData": int(model_data[i]["recovery"]),
            "HospitalizeRawData": int(dailycase_data[i]["hospital"]),
            "HospitalizeModelData": int(model_data[i]["hospital"]),
            "DeathRawData": int(dailycase_data[i]["deaths"]),
            "DeathModelData": int(model_data[i]["deaths"]),
            "Vaccines1RawData": int(vaccine_data[i]["vaccines1"]) - int(vaccine_data[i]["vaccines2"]),
            "Vaccines1ModelData": int(model_data[i]["vaccines1"]),
            "Vaccines2RawData": int(vaccine_data[i]["vaccines2"]) - int(vaccine_data[i]["vaccines3"]),
            "Vaccines2ModelData": int(model_data[i]["vaccines2"]),
            "MaintenanceShotRawData": int(dailycase_data[i]["recovery1"]) + int(vaccine_data[i]["vaccines3"]),
            "MaintenanceShotModelData": int(model_data[i]["maintenance"])

        })
            
        i = i + 1  
        
    return jsonify({
        "data": result
    })

@app.route("/vsdata/month/<id>")
@cross_origin()
def vsmonth(id):

    if (check_if_id_already_exist(id) == False):
        return "false"
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible as susceptible FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")
    
    insert_if_not_already_in_table(id)
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM updatesomenode WHERE id = '" + str(id) + "' ORDER BY date ASC;")
   
    i = 0
    month = 1
    
    year = -1
    
    infected = 0
    recovery = 0
    hospital = 0
    deaths = 0
    vaccines1 = 0
    vaccines2 = 0
    susceptible = 0
    recovery1 = 0
    vaccines3 = 0
    maintenance = 0

    infectedm = 0
    recoverym = 0
    hospitalm = 0
    deathsm = 0
    vaccines1m = 0
    vaccines2m = 0
    susceptiblem = 0
    maintenancem = 0

    infectedcal = 0
    vaccines1cal = 0
    vaccines2cal = 0
  
    result = []
    
    while i < len(dailycase_data):
        
        pass_condition = False
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
            
        if (i == 0):
            year = splited_date_string[0]
                  
        if (int(splited_date_string[1]) != month):
                
            pass_condition = True
                     
            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "SusceptibleRawData": int(susceptible),
                "SusceptibleModelData":int(susceptiblem),
                "InfectionRawData": int(infected),
                "InfectionModelData":int(infectedm),
                # "RecoveryRawData": int(recovery),
                # "RecoveryModelData":int(recoverym),
                "HospitalizeRawData": int(hospital),
                "HospitalizeModelData":int(hospitalm),
                "DeathRawData": int(deaths),
                "DeathModelData":int(deathsm),
                "Vaccines1RawData": int(vaccines1),
                "Vaccines1ModelData":int(vaccines1m),
                "Vaccines2RawData": int(vaccines2),
                "Vaccines2ModelData":int(vaccines2m),
                "MaintenanceShotRawData":int(maintenance),
                "MaintenanceShotModelData":int(maintenancem),
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            susceptible = 0
            recovery1 = 0
            vaccines3 = 0
            maintenance = 0

            infectedm = 0
            recoverym = 0
            hospitalm = 0
            deathsm = 0
            vaccines1m = 0
            vaccines2m = 0
            susceptiblem = 0
            maintenancem = 0

            infectedcal = 0
            vaccines1cal = 0
            vaccines2cal = 0
            
            # infected = infected + int(dailycase_data[i]["infected"])
            infectedcal = infectedcal + int(dailycase_data[i]["infected"])
            infectedm = infectedm + int(model_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            recoverym = recoverym + int(model_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            hospitalm = hospitalm + int(model_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            deathsm = deathsm + int(model_data[i]["deaths"])
            # vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines1cal = vaccines1cal + int(vaccine_data[i]["vaccines1"])
            vaccines1m = vaccines1m + int(model_data[i]["vaccines1"])
            # vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            vaccines2cal = vaccines2cal + int(vaccine_data[i]["vaccines2"])
            vaccines2m = vaccines2m + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            susceptiblem = susceptiblem + int(model_data[i]["susceptible"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            maintenance = vaccines3 + recovery1
            maintenancem = maintenancem + int(model_data[i]["maintenance"])
            infected = infectedcal -  recovery1
            vaccines1 = vaccines1cal - vaccines2cal
            vaccines2 = vaccines2cal - vaccines3
            
            if (splited_date_string[0] != year):
                month = 1
                year = splited_date_string[0]
            else:
                month = month + 1
            
        else:
            # infected = infected + int(dailycase_data[i]["infected"])
            infectedcal = infectedcal + int(dailycase_data[i]["infected"])
            infectedm = infectedm + int(model_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            recoverym = recoverym + int(model_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            hospitalm = hospitalm + int(model_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            deathsm = deathsm + int(model_data[i]["deaths"])
            # vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines1cal = vaccines1cal + int(vaccine_data[i]["vaccines1"])
            vaccines1m = vaccines1m + int(model_data[i]["vaccines1"])
            # vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            vaccines2cal = vaccines2cal + int(vaccine_data[i]["vaccines2"])
            vaccines2m = vaccines2m + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            susceptiblem = susceptiblem + int(model_data[i]["susceptible"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            maintenance = vaccines3 + recovery1
            maintenancem = maintenancem + int(model_data[i]["maintenance"])
            infected = infectedcal -  recovery1
            vaccines1 = vaccines1cal - vaccines2cal
            vaccines2 = vaccines2cal - vaccines3
            
            
        if (i == len(dailycase_data) - 1 and not pass_condition):

            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "SusceptibleRawData": int(susceptible),
                "SusceptibleModelData":int(susceptiblem),
                "InfectionRawData": int(infected),
                "InfectionModelData":int(infectedm),
                # "RecoveryRawData": int(recovery),
                # "RecoveryModelData":int(recoverym),
                "HospitalizeRawData": int(hospital),
                "HospitalizeModelData":int(hospitalm),
                "DeathRawData": int(deaths),
                "DeathModelData":int(deathsm),
                "Vaccines1RawData": int(vaccines1),
                "Vaccines1ModelData":int(vaccines1m),
                "Vaccines2RawData": int(vaccines2),
                "Vaccines2ModelData":int(vaccines2m),
                "MaintenanceShotRawData":int(maintenance),
                "MaintenanceShotModelData":int(maintenancem),
            })
    
        i = i + 1
    
    return jsonify({
        "data": result
    })

@app.route("/test")
@cross_origin()
def test():
    return "Status 200 ok"