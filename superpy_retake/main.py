# Imports
import argparse
import csv
from csv import DictWriter
from datetime import datetime, date, timedelta
import os
from tabulate import tabulate
from rich import print


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

file_path_bought = os.path.abspath("bought.csv")
file_path_sold = os.path.abspath("sold.csv")
file_path_inventory = os.path.abspath("inventory.csv")
file_path_expired = os.path.abspath("expired.csv")
file_path_report = os.path.abspath("report.csv")
file_path_profit = os.path.abspath("profit.csv")
file_path_date = os.path.abspath("date.txt")


# Write bought product dict to bought.csv file
def bought_product(productname, buydate, price, expirationdate):
    existing_rows = []
    with open(file_path_bought, 'r') as f:
        reader = csv.reader(f)
        for header in reader:
            break
        existing_rows = list(reader)
        new_id = len(existing_rows) + 1

    with open(file_path_bought, 'a', newline='') as f:
        writer = DictWriter(f, fieldnames=header)
        writer.writerow({
            'id': new_id, 'product_name': productname,
            'buy_date': buydate, 'buy_price': price,
            'expiration_date': expirationdate
        })

    # Write bought product dict to inventory.csv file
    with open(file_path_inventory, 'r') as f:
        reader = csv.reader(f)
        for header in reader:
            break

    with open(file_path_inventory, 'a', newline='') as f:
        writer = DictWriter(f, fieldnames=header)
        writer.writerow({
            'id': new_id, 'Product Name': productname,
            'Count': 1, 'Buy Price': price,
            'Expiration Date': expirationdate
        })


# Check inventory file
# Write sold products to sold.csv based on productname
def check_inventory(productname):
    source_file = file_path_inventory
    with open(source_file, 'r') as source:
        reader = csv.reader(source)
        for row in reader:
            row_product = row[1]
            if row_product == productname:
                return True

# Read inventory file and check stock
# def check_inventory(productname):
#    bought_id = {}

#    with open(file_path_inventory, newline='') as f:
#        reader = csv.reader(f, delimiter=',')
#        bought_dict = {rows[0]: rows[1] for rows in reader}
#    bought_id = bought_dict
#    for bought_id, product in bought_id.items():
#        if product == productname:
#            return True


