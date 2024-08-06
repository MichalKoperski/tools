from rich.console import Console
from rich.table import Table
from rich import print as rprint
import calendar
from datetime import date

var = {}
with open("costs.txt") as conf:
    for line in conf:
        if "=" in line:
            name, value = line.split(" = ")
            var[name] = int(str(value).rstrip())
globals().update(var)

moneyInput = input("How much cash: ")
if len(moneyInput) == 0:
    moneyInput = savings
moneyInput = int(moneyInput)

howManyColumns = input("How many columns: ")
if len(howManyColumns) == 0:
    howManyColumns = 6
howManyColumns = int(howManyColumns)

printVariable = input("Print prices? ")
if printVariable == "y" or printVariable == "yes":
    file = open(r"zzz.txt", "r")
    rprint(file.read())
    file.close()

monthNow = date.today().month
yearNow = date.today().year
restMonths = []
columns = []

for month in range(13):
    if month >= monthNow:
        if restMonths.__len__() < howManyColumns:
            restMonths.append(month)

calList = []
restVacations = []
i = 0
for cal in restMonths:
    calList.append(calendar.TextCalendar(calendar.MONDAY).formatmonth(yearNow, restMonths[i]))
    i += 1

i = 0
while calList.__len__() < howManyColumns:
    calList.append(calendar.TextCalendar(calendar.MONDAY).formatmonth(yearNow + 1, i + 1))
    i += 1

i = 0
if restMonths.__len__() == howManyColumns:
    restMonths.pop(0)
columns.append("       " + str("{:,}".format(moneyInput)))
for money in restMonths:
    if restMonths[i] == 4 or restMonths[i] == 9:
        moneyInput = int(moneyInput + int(1.8*salary) - rent - D13 - D14 - D26 - upc - orange - youtube - iCloud)
        convMoney = "       " + str("{:,}".format(moneyInput))
        columns.append(convMoney)
        i += 1
    elif restMonths[i] % 2 != 0:
        moneyInput = int(moneyInput + salary - rent - electricity - D13 - D14 - D26 - upc - orange - youtube - iCloud)
        convMoney = "       " + str("{:,}".format(moneyInput))
        columns.append(convMoney)
        i += 1
    else:
        moneyInput = int(moneyInput + salary - rent - D13 - D14 - D26 - upc - orange - youtube - iCloud)
        convMoney = "       " + str("{:,}".format(moneyInput))
        columns.append(convMoney)
        i += 1

while columns.__len__() < howManyColumns:
    i = 1
    if i == 4:
        moneyInput = int(moneyInput + int(
            1.8 * salary) - rent - D13 - D14 - D26 - upc - orange - youtube - iCloud)
        convMoney = "       " + str("{:,}".format(moneyInput))
        columns.append(convMoney)
        i += 1
    elif i % 2 != 0:
        moneyInput = int(
            moneyInput + salary - rent - electricity - D13 - D14 - D26 - upc - orange - youtube - iCloud)
        convMoney = "       " + str("{:,}".format(moneyInput))
        columns.append(convMoney)
        i += 1
    else:
        moneyInput = int(
            moneyInput + salary - rent - D13 - D14 - D26 - upc - orange - youtube - iCloud)
        convMoney = "       " + str("{:,}".format(moneyInput))
        columns.append(convMoney)
        i += 1

table = Table(title='--- SAVE MONEY ---', style='yellow', title_style='bold red')

rows = [
    calList,
]

for column in columns:
    table.add_column(column, style='green')

for row in rows:
    table.add_row(*row, style='green')

Console().print(table)