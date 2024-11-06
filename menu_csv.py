import datetime
import pandas as pd
import plotext as plt
import calendar

#====================================================BUDGET==============================================
def run_budget():
    months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}

    savings = 0
    cash_inflow = 0
    cash_outflow = 0

    var = {}
    with open("/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/costs.txt") as conf:
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

def menu_display():
    print()
    print("=" * 54)
    print("|| 1.run database  2.run budget  3.calendar  4.exit ||")
    print("=" * 54)
    print()
    choice = int(input("What do you want to do?: "))
    return choice

def menu_display_db():
    print()
    print("==================PERSON================\n"
          "||  1.select    2.insert    3.delete  ||\n"
          "==================ALL===================\n"
          "||      4.people        5.exit        ||\n"
          "========================================\n")
    choice = int(input("What do you want to do?: "))
    return choice


loop_menu = True
while loop_menu:
    loop_db = True
    choice = menu_display()
    if choice == 1:
        df = pd.read_csv('/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/db.csv', index_col='id')
        while loop_db:
            choice = menu_display_db()
            if choice == 1:
                person = input("Person: ")
                filt = (df['surname'] == person)
                if (len(df[filt]) != 0):
                    filt2 = df.loc[filt, 'surname'].drop_duplicates().index
                    print(df.loc[filt2, ['name', 'surname', 'start', 'position']])
                    print(df.loc[filt, ['date', 'description']])
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
                df.loc[id, ['id', 'start', 'name', 'surname', 'position', 'date', 'description']] = [id, start, name, surname, position, date, description]
            elif choice == 3:
                person = input("Surname: ")
                filt = (df['surname'] == person)
                df.drop(index=df[filt].index, inplace=True)
            elif choice == 4:
                filt = (df['surname'].drop_duplicates().index)
                print(df.loc[filt, ['name', 'surname', 'start', 'position']])
                print()
            else:
                df.drop(df.iloc[:, 6:].columns, axis=1, inplace=True)
                df.to_csv('/Users/michalkoperski/Library/Mobile Documents/com~apple~CloudDocs/db.csv')
                loop_db = False
                break
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
    else:
        loop_menu = False