import mysql.connector
db = mysql.connector.connect(
    host="sbjte.h.filess.io",
    user="hello_presentten",
    password="715e84eaadc57416103cc250def8413da5ecfa62",
    database="hello_presentten"
)

cursor = db.cursor()
