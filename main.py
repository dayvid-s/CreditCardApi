import mysql.connector
from flask import Flask, jsonify, make_response, request
from datetime import datetime
import calendar
from flask_httpauth import HTTPTokenAuth
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import onetimepad
# from creditcard import CreditCard



app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

sql_connection = mysql.connector.connect(
    host='localhost', 
    user='Dayvid',
    password='083a609da@',
    database='credit-card-bd'   
)

my_cursor = sql_connection.cursor() # all sql commands must be inside of this guy, and before the close function

admins = {
    "dayvid": generate_password_hash("hello"),
    "maistodos": generate_password_hash("12345"),
    }


token_auth = HTTPTokenAuth(scheme="Bearer")
secret_key = "somethinverycomplex" # last part of token, and more important  
#if attackers don't have this part of the token, they can't get the full token

@token_auth.verify_token
def verify_token(token):
    try:
        decoded_jwt = jwt.decode(token, secret_key, algorithms=["HS256"])
    except Exception as e:
        return None
    if decoded_jwt["name"] in admins:
        return decoded_jwt["name"]
    return None




@app.route('/api/v1/credit-cards/login', methods=["POST"]) 
def login():
    user_info = request.json
    if "username" not in user_info or "password" not in user_info:
        raise Exception("You need put your username and password")
    if not check_password_hash(admins[user_info["username"]], user_info["password"]):
        raise Exception("Invalid password")

    encoded_jwt = jwt.encode({"iss":"credit_card_api", "name": user_info["username"]}, secret_key, algorithm="HS256")
    return jsonify({"token": encoded_jwt})




@app.route('/api/v1/credit-cards') # req of type get by default.
@token_auth.login_required
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



@app.route('/api/v1/credit-cards',methods = ['POST']) # this must be refatored with blueprints
@token_auth.login_required
def create_credit_card():    #function are much big. must be refatored soon.
    my_cursor = sql_connection.cursor() 
    credit_card= request.json

    exp_date= credit_card['exp_date']
    holder= credit_card['holder']
    number= credit_card['number']
    cvv= credit_card['cvv']
    brand= credit_card['brand']

    try : datetime.strptime(exp_date, '%Y-%m') 
    except :
        return make_response(jsonify( message='invalid date, try YYYY-MM'))
    if datetime.now() > datetime.strptime(exp_date,'%Y-%m'):
        return make_response(jsonify( message="Your card expedition date cannot be less than today's date."),400)
    
    date_object = datetime.strptime(exp_date, '%Y-%m').date() #This is to transform our exp_date at format datetime
    year=date_object.year #This just is possible, cuz date_object is in DateTime format. 
    month = date_object.month
    
    last_day_of_the_month= calendar.monthrange(year,month )[1] #This position of array returns how much days the month has
    exp_date = date_object.replace(day=last_day_of_the_month)    
    
    if len(holder) < 3:
        return make_response(jsonify( message="The holder must have more than 2 characters."),400)


    if len(str(cvv)) < 3  or  len(str(cvv))> 4 :
        return make_response(
            jsonify(
                message=f"The cvv field must have between 3 and 4 numbers, you have informed:{(len(str(cvv)))}"),400)
    
    if isinstance(cvv, int) == False :
        return make_response(jsonify(message=f"The cvv field must be a number, without quotes"),400)
    
    # card_number = "4539578763621486"  # this is a Visa card

    # card_number = "4539578763621486"  # this is a Visa card
    # cc = CreditCard(card_number)
    # cc.is_valid()  # returns True
    # cc.get_brand()  # returns Visa

    number = onetimepad.encrypt(f"{number}", 'creditcardapiKey6032')
    # card_number_decripted = onetimepad.decrypt(F"{number}", 'creditcardapiKey6032')


    #After going through all validations, now it's time to send the credit card to database.
    command= f'insert into creditCards (exp_date,holder,number,cvv, brand)VALUES ("{exp_date}","{holder}","{number}",{cvv},"{brand}")'

    my_cursor.execute(command)
    sql_connection.commit()

    return make_response(
        jsonify(
            message= 'Credit card registered with successful!',
            card = credit_card
        )
    )




@app.route('/api/v1/credit-cards/<int:id>',methods = ['DELETE']) 
@token_auth.login_required
def delete_credit_card(id):    

    command= f'DELETE FROM creditCards WHERE idcreditcards ="{id}"'

    my_cursor.execute(command)
    sql_connection.commit()

    return make_response(
        jsonify(
            message= 'Credit card deleted with successful!',
        )
    )


app.run (port =5000, host='localhost', debug=True)
my_cursor.close()
sql_connection.close()