# Write sold product dict to sold.csv file
def sold_product(productname, selldate, price):
    product_dict = {}

    with open(file_path_bought, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        bought_dict = {rows[0]: rows[1] for rows in reader}
    product_dict = bought_dict

    existing_rows = []
    with open(file_path_sold, 'r') as f:
        reader = csv.reader(f)
        for header in reader:
            break
        existing_rows = list(reader)
        new_id_sold = len(existing_rows) + 1

    with open(file_path_sold, 'a', newline='') as f:
        writer = DictWriter(f, fieldnames=header)
        writer.writerow({
            'sold_id': new_id_sold,
            'bought_id': list(product_dict.values()).index(productname),
            'sell_date': selldate, 'sell_price': price
        })


# Remove sold items from inventory.csv file
def update_inventory():
    # Open sold file and get a unique set of ids
    sold_csv = csv.DictReader(open(file_path_sold, 'r'))
    sales = set(i.get('bought_id') for i in sold_csv)

    # Open inventory file and only retain the data not in the set
    inventory_csv = csv.DictReader(open(file_path_inventory, 'r'))
    inventory = [i for i in inventory_csv if i.get('id') not in sales]

    # Overwrite inventory file with the new results
    with open(file_path_inventory, 'w', newline='') as f:
        writer = csv.DictWriter(f, inventory[0].keys(), lineterminator='\n')
        writer.writeheader()
        writer.writerows(inventory)


# Check inventory file
# Write expired products to expired.csv based on date
def remove_expired(date):
    source_file = file_path_inventory
    destination_file = file_path_expired
    rows = []
    with open(source_file, 'r') as source:
        reader = csv.reader(source)
        header = next(reader)
        for row in reader:
            row_date = row[4]
            if row_date < date:
                rows.append(row)
            else:
                continue

    with open(destination_file, 'w', newline='') as destination:
        writer = csv.writer(destination)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


# Print reports on command line
def create_report():
    with open(
        file_path_expired, 'r'
            ) as f1, open(file_path_inventory, 'r') as f2:
        fileone = f1.readlines()
        filetwo = f2.readlines()

    with open(file_path_report, 'w', newline='') as output_file:
        for line in filetwo:
            if line not in fileone:
                output_file.write(line)

    header = ['Product Name', 'Count', 'Buy Price', 'Expiration Date']
    inventory = []
    line = []

    with open(file_path_report, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            line = [row[1], row[2], row[3], row[4]]
            inventory.append(line)
        print(tabulate(inventory, headers=header, tablefmt='fancy_grid'))


def calc_revenue(date):
    with open(file_path_sold, 'r') as f:
        dict_reader = csv.DictReader(f)
        revenue = 0
        for row in dict_reader:
            if row['sell_date'][0:10] == date:
                revenue = revenue + float(row['sell_price'])
            else:
                continue
        return round(revenue, 3)


def calc_monthly_revenue(month):
    with open(file_path_sold, 'r') as f:
        dict_reader = csv.DictReader(f)
        revenue = 0
        for row in dict_reader:
            if row['sell_date'][0:7] == month:
                revenue = revenue + float(row['sell_price'])
            else:
                continue
        return round(revenue, 3)


def create_profit_report():
    records1 = []
    line1 = []

    with open(file_path_sold, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            line1 = [row[0], row[1], row[2], row[3]]
            records1.append(line1)

    records2 = []
    line2 = []
    with open(file_path_bought, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            line2 = [row[0], row[1], row[3]]
            records2.append(line2)

    header = ['sold_id', 'bought_id', 'sell_date', 'sell_price', 'id',
              'product_name', 'buy_price']
    with open(file_path_profit, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for (sold_id, bought_id, sell_date, sell_price) in records1:
            for (id, product_name, buy_price) in records2:
                if bought_id == id:
                    writer.writerow([sold_id, bought_id, sell_date,
                                    sell_price, id, product_name,
                                    buy_price])


def calc_profit(date):
    with open(file_path_profit, 'r') as f:
        dict_reader = csv.DictReader(f)
        profit = 0
        for row in dict_reader:
            if row['sell_date'][0:10] == date:
                profit = profit + (
                    float(row['sell_price']) - float(row['buy_price'])
                    )
            else:
                continue
        return round(profit, 3)


def calc_monthly_profit(month):
    with open(file_path_profit, 'r') as f:
        dict_reader = csv.DictReader(f)
        profit = 0
        for row in dict_reader:
            if row['sell_date'][0:7] == month:
                profit = profit + (
                    float(row['sell_price']) - float(row['buy_price'])
                    )
            else:
                continue
        return round(profit, 3)


def calc_monthly_expired(month):
    with open(file_path_expired, 'r') as f:
        dict_reader = csv.DictReader(f)
        cost_expired = 0
        for row in dict_reader:
            if row['Expiration Date'][0:7] == month:
                cost_expired = cost_expired + (float(row['Buy Price']))
            else:
                continue
        return round(cost_expired, 3)


def forecast_expired(date):
    header = ['Product Name', 'Count', 'Buy Price', 'Expiration Date']
    forecast_expired = []
    line = []

    with open(file_path_inventory, newline='') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if row[4][0:10] == date:
                line = [row[1], row[2], row[3], row[4]]
                forecast_expired.append(line)
        return tabulate(
                        forecast_expired, headers=header, tablefmt='fancy_grid'
                    )


# set date
today = date.today()
string_today = today.strftime("%Y-%m-%d")

previous_date = date.today() - timedelta(days=1)
string_previous = previous_date.strftime("%Y-%m-%d")


def advance_time(number):
    advanced_date = date.today() + timedelta(days=number)
    string_advanced = advanced_date.strftime("%Y-%m-%d")
    return string_advanced


def update_datefile(date):
    date_file = ('date.txt')
    with open(date_file, 'w') as file:
        file.write(str(date))


# Retrieve system date from date.txt to use in buying & selling
file_path = file_path_date
with open(file_path, 'r') as file:
    content = file.read()
    line_with_date = content.strip().split("\n")[0]
    systemdate = line_with_date.strip()


# Set system date to yesterday to use in reporting
def advance_systemtime(date):
    date = datetime.strptime(systemdate, "%Y-%m-%d")
    yesterday = date - timedelta(days=1)
    yesterday_string = yesterday.strftime("%Y-%m-%d")
    return yesterday_string


# Write command-line tool
parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command')
buy = subparser.add_parser('buy', help='buy a product')
sell = subparser.add_parser('sell', help='sell a product')
inventory = subparser.add_parser('report-inventory',
                                 help='create an inventory report')
revenue = subparser.add_parser('report-revenue',
                               help='create a revenue report')
profit = subparser.add_parser('report-profit', help='create a profit report')
forecast = subparser.add_parser('forecast',
                                help='create forecast for products to expire')
setdate = subparser.add_parser('set-date',
                               help='set system date to given date')

buy.add_argument('--productname', type=str, required=True,
                 help='name of product bought')
buy.add_argument('--price', type=float, required=True,
                 help='price paid for product')
buy.add_argument('--expirationdate', type=str, required=True,
                 help='date when product expires, use yyyy-mm-dd format')

sell.add_argument('--productname', type=str, required=True,
                  help='name of product sold')
sell.add_argument('--price', type=float, required=True,
                  help='sell price for product')

inventory.add_argument('--today', action='store_true',
                       help='set the date to today')
inventory.add_argument('--yesterday', action='store_true',
                       help='set the date to yesterday')

revenue.add_argument('--today', action='store_true',
                     help='set the date to today')
revenue.add_argument('--yesterday', action='store_true',
                     help='set the date to yesterday')
revenue.add_argument('--date', type=str,
                     help='monthly profit report, use yyyy-mm format')

profit.add_argument('--today', action='store_true',
                    help='set the date to today')
profit.add_argument('--yesterday', action='store_true',
                    help='set the date to yesterday')
profit.add_argument('--date', type=str,
                    help='monthly profit report, use yyyy-mm format')

forecast.add_argument('--advancetime', type=int, required=True,
                      help='input number to advance time in days')

setdate.add_argument('--date', type=str,
                     help='change system date, use yyyy-mm-dd')
setdate.add_argument('--today', action='store_true',
                     help='set the date to today')

args = parser.parse_args()

if args.command == 'buy':
    try:
        datetime.strptime(args.expirationdate, '%Y-%m-%d')
    except ValueError:
        print("Incorrect date format, please use yyyy-mm-dd")
    else:
        bought_product(
            args.productname, systemdate, args.price, args.expirationdate
        )
        print('[bold green]OK[/bold green]')

if args.command == 'sell':
    if check_inventory(args.productname) is True:
        sold_product(
            args.productname, systemdate, args.price
        )
        update_inventory()
        print('[bold green]OK[/bold green]')
    else:
        print(
            'ERROR: Product not in stock or expired, please check inventory.'
        )

if args.command == 'report-inventory':
    if args.today:
        date = systemdate
        remove_expired(date)
        update_inventory()
        create_report()
    elif args.yesterday:
        date = systemdate
        new_date = advance_systemtime(date)
        print(new_date)
        remove_expired(new_date)
        update_inventory()
        create_report()
    else:
        print('ERROR: specify date with --today or --yesterday')

if args.command == 'report-revenue':
    if args.today:
        date = systemdate
        print("Today's revenue so far:", calc_revenue(date))
    elif args.yesterday:
        date = systemdate
        new_date = advance_systemtime(date)
        print(new_date)
        print("Yesterday's revenue:", calc_revenue(new_date))
    elif args.date:
        try:
            datetime.strptime(args.date, '%Y-%m')
        except ValueError:
            print('[red]Incorrect date format, please use yyyy-mm[/red]')
        else:
            month = datetime.strptime(args.date, "%Y-%m")
            string_month = f'{month.strftime("%B %Y")}:'
            print(
                'Revenue from', string_month, calc_monthly_revenue(args.date)
            )
    else:
        print('ERROR: specify date with --today, --yesterday or --date')

if args.command == 'report-profit':
    if args.today:
        date = systemdate
        create_profit_report()
        print("Today's profit so far:", calc_profit(date))
    elif args.yesterday:
        date = systemdate
        new_date = advance_systemtime(date)
        print(new_date)
        create_profit_report()
        print("Yesterday's profit:", calc_profit(new_date))
    elif args.date:
        try:
            datetime.strptime(args.date, '%Y-%m')
        except ValueError:
            print('[red]Incorrect date format, please use yyyy-mm[/red]')
        else:
            create_profit_report()
            month = datetime.strptime(args.date, "%Y-%m")
            string_month = f'{month.strftime("%B %Y")}:'
            profit = calc_monthly_profit(args.date)
            cost_expired = calc_monthly_expired(args.date)
            actual_profit = round(profit - cost_expired, 3)
            print("Profit from", string_month, profit)
            print("Actual Profit from", string_month, actual_profit)
    else:
        print('ERROR: specify date with --today, --yesterday or --date')

if args.command == 'forecast':
    date = advance_time(args.advancetime)
    print('[bold green]OK[/bold green]')
    print(forecast_expired(date))

if args.command == 'set-date':
    if args.today:
        date = string_today
        update_datefile(date)
        print(f'Date is set to (yyyy-mm-dd): {date}')
    elif args.date:
        try:
            datetime.strptime(args.date, '%Y-%m-%d')
        except ValueError:
            print('[red]Incorrect date format, please use yyyy-mm-dd[/red]')
        date = args.date
        update_datefile(date)
        print(f'Date is set to (yyyy-mm-dd): {date}')
    else:
        print('ERROR: specify date with --today or --date')


def main():
    pass


if __name__ == "__main__":
    main()
