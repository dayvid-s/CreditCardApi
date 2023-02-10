import mysql.connector
from flask import Flask, jsonify, make_response, request
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

sql_connection = mysql.connector.connect(
    host='localhost', 
    user='Dayvid',
    password='083a609da@',
    database='credit-card-bd'   
)

my_cursor = sql_connection.cursor() # all sql commands must be inside of this guy, and before the close function

@app.route('/credit-cards',) # req of type get by default.
def retrieve_all_credit_cards():  #this function will take all credit cards from database, and return to api rest
    my_cursor = sql_connection.cursor() 
    my_cursor.execute('SELECT * FROM creditCards')
    credit_cards = my_cursor.fetchall()
    credit_cards_formated = list()

    for card in credit_cards:
        credit_cards_formated.append({
            'idcreditcards': card[0],
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



@app.route('/credit-cards',methods = ['POST'])
def create_credit_card():  
    my_cursor = sql_connection.cursor() 
    credit_card= request.json

    exp_date= credit_card['exp_date']
    holder= credit_card['holder']
    number= credit_card['number']
    cvv= credit_card['cvv']
    brand= credit_card['brand']

    try : datetime.strptime(exp_date, '%Y-%m-%d') 
    except :
        return make_response(jsonify( message='invalid date, try YYYY-MM-DD'))
    if datetime.now() > datetime.strptime(exp_date,'%Y-%m-%d'):
        return make_response(jsonify( message="Your card expedition date cannot be less than today's date."))


    command= f'insert into creditCards (exp_date, holder, number, cvv, brand)VALUES ("{exp_date}", "{holder}",{number}, {cvv}, "{brand}")'
    
    my_cursor.execute(command)
    sql_connection.commit()

    return make_response(
        jsonify(
            message= 'Credit card registered with successful!',
            card = credit_card
        )
    )


app.run (port =5000, host='localhost', debug=True)
my_cursor.close()
sql_connection.close()
