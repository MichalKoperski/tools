import datetime
import mysql.connector
from mysql.connector import Error
import pandas as pd
from getpass import getpass

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def run_budget():
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}

    savings = 0
    cash_inflow = 0
    cash_outflow = 0

    var = {}
    with open("costs.txt") as conf:
        for line in conf:
            if "=" in line:
                name, value = line.split(" = ")
                if name == "salary":
                    cash_inflow = int(value)
                elif name == "savings":
                    savings = int(value)
                else:
                    var[name] = int(str(value).rstrip())
    globals().update(var)

    for key, value in var.items():
        cash_outflow += int(value)

    cash_flow = cash_inflow - cash_outflow
    month_costs = {}
    max_length = 0

    for i in range(datetime.date.today().month, 13):
        for key, value in months.items():
            if i == key:
                if i == datetime.date.today().month:
                    cash_flow += savings
                    month_costs.update({value: cash_flow})
                    cash_flow = cash_flow + cash_inflow - cash_outflow
                else:
                    month_costs.update({value: cash_flow})
                    cash_flow = cash_flow + cash_inflow - cash_outflow

    if datetime.date.today().month > 1:
        for i in range(1, datetime.date.today().month):
            for key, value in months.items():
                if i == key:
                    month_costs.update({value: cash_flow})
                    cash_flow = cash_flow + cash_inflow - cash_outflow

    for key, value in month_costs.items():
        if int(str(value).__len__()) > max_length:
            max_length = str(value).__len__()

    for key, value in month_costs.items():
        x = 5 + max_length - str(key).__len__()
        print(" " * x + str(key), end=" |")

    print()
    print("-" * (7 + max_length) * month_costs.__len__())

    for key, value in month_costs.items():
        y = 4 + max_length - str(value).__len__()
        print(" " * y + str("{:,}".format(value)), end=" |")

while True:
    print("="*100)
    print("1.run database\n2.run budget")
    choice = int(input("What do you want to do?: "))
    if choice == 1:
        user_password = getpass()
        connection = create_db_connection('localhost','root',user_password,'person_database')
        print("1.select a person\n2.insert a person\n3.insert a description\n4.show all people")
        choice = int(input("What do you want to do?: "))
        if choice == 1:
            person = input("Person: ")
            query = "select * from person where surname = '%s'" %person
            print(read_query(connection, query))

        elif choice == 4:
            query = "select name, surname from person"
            print(read_query(connection, query))

    elif choice == 2:
        run_budget()
        break