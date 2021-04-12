# Imports
import argparse                         # Parses CLI into function arguments
import csv                              # Handles csv reading and writing
import classes                          # Handles classes
import date_functions                   # Handles date functions
import file_functions                   # Handles reading and writing files
from rich.console import Console        # Enables pretty console printing
from rich.table import Table            # Enables easy and pretty table layout
import requests                         # Enables HTTP GET


# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# Your code below this line.

console = Console(style='cyan')


def main():
    # This should execute before every CLI command, checks directory and certain files.
    file_functions.checkdir()

    # Setting up argparse and cli-argument validation
    args = cli_arguments()
    if args.command == "report":
        if args.reporttype == 'inventory':
            if args.date == 'today' or args.date == 'yesterday':
                richprint_inventory(args.date)
            elif len(args.date) == 10 and args.date[:3].isnumeric() and args.date[4] == '-' and args.date[5:6].isnumeric() and args.date[7] == '-' and args.date[8:9].isnumeric():
                date_functions.convert_str_to_date(args.date)
                richprint_inventory(args.date)
            else:
                console.print(
                    "[red]ERROR: inventory report can only accept 'today', 'yesterday', or YYYY-MM-DD as input")
        if args.reporttype == 'profit':
            if args.date != 'today' and args.date != 'yesterday':
                # YYYY-MM = 7 chars
                if len(args.date) == 7 and args.date[:3].isnumeric() and args.date[4] == '-' and args.date[5:6].isnumeric():
                    report_profit(args.date)
                # YYYY-MM-DD = 10 chars
                elif len(args.date) == 10 and args.date[:3].isnumeric() and args.date[4] == '-' and args.date[5:6].isnumeric() and args.date[7] == '-' and args.date[8:9].isnumeric():
                    report_profit(args.date)
                else:
                    console.print(
                        "[bold red]ERROR: date has to be 'today', 'yesterday', YYYY-MM or YYYY-MM-DD [/bold red]")
            else:
                report_profit(args.date)
        if args.reporttype == 'revenue':
            if args.date != 'today' and args.date != 'yesterday':
                # YYYY-MM = 7 chars
                if len(args.date) == 7 and args.date[:3].isnumeric() and args.date[4] == '-' and args.date[5:6].isnumeric():
                    report_revenue(args.date)
                # YYYY-MM-DD = 10 chars
                elif len(args.date) == 10 and args.date[:3].isnumeric() and args.date[4] == '-' and args.date[5:6].isnumeric() and args.date[7] == '-' and args.date[8:9].isnumeric():
                    report_revenue(args.date)
                else:
                    console.print(
                        "[bold red]ERROR: date has to be 'today', 'yesterday', YYYY-MM or YYYY-MM-DD [/bold red]")
            else:
                report_revenue(args.date)
    elif args.command == "export":
        if args.date == 'today' or args.date == 'yesterday':
            export(args.date)
        elif len(args.date) == 10 and args.date[:3].isnumeric() and args.date[4] == '-' and args.date[5:6].isnumeric() and args.date[7] == '-' and args.date[8:9].isnumeric():
            date_functions.convert_str_to_date(args.date)
            export(args.date)
        else:
            console.print(
                "[bold red]ERROR: export can only accept 'today', 'yesterday', or YYYY-MM-DD as input[/bold red]")
    elif args.command == 'buy':
        if len(args.expiry) == 10 and args.expiry[:3].isnumeric() and args.expiry[4] == '-' and args.expiry[5:6].isnumeric() and args.expiry[7] == '-' and args.expiry[8:9].isnumeric():
            try:
                date_functions.convert_str_to_date(args.expiry)
            except:
                pass
            else:
                record_buy(args.product, args.price, args.expiry)
        else:
            console.print(
                f'[bold red]ERROR: {args.expiry} is not a valid date, enter in YYYY-MM-DD format.[/bold red]')
    elif args.command == 'sell':
        if args.ding == 'off' or args.ding == 'on':
            record_sell(args.product, args.price, args.ding)
        else:
            console.print(
                f"[bold red]ERROR: {args.ding} is not a valid value for --ding, only 'on' or 'off' are valid[/bold red]")
    elif args.command == 'advance-time':
        if args.days == 'reset':
            date_functions.write_date('today')
            console.print('Date successfully reset.')
            console.print('Current date is: ')
            console.print(date_functions.read_date())
        elif args.days == 'show':
            console.print('Current date is: ')
            console.print(date_functions.read_date())
        else:
            try:
                days = int(args.days)
                if days > 0:
                    date_functions.advance_date(days)
                else:
                    raise ValueError
            except ValueError:
                console.print(
                    '[bold red]ERROR: invalid input, has to be positive integer, "reset" or "show"[/bold red]')
    elif args.command is None:
        console.print('[bold red]\t ERROR: no command given, \
            type "python main.py -h" to see help.[/bold red]')


