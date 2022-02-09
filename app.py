import psycopg2
from psycopg2 import Error
import psycopg2.extras
from flask import request
from scipy.integrate import odeint
import numpy as np
import datetime

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)

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

def insert(insert_string):
    connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")

    connection.autocommit = True
    cursor = connection.cursor()
    cursor.executemany("INSERT INTO initialvalue VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", insert_string)
 
    connection.commit()
    connection.close()

def updatecal(date,s,v1,v2,i,r,h,d,m,timestamp):
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

@app.route("/coviddata" , methods=['POST'])
@cross_origin()
def data():
    
    start = request.get_json()["start_date"]     
    end = request.get_json()["end_date"]
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, hospitalized as hospital, deaths as deaths, susceptible, recovered as recovery1  FROM dailycase WHERE date BETWEEN \'" + start + "\' and \'" + end + "\' ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata WHERE date BETWEEN \'" + start + "\' and \'" + end + "\' ORDER BY date ASC;")
    

    i = 0
    result = []
    
    while i < len(dailycase_data):
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
        result.append({
            "name": str(dailycase_data[i]["name"]),
            "Susceptible": int(dailycase_data[i]["susceptible"]),
            "Infected": int(dailycase_data[i]["infected"]),
            "Recovery": int(dailycase_data[i]["recovery"]),
            "Hospital": int(dailycase_data[i]["hospital"]),
            "Deaths": int(dailycase_data[i]["deaths"]),
            "Vaccine1": int(vaccine_data[i]["vaccines1"]),
            "Vaccine2": int(vaccine_data[i]["vaccines2"]),
            "Maintenance":int(dailycase_data[i]["recovery1"])+int(vaccine_data[i]["vaccines3"]),
            # "test": str(dailycase_data[i]["name"])
        })
            
        i = i + 1       
    
    return jsonify({
         "data": result
    })
    
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
            "Infected": int(dailycase_data[i]["infected"]),
            "Recovery": int(dailycase_data[i]["recovery"]),
            "Hospital": int(dailycase_data[i]["hospital"]),
            "Deaths": int(dailycase_data[i]["deaths"]),
            "Vaccine1": int(vaccine_data[i]["vaccines1"]),
            "Vaccine2": int(vaccine_data[i]["vaccines2"]),
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
    
    result = []
    
    while i < len(dailycase_data):
        
        pass_condition = False
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
        if (i == 0):
            year = splited_date_string[0]
            
        if (splited_date_string[0] != year):
            month = 0
            year = splited_date_string[0]
        
        if (int(splited_date_string[2]) != day):
            
            pass_condition = True
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                "Recovery": int(recovery),
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
          
            
            day = 1
            month = month + 1
            week = 1
        
        
        if ((day % 7) != 0):
            infected = infected + int(dailycase_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            maintenance = vaccines3 + recovery1
            day = day + 1
            
        else:
            
            pass_condition = True
            
            infected = infected + int(dailycase_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            maintenance = vaccines3 + recovery1
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                "Recovery": int(recovery),
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
            recovery1 = 0
            vaccines3 = 0
            maintenance = 0

            week = week + 1
            day = day + 1
            
        if (i == len(dailycase_data) - 1 and not pass_condition):
            
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                "Recovery": int(recovery),
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
    # s = 2051788537
    # sus = 0
    
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
                "Recovery": int(recovery),
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
            
            infected = infected + int(dailycase_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            maintenance = vaccines3 + recovery1
            
            if (splited_date_string[0] != year):
                month = 1
                year = splited_date_string[0]
            else:
                month = month + 1
            
        else:
            infected = infected + int(dailycase_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            maintenance = vaccines3 + recovery1
            
            
        if (i == len(dailycase_data) - 1 and not pass_condition):

            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                "Recovery": int(recovery),
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
    
@app.route("/covidmodel" , methods=['GET','POST'])
@cross_origin()
def input_request():

    if request.method == 'POST':

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
        length = request.get_json()["tiime_length"]
        

        json = (beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah, datetime.datetime.now(), length, start)
        insert([json])
        return ""
    else:
        result = []
        i = 0
        initial_value = query("SELECT beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah, length FROM initialvalue ORDER BY date DESC LIMIT 1;")
    
        while i < len(initial_value):
            
            result.append({
                "beta": float(initial_value[i]["beta"]),
                "zetas": float(initial_value[i]["zetas"]),
                "zetah": float(initial_value[i]["zetah"]),
                "omega1": float(initial_value[i]["omega1"]),
                "omega2": float(initial_value[i]["omega2"]),
                "omega3": float(initial_value[i]["omega3"]),
                "epsilon1": float(initial_value[i]["epsilon1"]),
                "epsilon2": float(initial_value[i]["epsilon2"]),
                "mu": float(initial_value[i]["mu"]),
                "alpha": float(initial_value[i]["alpha"]),
                "lambdas": float(initial_value[i]["lambdas"]),
                "lambdah": float(initial_value[i]["lambdah"]),
                "time_length": int(initial_value[i]["length"]),
            })
                
            i = i + 1  
        #     print(result)
        # return ""
            
        return jsonify({
            "initial": result
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

@app.route("/calcovidmodel" , methods=['POST'])
@cross_origin()
def calcovidmodel():

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
    global length

    initial_value = query("SELECT beta, zetas, zetah, omega1, omega2, omega3, epsilon1, epsilon2, mu, alpha, lambdas, lambdah, length FROM initialvalue ORDER BY date DESC LIMIT 1;")
    beta = float(initial_value[0]["beta"])
    zetas = float(initial_value[0]["zetas"])
    zetah = float(initial_value[0]["zetah"])
    omega1 = float(initial_value[0]["omega1"])
    omega2 = float(initial_value[0]["omega2"])
    omega3 = float(initial_value[0]["omega3"])
    epsilon1 = float(initial_value[0]["epsilon1"])
    epsilon2 = float(initial_value[0]["epsilon2"])
    mu = float(initial_value[0]["mu"])
    alpha = float(initial_value[0]["alpha"])
    lambdas = float(initial_value[0]["lambdas"])
    lambdah = float(initial_value[0]["lambdah"])
    length = int(initial_value[0]["length"])
    
    # innitial conditions
    start = request.get_json()["start_date"]

    date_start = datetime.datetime.strptime(start, "%Y-%m-%d")
    # print(int(length))

    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible  FROM dailycase WHERE date = \'" + start + "\' ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata WHERE date = \'" + start + "\' ORDER BY date ASC;")
    
    i = 0
    result = []
    
    while i < len(dailycase_data):
        

        x0=[int(dailycase_data[i]["susceptible"]),int(vaccine_data[i]["vaccines1"]),int(vaccine_data[i]["vaccines2"]),int(dailycase_data[i]["infected"]),int(dailycase_data[i]["recovery"]),int(dailycase_data[i]["hospital"]),int(dailycase_data[i]["recovery1"]) + int(vaccine_data[i]["vaccines3"]),int(dailycase_data[i]["deaths"])]
        
        i = i + 1

    t = np.linspace(0,int(length) - 1,int(length))
    output = odeint(odes,x0,t)
    # print(t)
    

    for i in range(int(length)):  

        date_1 = date_start + datetime.timedelta(days=i)
        date_string = str(date_1)
        splited_date_string = date_string.split(sep = " ")
        
        result.append({
            "name": str(splited_date_string[0]), 
            "Susceptible": int(output[i][0]),
            "Infected": int(output[i][3]),
            "Recovery": int(output[i][4]),
            "Hospital": int(output[i][5]),
            "Deaths": int(output[i][7]),
            "Vaccine1": int(output[i][1]),
            "Vaccine2": int(output[i][2]),
            "Maintenance": int(output[i][6]),
            # "test": str(dailycase_data[i]["name"])
        })

        updatecal(str(splited_date_string[0]),int(output[i][0]),int(output[i][1]),int(output[i][2]),int(output[i][3]),int(output[i][4]),int(output[i][5]),int(output[i][7]),int(output[i][6]),datetime.datetime.now())
  
    # print(result)
    # return ""
    
    return jsonify({
         "data": result
    })

@app.route("/covidmodel/day")
@cross_origin()
def modelday():
    
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM calculatemodel ORDER BY date ASC;")
    
    
    i = 0
    result = []
    
    while i < len(model_data):
        
        result.append({
            "name": str(model_data[i]["name"]),
            "Susceptible": int(model_data[i]["susceptible"]),
            "Infected": int(model_data[i]["infected"]),
            "Recovery": int(model_data[i]["recovery"]),
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

@app.route("/covidmodel/week")
@cross_origin()
def modelweek():
    
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM calculatemodel ORDER BY date ASC;")
    
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
    maintenance = 0

    
    result = []
    
    while i < len(model_data):
        
        pass_condition = False
        
        date_string = str(model_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
        if (i == 0):
            year = splited_date_string[0]
            
        if (splited_date_string[0] != year):
            month = 0
            year = splited_date_string[0]
        
        if (int(splited_date_string[2]) != day):
            
            pass_condition = True
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
                "Year": str(year),
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            susceptible = 0
            maintenance = 0
          
            
            day = 1
            month = month + 1
            week = 1
        
        
        if ((day % 7) != 0):
            infected = infected + int(model_data[i]["infected"])
            recovery = recovery + int(model_data[i]["recovery"])
            hospital = hospital + int(model_data[i]["hospital"])
            deaths = deaths + int(model_data[i]["deaths"])
            vaccines1 = vaccines1 + int(model_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(model_data[i]["susceptible"])
            maintenance = maintenance + int(model_data[i]["maintenance"])
            
            day = day + 1
            
        else:
            
            pass_condition = True
            
            infected = infected + int(model_data[i]["infected"])
            recovery = recovery + int(model_data[i]["recovery"])
            hospital = hospital + int(model_data[i]["hospital"])
            deaths = deaths + int(model_data[i]["deaths"])
            vaccines1 = vaccines1 + int(model_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(model_data[i]["susceptible"])
            maintenance = maintenance + int(model_data[i]["maintenance"])
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
                "Year": str(year),
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            maintenance = 0
            
            week = week + 1
            day = day + 1
            
        if (i == len(model_data) - 1 and not pass_condition):
            

            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": int(susceptible),
                "Infected": int(infected),
                "Recovery": int(recovery),
                "Hospital": int(hospital),
                "Deaths": int(deaths),
                "Vaccine1": int(vaccines1),
                "Vaccine2": int(vaccines2),
                "Maintenance":int(maintenance),
                "Year": str(year),
            })
            
        i = i + 1        
    
    return jsonify({
        "data": result
    })

@app.route("/covidmodel/month")
@cross_origin()
def modelmonth():

    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM calculatemodel ORDER BY date ASC;")
   
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
                "Recovery": int(recovery),
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
                "Recovery": int(recovery),
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


@app.route("/vsdata/day")
@cross_origin()
def vsday():
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM calculatemodel ORDER BY date ASC;")
   
    s = 66186727
    i = 0
    result = []
    
    while i < len(dailycase_data):
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
            
        sus = s - (vaccine_data[i]["vaccines1"] + dailycase_data[i]["infected"] + dailycase_data[i]["recovery"] + dailycase_data[i]["hospital"] + dailycase_data[i]["deaths"])

        result.append({
            "name": str(dailycase_data[i]["name"]),
            "SusceptibleRawData": int(sus),
            "SusceptibleModelData": int(model_data[i]["susceptible"]),
            "InfectionRawData": int(dailycase_data[i]["infected"]),
            "InfectionModelData": int(model_data[i]["infected"]),
            "RecoveryRawData": int(dailycase_data[i]["recovery"]),
            "RecoveryModelData": int(model_data[i]["recovery"]),
            "HospitalizeRawData": int(dailycase_data[i]["hospital"]),
            "HospitalizeModelData": int(model_data[i]["hospital"]),
            "DeathRawData": int(dailycase_data[i]["deaths"]),
            "DeathModelData": int(model_data[i]["deaths"]),
            "Vaccines1RawData": int(vaccine_data[i]["vaccines1"]),
            "Vaccines1ModelData": int(model_data[i]["vaccines1"]),
            "Vaccines2RawData": int(vaccine_data[i]["vaccines2"]),
            "Vaccines2ModelData": int(model_data[i]["vaccines2"]),
            "MaintenanceShotRawData": int(dailycase_data[i]["recovery1"]) + int(vaccine_data[i]["vaccines3"]),
            "MaintenanceShotModelData": int(model_data[i]["maintenance"])

        })
            
        i = i + 1  
        
    return jsonify({
        "data": result
    })

@app.route("/vsdata/week")
@cross_origin()
def vsweek():
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible as susceptible FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM calculatemodel ORDER BY date ASC;")
   
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

    infectedm = 0
    recoverym = 0
    hospitalm = 0
    deathsm = 0
    vaccines1m = 0
    vaccines2m = 0
    susceptiblem = 0
    maintenancem = 0
    
    result = []
    
    while i < len(dailycase_data):
        
        pass_condition = False
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
        if (i == 0):
            year = splited_date_string[0]
            
        if (splited_date_string[0] != year):
            month = 0
            year = splited_date_string[0]
        
        if (int(splited_date_string[2]) != day):
            
            pass_condition = True
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "SusceptibleRawData": int(susceptible),
                "SusceptibleModelData":int(susceptiblem),
                "InfectionRawData": int(infected),
                "InfectionModelData":int(infectedm),
                "RecoveryRawData": int(recovery),
                "RecoveryModelData":int(recoverym),
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
            recoverym = 0
            hospitalm = 0
            deathsm = 0
            vaccines1m = 0
            vaccines2m = 0
            susceptiblem = 0
            maintenancem = 0

            day = 1
            month = month + 1
            week = 1
        
        
        if ((day % 7) != 0):
            infected = infected + int(dailycase_data[i]["infected"])
            infectedm = infectedm + int(model_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            recoverym = recoverym + int(model_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            hospitalm = hospitalm + int(model_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            deathsm = deathsm + int(model_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines1m = vaccines1m + int(model_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            vaccines2m = vaccines2m + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            susceptiblem = susceptiblem + int(model_data[i]["susceptible"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            maintenance = vaccines3 + recovery1
            maintenancem = maintenancem + int(model_data[i]["maintenance"])
            
            day = day + 1
            
        else:
            
            pass_condition = True
            
            infected = infected + int(dailycase_data[i]["infected"])
            infectedm = infectedm + int(model_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            recoverym = recoverym + int(model_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            hospitalm = hospitalm + int(model_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            deathsm = deathsm + int(model_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines1m = vaccines1m + int(model_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            vaccines2m = vaccines2m + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            susceptiblem = susceptiblem + int(model_data[i]["susceptible"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            maintenance = vaccines3 + recovery1
            maintenancem = maintenancem + int(model_data[i]["maintenance"])
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "SusceptibleRawData": int(susceptible),
                "SusceptibleModelData":int(susceptiblem),
                "InfectionRawData": int(infected),
                "InfectionModelData":int(infectedm),
                "RecoveryRawData": int(recovery),
                "RecoveryModelData":int(recoverym),
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
            recoverym = 0
            hospitalm = 0
            deathsm = 0
            vaccines1m = 0
            vaccines2m = 0
            susceptiblem = 0
            maintenancem = 0

            week = week + 1
            day = day + 1
            
        if (i == len(dailycase_data) - 1 and not pass_condition):
            
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "SusceptibleRawData": int(susceptible),
                "SusceptibleModelData":int(susceptiblem),
                "InfectionRawData": int(infected),
                "InfectionModelData":int(infectedm),
                "RecoveryRawData": int(recovery),
                "RecoveryModelData":int(recoverym),
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
                "Year": str(year)
            })
            
        i = i + 1        
    
    return jsonify({
        "data": result
    })


@app.route("/vsdata/month")
@cross_origin()
def vsmonth():
    
    dailycase_data = query("SELECT date as name, confirmed as infected, newrecovered as recovery, recovered as recovery1, hospitalized as hospital, deaths as deaths, susceptible as susceptible FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, first_dose as vaccines1, second_dose as vaccines2, third_dose as vaccines3 FROM vaccinedata ORDER BY date ASC;")
    model_data = query("SELECT date as name, i as infected, r as recovery, h as hospital, d as deaths, s as susceptible, v1 as vaccines1, v2 as vaccines2, m as maintenance FROM calculatemodel ORDER BY date ASC;")
   
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
                "RecoveryRawData": int(recovery),
                "RecoveryModelData":int(recoverym),
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
            
            infected = infected + int(dailycase_data[i]["infected"])
            infectedm = infectedm + int(model_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            recoverym = recoverym + int(model_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            hospitalm = hospitalm + int(model_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            deathsm = deathsm + int(model_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines1m = vaccines1m + int(model_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            vaccines2m = vaccines2m + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            susceptiblem = susceptiblem + int(model_data[i]["susceptible"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            maintenance = recovery1 + vaccines3
            maintenancem = maintenancem + int(model_data[i]["maintenance"])
            
            if (splited_date_string[0] != year):
                month = 1
                year = splited_date_string[0]
            else:
                month = month + 1
            
        else:
            infected = infected + int(dailycase_data[i]["infected"])
            infectedm = infectedm + int(model_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            recoverym = recoverym + int(model_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            hospitalm = hospitalm + int(model_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            deathsm = deathsm + int(model_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines1m = vaccines1m + int(model_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            vaccines2m = vaccines2m + int(model_data[i]["vaccines2"])
            susceptible = susceptible + int(dailycase_data[i]["susceptible"])
            susceptiblem = susceptiblem + int(model_data[i]["susceptible"])
            recovery1 = recovery1 + int(dailycase_data[i]["recovery1"])
            vaccines3 = vaccines3 + int(vaccine_data[i]["vaccines3"])
            maintenance = recovery1 + vaccines3
            maintenancem = maintenancem + int(model_data[i]["maintenance"])
            
            
        if (i == len(dailycase_data) - 1 and not pass_condition):

            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "SusceptibleRawData": int(susceptible),
                "SusceptibleModelData":int(susceptiblem),
                "InfectionRawData": int(infected),
                "InfectionModelData":int(infectedm),
                "RecoveryRawData": int(recovery),
                "RecoveryModelData":int(recoverym),
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