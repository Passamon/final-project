import psycopg2
from psycopg2 import Error

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():

    try:
        # Connect to an existing database
        connection = psycopg2.connect(user="mwtnjzht",
                                    password="fVSeF78PdfVJX-NQ9RDjAYdsHejAe11n",
                                    host="john.db.elephantsql.com",
                                    port="5432",
                                    database="mwtnjzht")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Executing a SQL query
        cursor.execute("SELECT * FROM test;")
        # Fetch result
        record = cursor.fetchone()
        return jsonify({
            "output": record
        })

    except (Exception, Error) as error:
        return jsonify({
            "error": 123
        })
    finally:
        if (connection):
            cursor.close()
            connection.close()
    
    