import psycopg2
from psycopg2 import Error
import psycopg2.extras
from flask import request

from flask import Flask, jsonify

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

@app.route("/coviddata")
def coviddata():
    vaccine_data = query("SELECT * FROM vaccinedata;")
    dailycase_data = query("SELECT * FROM dailycase;")
    return jsonify({
       "vaccine_data": vaccine_data,
       "dailycase_data": dailycase_data
    })
    
# @app.route("/request_input_example")
# def request_input_example():

#     query("INSERT INTO abc VALUES(\"" + str(request.get_json()["hello"]) + "\")")
    
#     return jsonify({
#         "user_request": request.get_json()["hello"]
#     })