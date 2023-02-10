import mysql.connector
from flask import Flask, jsonify, make_response, request
from datetime import datetime
import calendar


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

sql_connection = mysql.connector.connect(
    host='localhost', 
    user='Dayvid',
    password='083a609da@',
    database='credit-card-bd'   
)

my_cursor = sql_connection.cursor() # all sql commands must be inside of this guy, and before the close function

@app.route('/api/v1/credit-cards',) # req of type get by default.
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
            message= 'Here are all credit cards!',
            data= credit_cards_formated
        )
    )



@app.route('/api/v1/credit-cards',methods = ['POST'])
def create_credit_card():    #function are much big. must be refatored soon.
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
    
    date_object = datetime.strptime(exp_date, '%Y-%m-%d').date() #This is to transform our exp_date at format datetime
    year=date_object.year #This just is possible, cuz date_object is in DateTime format. 
    month = date_object.month
    
    last_day_of_the_month= calendar.monthrange(year,month )[1] #This position of array returns how much days the month has
    exp_date = date_object.replace(day=last_day_of_the_month)
    if len(holder) < 3:
        return make_response(jsonify( message="The holder must have more than 2 characters."))

    
    
    

    #After going through all validations, now it's time to send the credit card to database.
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