def cli_arguments():
    # https://docs.python.org/3/howto/argparse.html#id1

    parser = argparse.ArgumentParser(description='SUPERPY: Shop inventory \
                                                  software')
    subparser = parser.add_subparsers(dest='command')

    # Buy parser
    buy_parser = subparser.add_parser('buy',
                                      help='Add bought product to inventory')
    buy_parser.add_argument('-prod', '--product', type=str.lower,
                            help="name of product, example: --product apple or --product 'apple pie'", required=True)
    buy_parser.add_argument('-$', '--price', type=float,
                            help='cost price of item using a period (.), example: --price 0.60',
                            required=True)
    buy_parser.add_argument('-exp', '--expiry', type=str,
                            help='expiry date in YYYY-MM-DD format, for \
                                example: --expiry 2021-08-31', required=True)

    # Sell parser
    sell_parser = subparser.add_parser('sell',
                                       help='sell product from inventory')
    sell_parser.add_argument('-prod', '--product', type=str.lower,
                             help="name of product, example: --product apple or --product 'apple pie'",
                             required=True)
    sell_parser.add_argument('-$', '--price', type=float,
                             help='cost price of item using a period (.), example: --price 0.60',
                             required=True)
    sell_parser.add_argument('--ding', default='off', type=str.lower, help="this value is not required. if set to 'on', superpy will interact with your Homey controller. the default value is 'off'"
                             )

    # Advance-time parser
    date_parser = subparser.add_parser('advance-time',
                                       help='advance date by x days, show \
                                            current date or reset to current \
                                            date')
    date_parser.add_argument('days', help='(1) type number of days to advance, \
                             for example "python main.py advance-time 2". (2) \
                             You can show current date using "python main.py \
                             advance-time show". (3) You can reset to today\'s\
                             date using "python main.py advance-time reset".')

    # Report parser
    report_parser = subparser.add_parser(
        'report', help='inventory, profit or revenue report')
    report_parser.add_argument('reporttype', help='get \
                                inventory, profit or revenue report,\
                                example: report inventory today', choices=['inventory', 'revenue', 'profit'])
    report_parser.add_argument('--date', help="date, in YYYY-MM-DD format, or using the word 'today' or 'yesterday'. \
                               for profit and revenue you can also use YYYY-MM\
                               to get report on whole month.", default='today')

    # Export parser
    print_parser = subparser.add_parser(
        'export', help='export inventory to csv.file')
    print_parser.add_argument('--date', help="date, in YYYY-MM-DD format, or using the word 'today' or 'yesterday'. \
                               for profit and revenue you can also use YYYY-MM\
                               to get report on whole month.", default='today')

    args = parser.parse_args()
    return args


def record_buy(product_name, buy_price, expiration_date):
    # Check for highest ID number, assumption: last line is highest
    id_reader = list(csv.reader(open('bought.csv', 'r')))
    try:
        # prints last line, first item of list
        highest_id = int(id_reader[-1][0])
    except ValueError:  # Empty bought.csv throws error
        highest_id = 0

    # Now assemble buy_item class instance so you can write it to .csv
    id_num = highest_id + 1
    buy_date = date_functions.read_date()
    bought_item = classes.buy_item(id_num, product_name, buy_date,
                                   buy_price, expiration_date)

    # Write to file
    with open('bought.csv', 'a', newline='') as csvfile:
        buy_line = {'ID': bought_item.id_num,
                    'product name': bought_item.product_name,
                    'buy date': bought_item.buy_date,
                    'buy price': bought_item.buy_price,
                    'expiration date': bought_item.expiration_date, }
        field_names = ['ID', 'product name',
                       'buy date', 'buy price', 'expiration date']
        write = csv.DictWriter(csvfile, fieldnames=field_names)
        write.writerow(buy_line)

    console.print(f'[green]Added {product_name} to inventory[/green]')


