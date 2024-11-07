import datetime
import pandas as pd
import plotext as plt
import calendar
import requests
import mysql.connector
from mysql.connector import Error
from getpass import getpass
from tabulate import tabulate


#====================================================CLOCK==============================================


def show_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%-H:%M")
    date = datetime.datetime.today().strftime("%Y-%m-%d")
    print()
    print(f"Clock: {current_time}   {date}")


#====================================================CURRENCY==============================================


def currency_converter():
    api_key = 0
    with open("/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/!!data/open_currency.txt") as conf:
        for line in conf:
            api_key = line

    url = f"https://openexchangerates.org/api/latest.json?app_id={api_key}"

    response = requests.get(url)
    data = response.json()

    exchange_rates = data["rates"]

    available_currencies = ""
    for currency in exchange_rates.keys():
        available_currencies += currency + ", "

    available_currencies = available_currencies[:-2]

    print("Available currencies: " + available_currencies)

    from_currency = input("Enter the base currency: ").upper()
    to_currency = input("Enter the target currency: ").upper()

    amount = float(input("Enter the amount to convert: "))

    original_amount = amount / exchange_rates[from_currency]
    converted_amount = original_amount * exchange_rates[to_currency]

    print(f"{amount} {from_currency} = {converted_amount} {to_currency}")


#====================================================BUDGET==============================================


def run_budget():
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}

    savings = 0
    cash_inflow = 0
    cash_outflow = 0

    var = {}
    with open("/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/!!data/costs.txt") as conf:
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

# ====================================================GRAPH=============================================
    a = {}
    for key, value in month_costs.items():
        s = (int(value / 1000))
        a.update({key:s})
    plt.simple_bar(a.keys(), a.values(), width=100, title='Savings in TPLN', color='green')
    print()
    print()
    plt.show()


# ====================================================CSV==============================================
def csv_db():
    df = pd.read_csv('/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/!!data/db.csv', index_col='id')
    while True:
        choice = menu_display_csv()
        if choice == 1:
            person = input("Person: ")
            filt = (df['surname'] == person)
            if (len(df[filt]) != 0):
                filt2 = df.loc[filt, 'surname'].drop_duplicates().index
                print(tabulate(df.loc[filt2, ['name', 'surname', 'start', 'position']], headers=['id', 'name', 'surname', 'start', 'position'], tablefmt='psql'))
                print(tabulate(df.loc[filt, ['date', 'description']], headers=['date', 'description'], tablefmt='psql'))
            else:
                print("No such person")
        elif choice == 2:
            name = input("Name: ")
            surname = input("Surname: ")
            start = input("Date: ")
            position = input("Position: ")
            date = input("Date: ")
            description = input("Description: ")
            id = len(df) + 1
            df.loc[id, ['id', 'start', 'name', 'surname', 'position', 'date', 'description']] = [id, start, name,
                                                                                                 surname, position,
                                                                                                 date, description]
        elif choice == 3:
            person = input("Surname: ")
            filt = (df['surname'] == person)
            df.drop(index=df[filt].index, inplace=True)
        elif choice == 4:
            filt = (df['surname'].drop_duplicates().index)
            print(tabulate(df.loc[filt, ['name', 'surname', 'start', 'position']], headers=['id', 'name', 'surname', 'start', 'position'], tablefmt='psql'))
            print()
        else:
            df.drop(df.iloc[:, 6:].columns, axis=1, inplace=True)
            df.to_csv('/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/!!data/db.csv')
            break


#==============================================SQL================================================
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


def execute_query(connection, query, val):
    cursor = connection.cursor()
    try:
        cursor.execute(query, val)
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


def sql_db():
    connection = create_db_connection('localhost', 'root', getpass(), 'person_database')
    while True:
        choice = menu_display_sql()
        if choice == 1:
            person = input("Person: ")
            query = "select id_person from person where surname = '%s'" % person
            if len(read_query(connection, query)) != 0:
                id = int(read_query(connection, query)[0][0])
                query = "select * from person where surname = '%s'" % person
                print(tabulate(read_query(connection, query), headers=['id', 'date', 'name', 'surname', 'position'],
                               tablefmt='psql'))
                query = ("select events.date, events.description from person, events where "
                         "events.id_person=person.id_person and person.id_person = %s order by events.date") % id
                print(tabulate(read_query(connection, query), headers=['date', 'description'], tablefmt='psql'))
                print()
            else:
                print("No such person in database")
        elif choice == 2:
            name = input("Name: ")
            surname = input("Surname: ")
            start = input("Date: ")
            position = input("Position: ")
            query = "insert into person(start, name, surname, position) values (%s, %s, %s, %s);"
            val = (start, name, surname, position)
            execute_query(connection, query, val)
        elif choice == 3:
            person = input("Surname: ")
            query = "delete from person where surname = '%s'" % person
            val = ()
            execute_query(connection, query, val)
        elif choice == 4:
            person = input("Surname: ")
            date = input("Date: ")
            description = input("Description: ")
            query = "select id_person from person where surname = '%s'" % person
            id = int(read_query(connection, query)[0][0])
            query = "insert into events(id_person, date, description) values (%s, %s, %s);"
            val = (id, date, description)
            execute_query(connection, query, val)
        elif choice == 5:
            person = input("Surname: ")
            query = "select id_person from person where surname = '%s'" % person
            id = int(read_query(connection, query)[0][0])
            query = "delete from events where id_person = '%s'" % id
            val = ()
            execute_query(connection, query, val)
        elif choice == 6:
            query = "select * from person"
            print(tabulate(read_query(connection, query), headers=['id', 'date', 'name', 'surname', 'position'],
                           tablefmt='psql'))
            print()
        elif choice == 7:
            query = ("select person.name, person.surname, events.date, events.description from "
                     "events, person where events.id_person=person.id_person order by events.date")
            print(tabulate(read_query(connection, query), headers=['name', 'surname', 'date', 'description'],
                           tablefmt='psql'))
            print()
        else:
            break


def menu_display():
    show_time()
    print()
    print("=" * 76)
    print("|| 1.run database  2.run budget  3.calendar  4.currency converter  5.exit ||")
    print("=" * 76)
    print()
    choice = int(input("What do you want to do?: "))
    return choice


def menu_display_csv():
    show_time()
    print()
    print("==================PERSON================\n"
          "||  1.select    2.insert    3.delete  ||\n"
          "==================ALL===================\n"
          "||      4.people        5.exit        ||\n"
          "========================================\n")
    choice = int(input("What do you want to do?: "))
    return choice


def menu_display_sql():
    print()
    print("==================PERSON================\n"
          "||  1.select    2.insert    3.delete  ||\n"
          "================DESCRIPTION=============\n"
          "||     4.insert           5.delete    ||\n"
          "==================ALL===================\n"
          "||  6.people     7.events    8.exit   ||\n"
          "========================================\n")
    choice = int(input("What do you want to do?: "))
    return choice


def terminal():
    loop_menu = True
    while loop_menu:
        choice = menu_display()
        if choice == 1:
            choice = input("sql [s] or csv [c]: ")
            if choice == 's':
                sql_db()
            else:
                csv_db()
        elif choice == 2:
            print()
            run_budget()
            print()
        elif choice == 3:
            choice = input("month [m] or year [y]: ")
            print()
            if choice == 'm':
                print(calendar.month(datetime.date.today().year, datetime.date.today().month))
            else:
                print(calendar.calendar(datetime.date.today().year))
        elif choice == 4:
            print()
            currency_converter()
            print()
        else:
            loop_menu = False


terminal()