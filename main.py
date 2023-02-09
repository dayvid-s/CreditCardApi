import mysql.connector
from flask import Flask, jsonify, make_response
from datetime import datetime

app = Flask(__name__)

sql_connection = mysql.connector.connect(
    host='localhost', 
    user='Dayvid',
    password='083a609da@',
    database='credit-card-bd'   
)
my_cursor = sql_connection.cursor()   # all sql commands must be inside of this guy, and before the close function


@app.route('/credit-cards',) # req of type get by default.
def retrieve_all_credit_cards():  #this function will take all credit cards from database, and return to api rest
    my_cursor.execute('SELECT * FROM creditCards')
    result = my_cursor.fetchall()

    return make_response(
        jsonify(
            message= 'All credit cards!',
            data= result
        )
    )

app.run (port =5000, host='localhost', debug=True)

my_cursor.close()
sql_connection.close()