def create_inventory(reportdate='today', dict_needed='counted_inventory'):
    # Convert cli-argument into usable date object
    check_this_date = ''
    if reportdate == 'today':
        check_this_date = date_functions.read_date()
    elif reportdate == 'yesterday':
        check_this_date = date_functions.yesterday()
    else:
        check_this_date = date_functions.convert_str_to_date(reportdate)

    # Only put items in inventory that were bought on or before the reportdate
    # This results in bought_before_date dictionary list
    bought_dicts = file_functions.read_csv_into_dict('bought.csv')
    bought_before_reportdate = []
    for dictionaries in bought_dicts:
        bought_date = date_functions.convert_str_to_date(
            dictionaries['buy date'])
        if bought_date <= check_this_date:
            bought_before_reportdate.append(dictionaries)

    # Read sold.csv and note bought IDs, then remove those bought items from inventory
    # Only process items that were sold on or before reportdate
    # This results in inventory_with_expired dictionary list
    sold_dicts = file_functions.read_csv_into_dict('sold.csv')

    sold_before_reportdate = []
    for dictionaries in sold_dicts:
        sold_date = date_functions.convert_str_to_date(
            dictionaries['sell date'])
        if sold_date <= check_this_date:
            sold_before_reportdate.append(dictionaries)

    bought_ID_list = []
    for dictionaries in sold_before_reportdate:
        bought_ID_list.append(dictionaries['bought ID'])
    inventory_with_expired = [
        product for product in bought_before_reportdate if product['ID'] not in bought_ID_list]

    # Now remove expired items from inventory_with_expired
    # This results in inventory_within_date
    inventory_within_date = []
    for dictionaries in inventory_with_expired:
        expiry_date = date_functions.convert_str_to_date(
            dictionaries['expiration date'])
        if expiry_date >= check_this_date:
            inventory_within_date.append(dictionaries)

    # Sum identical items and note earliest expiry date.
    # This results in counted_inventory
    product_list = []  # Make list with unique product names
    for dictionaries in inventory_within_date:
        if dictionaries['product name'] not in product_list:
            product_list.append(dictionaries['product name'])
    iteration = 0
    counted_inventory = []
    for _ in range(len(product_list)):
        count = 0
        expiry_date = date_functions.futuredate()
        for dictionaries in inventory_within_date:
            if dictionaries['product name'] == product_list[iteration]:
                count += 1
                if date_functions.convert_str_to_date(dictionaries['expiration date']) < expiry_date:
                    expiry_date = date_functions.convert_str_to_date(
                        dictionaries['expiration date'])
        counted_inventory.append({'product name': product_list[iteration],
                                  'count': count,
                                  'earliest expiry date': date_functions.convert_date_to_str(expiry_date)})
        iteration += 1

    # Write counted_inventory to file, used for (rich)print_inventory()
    with open('inventory.csv', 'w', newline='') as csvfile:
        field_names = ['product name', 'count', 'earliest expiry date']
        write = csv.DictWriter(csvfile, fieldnames=field_names)
        write.writeheader()
        write.writerows(counted_inventory)

    if dict_needed == 'inventory_within_date':  # only required for record_sell()
        return inventory_within_date
    else:
        return counted_inventory, check_this_date


def record_sell(product_name, sell_price, ding):
    # Create list of items in stock with product name
    within_date_dicts = create_inventory(
        'today', dict_needed='inventory_within_date')
    matching_product_stock_dict = []
    product_in_stock = False

    for dictionaries in within_date_dicts:
        if dictionaries['product name'] == product_name:
            matching_product_stock_dict.append(dictionaries)
            product_in_stock = True

    if product_in_stock is False:
        console.print(
            f"[bold red]Item {product_name} is not in stock, cannot sell what you don't have[/bold red]")
        return

    # Check list for earliest expiring product and sell that
    future_date = date_functions.futuredate()
    ID_to_sell = ''
    for dictionaries in matching_product_stock_dict:
        product_date = date_functions.convert_str_to_date(
            dictionaries['expiration date'])
        if product_date < future_date:
            future_date = product_date
            ID_to_sell = dictionaries['ID']

    # Determine highest ID in sold.csv line.
    id_reader = list(csv.reader(open('sold.csv', 'r')))
    try:
        # Prints last line, first item of list
        highest_id = int(id_reader[-1][0])
    except ValueError:  # Empty sold.csv throws error
        highest_id = 0

    # Write to file
    id_num = highest_id + 1
    sell_date = date_functions.read_date()
    sold_item = classes.sell_item(id_num, ID_to_sell, sell_date, sell_price)
    with open('sold.csv', 'a', newline='') as csvfile:
        sell_line = {'ID': sold_item.id_num,
                     'bought ID': sold_item.bought_id,
                     'sell date': sold_item.sell_date,
                     'sell price': sold_item.sell_price}
        field_names = ['ID', 'bought ID',
                       'sell date', 'sell price']
        write = csv.DictWriter(csvfile, fieldnames=field_names)
        write.writerow(sell_line)

    console.print(f'[green]{product_name} sold[/green]')
    if ding == 'on':
        ding_ding(product_name)  # alerts owner to made sale


