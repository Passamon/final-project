import psycopg2
from psycopg2 import Error
import psycopg2.extras
from flask import request

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

import datetime

import random

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

@app.route("/coviddata" , methods=['POST'])
@cross_origin()
def data():
    
    start = request.get_json()["start_date"]     
    end = request.get_json()["end_date"]
    
    dailycase_data = query("SELECT date as name, newconfirmed as infected, newrecovered as recovery, newhospitalized as hospital, newdeaths as deaths FROM dailycase WHERE date BETWEEN \'" + start + "\' and \'" + end + "\' ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, vaccines1, vaccines2, vaccines3 FROM vaccinedata WHERE date BETWEEN \'" + start + "\' and \'" + end + "\' ORDER BY date ASC;")
    

    s = 66186727
    sus = 0
    i = 0
    result = []
    
    while i < len(dailycase_data):
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
        
        sus = s - (vaccine_data[i]["vaccines1"] + dailycase_data[i]["infected"] + dailycase_data[i]["recovery"] + dailycase_data[i]["hospital"] + dailycase_data[i]["deaths"])
        s = sus
        
        result.append({
            "name": str(dailycase_data[i]["name"]),
            "Susceptible": str(sus),
            "Infected": dailycase_data[i]["infected"],
            "Recovery": dailycase_data[i]["recovery"],
            "Hospital": dailycase_data[i]["hospital"],
            "Deaths": dailycase_data[i]["deaths"],
            "Vaccine1": vaccine_data[i]["vaccines1"],
            "Vaccine2": vaccine_data[i]["vaccines2"],
            # "Vaccine3": vaccine_data[i]["vaccines3"],
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
    
    dailycase_data = query("SELECT date as name, newconfirmed as infected, newrecovered as recovery, newhospitalized as hospital, newdeaths as deaths FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, vaccines1, vaccines2, vaccines3 FROM vaccinedata ORDER BY date ASC;")
    
    s = 66186727
    sus = 0
    i = 0
    result = []
    
    while i < len(dailycase_data):
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
            
        # sus = 66186727 - (vaccine_data[i]["vaccines1"] + dailycase_data[i]["infected"] + dailycase_data[i]["recovery"] + dailycase_data[i]["hospital"] + dailycase_data[i]["deaths"])
        sus = s - (vaccine_data[i]["vaccines1"] + dailycase_data[i]["infected"] + dailycase_data[i]["recovery"] + dailycase_data[i]["hospital"] + dailycase_data[i]["deaths"])
        s = sus
        
        result.append({
            "name": str(dailycase_data[i]["name"]),
            "Susceptible": str(sus),
            "Infected": dailycase_data[i]["infected"],
            "Recovery": dailycase_data[i]["recovery"],
            "Hospital": dailycase_data[i]["hospital"],
            "Deaths": dailycase_data[i]["deaths"],
            "Vaccine1": vaccine_data[i]["vaccines1"],
            "Vaccine2": vaccine_data[i]["vaccines2"],
            # "Vaccines3": vaccine_data[i]["vaccines3"],
            "test": str(dailycase_data[i]["name"])
        })
            
        i = i + 1  
    
    return jsonify({
        "data": result
    })
    
@app.route("/coviddata/week")
@cross_origin()
def week():
    
    dailycase_data = query("SELECT date as name, newconfirmed as infected, newrecovered as recovery, newhospitalized as hospital, newdeaths as deaths FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, vaccines1, vaccines2, vaccines3 FROM vaccinedata ORDER BY date ASC;")
    
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
    s = 66186727
    sus = 0
    
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
            
        #     vaccine_1 = 0
        #     vaccine_2 = 0
            
        #     if (str(year) == "2021"):
        #         vaccine_1 = random.randint(10000, 50000)
        #         vaccine_2 = random.randint(10000, 50000)
                
            sus = s - (vaccines1 + infected + recovery + hospital + deaths)
            s = sus
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": str(sus),
                "Infected": infected,
                "Recovery": recovery,
                "Hospital": hospital,
                "Deaths": deaths,
                "Vaccine1": vaccines1,
                "Vaccine2": vaccines2,
                "Year": str(year),
                "test": str(dailycase_data[i]["name"])
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            s = 66186727
            sus = 0
            
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
            
            day = day + 1
            
        else:
            
            pass_condition = True
            
            infected = infected + int(dailycase_data[i]["infected"])
            recovery = recovery + int(dailycase_data[i]["recovery"])
            hospital = hospital + int(dailycase_data[i]["hospital"])
            deaths = deaths + int(dailycase_data[i]["deaths"])
            vaccines1 = vaccines1 + int(vaccine_data[i]["vaccines1"])
            vaccines2 = vaccines2 + int(vaccine_data[i]["vaccines2"])
            
            # vaccine_1 = 0
            # vaccine_2 = 0
            
            # if (str(year) == "2021"):
            #     vaccine_1 = random.randint(10000, 50000)
            #     vaccine_2 = random.randint(10000, 50000)
                
            sus = s - (vaccines1 + infected + recovery + hospital + deaths)
            s = sus
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": str(sus),
                "Infected": infected,
                "Recovery": recovery,
                "Hospital": hospital,
                "Deaths": deaths,
                "Vaccine1": vaccines1,
                "Vaccine2": vaccines2,
                "Year": str(year),
                "test": str(dailycase_data[i]["name"])
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            
            week = week + 1
            day = day + 1
            
        if (i == len(dailycase_data) - 1 and not pass_condition):
            
            # vaccine_1 = 0
            # vaccine_2 = 0
            
            # if (str(year) == "2021"):
            #     vaccine_1 = random.randint(10000, 50000)
            #     vaccine_2 = random.randint(10000, 50000)
                
            sus = s - (vaccines1 + infected + recovery + hospital + deaths)
            s = sus
            
            result.append({
                "name": str(week) + "-" + monthToMonthName(month),
                "Susceptible": str(sus),
                "Infected": infected,
                "Recovery": recovery,
                "Hospital": hospital,
                "Deaths": deaths,
                "Vaccine1": vaccines1,
                "Vaccine2": vaccines2,
                "Year": str(year),
                "test": str(dailycase_data[i]["name"])
            })
            
        i = i + 1        
    
    return jsonify({
        "data": result
    })
    
@app.route("/coviddata/month")
@cross_origin()
def month():
    
    dailycase_data = query("SELECT date as name, newconfirmed as infected, newrecovered as recovery, newhospitalized as hospital, newdeaths as deaths FROM dailycase ORDER BY date ASC;")
    vaccine_data = query("SELECT date as name, vaccines1, vaccines2, vaccines3 FROM vaccinedata ORDER BY date ASC;")
    
    i = 0
    month = 1
    
    year = -1
    
    infected = 0
    recovery = 0
    hospital = 0
    deaths = 0
    vaccines1 = 0
    vaccines2 = 0
    s = 66186727
    sus = 0
    
    result = []
    
    while i < len(dailycase_data):
        
        pass_condition = False
        
        date_string = str(dailycase_data[i]["name"])
        splited_date_string = date_string.split(sep = "-")
        
        if (i == 0):
            year = splited_date_string[0]
        
        if (int(splited_date_string[1]) != month):
            
            pass_condition = True
            
            # vaccine_1 = 0
            # vaccine_2 = 0
            
            # if (str(year) == "2021"):
            #     vaccine_1 = random.randint(10000, 50000)
            #     vaccine_2 = random.randint(10000, 50000)
                
            sus = s - (vaccines1 + infected + recovery + hospital + deaths)
            s = sus
            
            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "Susceptible": str(sus),
                "Infected": infected,
                "Recovery": recovery,
                "Hospital": hospital,
                "Deaths": deaths,
                "Vaccine1": vaccines1,
                "Vaccine2": vaccines2,
                "test": str(dailycase_data[i]["name"])
            })
            
            infected = 0
            recovery = 0
            hospital = 0
            deaths = 0
            vaccines1 = 0
            vaccines2 = 0
            
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
            
            
        if (i == len(dailycase_data) - 1 and not pass_condition):
            # vaccine_1 = 0
            # vaccine_2 = 0
            
            # if (str(year) == "2021"):
            #     vaccine_1 = random.randint(10000, 50000)
            #     vaccine_2 = random.randint(10000, 50000)
                
            sus = s - (vaccines1 + infected + recovery + hospital + deaths)
            s = sus
            
            result.append({
                "name": monthToMonthName(month) + "-" + str(year),
                "Susceptible": str(sus),
                "Infected": infected,
                "Recovery": recovery,
                "Hospital": hospital,
                "Deaths": deaths,
                "Vaccine1": vaccines1,
                "Vaccine2": vaccines2,
                "test": str(dailycase_data[i]["name"])
            })
    
        i = i + 1
    
    return jsonify({
        "data": result
    })
    
    
    
# @app.route("/request_input_example")
# @cross_origin()
# def request_input_example():

#     query("INSERT INTO abc VALUES(\"" + str(request.get_json()["hello"]) + "\")")
    
#     return jsonify({
#         "user_request": request.get_json()["hello"]
#     })

