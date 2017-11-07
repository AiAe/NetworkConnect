import sqlite3
import datetime

def connect():
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    return connection, cursor

def execute(connection, cursor, quary, args):
    cursor.execute(quary, args)
    connection.commit()
    connection.close()

def quarry(connection, cursor, query, args={}, one=False):
    cursor.execute(query, args)
    cursor.row_factory = sqlite3.Row
    rv = cursor.fetchall()
    connection.close()
    return (rv if rv else None) if one else rv

def find_date(date):
    connection, cursor = connect()
    find = quarry(connection, cursor, "SELECT date FROM graph WHERE date = ?", [date], one=True)

    if find != None and len(find) > 0:
        return True
    else:
        return False

def read(date):
    connection, cursor = connect()
    value = 0
    for q in quarry(connection, cursor, "SELECT * FROM graph WHERE date = ?", [date]):
        value = q[2]
    if value == 0:
        return 0
    else:
        return value

def write():
    connection, cursor = connect()
    date = datetime.datetime.now().strftime("%Y%m%d")
    temp = int(read(date))
    if find_date(date):
        value = temp + 1
        execute(connection, cursor, "UPDATE graph SET value = ? WHERE date = ?", [value, date])
    else:
        execute(connection, cursor, "INSERT INTO graph (date, value) VALUES (?, ?)", [date, 1])

def output():
    connection, cursor = connect()
    dates = []
    values = []

    for value in quarry(connection, cursor, "SELECT * FROM graph WHERE NOT id = ?", ["0"]):

        dates.append(value[1][6:8] + "/" + value[1][4:6] + "/" + value[1][:4])
        values.append(value[2])

    return dates, values
