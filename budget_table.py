import datetime

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
