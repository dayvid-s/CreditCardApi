# first I gonna create a connection with sql, and later, i will work with api restfull.
import mysql.connector


sqlConnection = mysql.connector.connect(
    host='localhost', 
    user='Dayvid',
    password='083a609da@',
    database='credit-card-bd'
)

sqlCursor = sqlConnection.cursor()

sqlCursor.close()
sqlConnection.close()