def report_revenue(reportdate, printvalue=True):
    reportdate, date_is_whole_month, end_date, print_string = date_functions.report_handle_date(
        reportdate)
    # Read sold.csv into dict
    revenue_dict = file_functions.read_csv_into_dict('sold.csv')
    total_revenue = 0

    if date_is_whole_month is False:  # Compare against single date
        for dictionaries in revenue_dict:
            item_date = date_functions.convert_str_to_date(
                dictionaries['sell date'])
            if item_date == reportdate:
                total_revenue = total_revenue + \
                    float(dictionaries['sell price'])

    if date_is_whole_month is True:  # Compare to date range
        for dictionaries in revenue_dict:
            item_date = date_functions.convert_str_to_date(
                dictionaries['sell date'])
            if reportdate <= item_date < end_date:
                total_revenue = total_revenue + \
                    float(dictionaries['sell price'])
    # Default function prints value, unless defined differently
    if printvalue is True:
        if print_string == 'in month (':
            console.print('Total revenue ' + print_string +
                          str(reportdate)[0:7] + ') is:')
        else:
            console.print('Total revenue ' + print_string +
                          str(reportdate) + ') is:')
        console.print('[cyan]€ {:.2f}[/cyan]'.format(total_revenue))
    else:
        return total_revenue


def report_profit(reportdate, printvalue=True):
    get_revenue_date = reportdate
    reportdate, date_is_whole_month, end_date, print_string = date_functions.report_handle_date(
        reportdate)

    # Read bought.csv and add items on date required
    cost_dict = file_functions.read_csv_into_dict('bought.csv')
    total_cost = 0

    if date_is_whole_month is False:  # compare against single date
        for dictionaries in cost_dict:
            item_date = date_functions.convert_str_to_date(
                dictionaries['buy date'])
            if item_date == reportdate:
                total_cost = total_cost + float(dictionaries['buy price'])

    if date_is_whole_month is True:  # compare to date range
        for dictionaries in cost_dict:
            item_date = date_functions.convert_str_to_date(
                dictionaries['buy date'])
            if reportdate <= item_date < end_date:
                total_cost = total_cost + float(dictionaries['buy price'])
    # Get revenue for same period and subtract cost from revenue
    total_revenue = report_revenue(get_revenue_date, False)
    total_profit = total_revenue - total_cost
    if printvalue is True:
        if print_string == 'in month (':
            console.print('Total profit ' + print_string +
                          str(reportdate)[0:7] + ') is:')
        else:
            console.print('Total profit ' + print_string +
                          str(reportdate) + ') is:')
        if total_profit >= 0:
            console.print('[green]€ {:.2f}[/green]'.format(total_profit))
        else:
            console.print('[red]€ {:.2f}[/red]'.format(total_profit))
    else:
        return total_profit


def richprint_inventory(reportdate):
    inventory = create_inventory(reportdate)
    if inventory == []:
        console.print(f'{reportdate}: ---inventory is empty---')
    else:
        with open('inventory.csv', 'r', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            title_string = 'Inventory: ' + reportdate
            table = Table(title=title_string,
                          header_style='bold cyan', show_lines=True)
            table.add_column('product name', style='pink3', no_wrap=True)
            table.add_column('count', style='pink3', no_wrap=True)
            table.add_column('earliest expiry date',
                             style='pink3', no_wrap=True)
            for row in csv_reader:
                print_values = list(row.values())
                table.add_row(*print_values)
            console.print(table)


def export(reportdate):
    # Creates up to date inventory.csv
    inventory, printdate = create_inventory(reportdate)
    printdate = date_functions.convert_date_to_str(printdate)
    if inventory == []:
        console.print(
            f'[bold red]ERROR: inventory (date: {reportdate}) is empty, file will not be exported.[/bold red]')
    else:
        filename = 'inventory-date-' + printdate + '___generated_on--' + \
            date_functions.datetimestring() + '.csv'
        # Copy inventory.csv to new filename.csv
        file_functions.copy_inventory_to_file(filename)


def ding_ding(productname):
    # Before you are able to use this feature, insert your homey_cloud_id in the requests.get URL.
    # After inserting ID, comment out or remove the console.print placeholder line
    # You can find this ID on https://developer.athom.com/tools/system

    prof_today = str(round(report_profit('today', False), 2))
    rev_today = str(round(report_revenue('today', False), 2))
    payload = productname + ' sold, total revenue today is €' + \
        rev_today + ', total profit is €' + prof_today
    '''requests.get(
        'https://<homey_cloud_id>.connect.athom.com/api/manager/logic/webhook/superpy-sale?tag=' + payload)'''
    console.print(
        'ding_ding() has been triggered, this is a placeholder since the webhook needs a valid homey_cloud_id')


if __name__ == '__main__':
    main()
