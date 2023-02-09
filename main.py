import mysql.connector
from flask import Flask, jsonify, make_response
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

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
    credit_cards = my_cursor.fetchall()
    credit_cards_formated = list()

    for card in credit_cards:
        credit_cards_formated.append({
            'id_credit_card':card[0],
            'exp_date': card[1],
            'holder':card[2],
            'number':card[3],
            'cvv': card[4],
            'brand':card[5]
        })

    return make_response(
        jsonify(
            message= 'All credit cards!',
            data= credit_cards_formated
        )
    )




app.run (port =5000, host='localhost', debug=True)

my_cursor.close()
sql_connection.close()
