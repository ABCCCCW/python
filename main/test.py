import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="python"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM hoadon")

for x in mycursor.fetchall():
  print(x)
