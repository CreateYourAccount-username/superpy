# Imports
import argparse
import csv
import classes
import date_functions
import file_functions
from rich.console import Console
from rich.table import Table


# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# Your code below this line.

console = Console(style='cyan')


def main():
    file_functions.checkdir()  # this should execute before every CLI command
    args = cli_arguments()
    print(args)  # to be deleted

    if args.command == "report":
        report(args.reporttype, args.date)
    elif args.command == 'buy':
        try:
            date_functions.convert_str_to_date(args.expiry)
        except ValueError:
            console.print(
                '[red]ERROR: Something went wrong in the buy command[/red]')
        else:
            record_buy(args.product, args.price, args.expiry)
    elif args.command == 'sell':
        record_sell(args.product, args.price)
    elif args.command == 'advance-time':
        if args.days == 'reset':
            date_functions.write_date('today')
            console.print('Date successfully reset.')
            console.print('Current date is: ')
            console.print(date_functions.read_date())
        elif args.days == 'show':
            console.print('Current date is: ')
            console.print(date_functions.read_date())
        else:  # convert string input to int
            try:
                days = int(args.days)
                if days > 0:
                    date_functions.advance_date(days)
                else:
                    raise ValueError
            except ValueError:
                console.print(
                    '[bold red]invalid input, has to be positive integer, "reset" or "show"[/bold red]')

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
    report_parser.add_argument('date', help="date, in YYYY-MM-DD format, or using the word 'today' or 'yesterday'. \
                               for profit and revenue you can also use YYYY-MM\
                               to get report on whole month.")

    args = parser.parse_args()
    return args


def record_buy(product_name, buy_price, expiration_date):

    # Check for highest ID number, assumption: last line is highest
    # Read last line
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
    # read bought.csv file
    inventory_dicts = file_functions.read_csv_into_dict('bought.csv')
    #console.print('[yellow]Printing inventory_dict with bought.csv items[/yellow]')
    # console.print(inventory_dicts)
    # Read sold.csv and note bought IDs, then remove those bought items from inventory
    sold_dicts = []
    with open('sold.csv', 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            sold_dicts.append(row)
    # console.print('Printing sold dicts')
    # console.print(sold_dicts)
    bought_ID_list = []
    for dictionaries in sold_dicts:
        bought_ID_list.append(dictionaries['bought ID'])
    # console.print('Printing bought ID list')
    # console.print(bought_ID_list)
    inventory_dicts = [
        product for product in inventory_dicts if product['ID'] not in bought_ID_list]
    # console.print('[yellow]Printing inventory_dict with sold items removed[/yellow]')
    # console.print(inventory_dicts)

    # Catch reportdate today - yesterday - YYYY-MM-DD date
    check_this_date = ''
    if reportdate == 'today':
        check_this_date = date_functions.read_date()
    elif reportdate == 'yesterday':
        check_this_date = date_functions.yesterday()
    else:
        check_this_date = date_functions.convert_str_to_date(reportdate)

    within_date_dicts = []
    for dictionaries in inventory_dicts:
        expiry_date = date_functions.convert_str_to_date(
            dictionaries['expiration date'])
        if expiry_date >= check_this_date:
            within_date_dicts.append(dictionaries)
    #console.print('Printing within date dicts')
    # console.print(within_date_dicts)
    # END RESULT IS WITHIN_DATE_DICTs

    # list unique products
    product_list = []
    # make list with unique product names
    for dictionaries in within_date_dicts:
        if dictionaries['product name'] not in product_list:
            product_list.append(dictionaries['product name'])
    #console.print('Printing bought ID list')
    # console.print(product_list)
    iteration = 0
    # count number of products and take earliest expiry
    counted_inventory = []
    for x in range(len(product_list)):
        count = 0
        expiry_date = date_functions.futuredate()
        for dictionaries in within_date_dicts:
            if dictionaries['product name'] == product_list[iteration]:
                count += 1
                if date_functions.convert_str_to_date(dictionaries['expiration date']) < expiry_date:
                    expiry_date = date_functions.convert_str_to_date(
                        dictionaries['expiration date'])
        counted_inventory.append({'product name': product_list[iteration],
                                  'count': count,
                                  'earliest expiry date': date_functions.convert_date_to_str(expiry_date)})
        iteration += 1
    #console.print('[yellow]Printing counted inventory[/yellow]')
    # console.print(counted_inventory)
    # END RESULT IS COUNTED_INVENTORY

    # Write within_date_dicts to file
    with open('inventory.csv', 'w', newline='') as csvfile:
        field_names = ['product name', 'count', 'earliest expiry date']
        write = csv.DictWriter(csvfile, fieldnames=field_names)
        write.writeheader()
        # write.writerows(within_date_dicts)
        write.writerows(counted_inventory)

    if dict_needed == 'within_date_dicts':
        return within_date_dicts
    else:
        return counted_inventory
        # return within_date_dicts


def record_sell(product_name, sell_price):
    within_date_dicts = create_inventory(
        'today', dict_needed='within_date_dicts')

    # Create list of items in stock with product name
    matching_product_stock_dict = []
    product_in_stock = False

    for dictionaries in within_date_dicts:
        if dictionaries['product name'] == product_name:
            # print(product_name + ' in stock')
            matching_product_stock_dict.append(dictionaries)
            product_in_stock = True

    if product_in_stock is False:  # Error if not in stock
        console.print(
            f"[red]Item {product_name} is not in stock, cannot sell what you don't have")
        return

    # print('\t product names matched, printing matching product_stock_dict:')
    # print(matching_product_stock_dict)
    # Check list for oldest product and sell that
    future_date = date_functions.futuredate()
    ID_to_sell = ''
    for dictionaries in matching_product_stock_dict:
        product_date = date_functions.convert_str_to_date(
            dictionaries['expiration date'])
        if product_date < future_date:
            # print(dictionaries['ID'] + ' is the nearest expiration date')
            future_date = product_date
            ID_to_sell = dictionaries['ID']

    # Determine highest ID in sold.csv line.
    # Check for highest ID number, assumption: last line is highest
    # Read last line
    id_reader = list(csv.reader(open('sold.csv', 'r')))
    try:
        # prints last line, first item of list
        highest_id = int(id_reader[-1][0])
    except ValueError:  # Empty sold.csv throws error
        highest_id = 0

    # Now assemble sell_item class instance so you can write it to .csv
    id_num = highest_id + 1
    sell_date = date_functions.read_date()
    sold_item = classes.sell_item(id_num, ID_to_sell, sell_date, sell_price)

    # Write to file
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


def report_revenue(reportdate, printvalue=True):
    reportdate, date_is_whole_month, end_date, print_string = date_functions.report_handle_date(
        reportdate)
    # get revenue dict
    revenue_dict = file_functions.read_csv_into_dict('sold.csv')
    total_revenue = 0

    if date_is_whole_month is False:  # compare against single date
        for dictionaries in revenue_dict:
            item_date = date_functions.convert_str_to_date(
                dictionaries['sell date'])
            if item_date == reportdate:
                total_revenue = total_revenue + \
                    float(dictionaries['sell price'])

    if date_is_whole_month is True:  # compare to date range
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


def report_profit(reportdate):
    get_revenue_date = reportdate
    reportdate, date_is_whole_month, end_date, print_string = date_functions.report_handle_date(
        reportdate)

    # get cost_dict
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
    # get revenue for same period:
    total_revenue = report_revenue(get_revenue_date, False)
    total_profit = total_revenue - total_cost
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


def report(reporttype, reportdate):
    if reporttype == 'inventory':
        if reportdate == 'today':
            print_inventory(reportdate)
        elif reportdate == 'yesterday':
            print_inventory(reportdate)
        elif len(reportdate) == 10 and reportdate[:3].isnumeric() and reportdate[4] == '-' and reportdate[5:6].isnumeric() and reportdate[7] == '-' and reportdate[8:9].isnumeric():
            try:
                date_functions.convert_str_to_date(reportdate)
                print_inventory(reportdate)
            except:
                console.print(
                    '[red]Something went wrong in the inventory report command[/red]')
        else:
            console.print(
                "[red]ERROR: inventory report can only accept 'today', 'yesterday', or YYYY-MM-DD as input")
    if reporttype == 'profit':
        if reportdate != 'today' and reportdate != 'yesterday':
            # YYYY-MM = 7 chars
            if len(reportdate) == 7 and reportdate[:3].isnumeric() and reportdate[4] == '-' and reportdate[5:6].isnumeric():
                # console.print(f'Profit: {reportdate}')
                report_profit(reportdate)
           # YYYY-MM-DD = 10
            elif len(reportdate) == 10 and reportdate[:3].isnumeric() and reportdate[4] == '-' and reportdate[5:6].isnumeric() and reportdate[7] == '-' and reportdate[8:9].isnumeric():
                # console.print(f'Profit: {reportdate}')
                report_profit(reportdate)
            else:
                console.print(
                    "[red]ERROR: date has to be 'today', 'yesterday', YYYY-MM or YYYY-MM-DD [/red]")
        else:
            report_profit(reportdate)
    if reporttype == 'revenue':
        if reportdate != 'today' and reportdate != 'yesterday':
            # YYYY-MM = 7 chars
            if len(reportdate) == 7 and reportdate[:3].isnumeric() and reportdate[4] == '-' and reportdate[5:6].isnumeric():
                # console.print(f'Profit: {reportdate}')
                report_revenue(reportdate)
           # YYYY-MM-DD = 10
            elif len(reportdate) == 10 and reportdate[:3].isnumeric() and reportdate[4] == '-' and reportdate[5:6].isnumeric() and reportdate[7] == '-' and reportdate[8:9].isnumeric():
                # console.print(f'Profit: {reportdate}')
                report_revenue(reportdate)
            else:
                console.print(
                    "[red]ERROR: date has to be 'today', 'yesterday', YYYY-MM or YYYY-MM-DD [/red]")
        else:
            report_revenue(reportdate)
        # console.print(f'Revenue: {reportdate}')


def print_inventory(reportdate):
    inventory = create_inventory(reportdate)
    if inventory == []:
        console.print('[cyan]---empty inventory---[/cyan]')
    else:
        with open('inventory.csv', 'r', newline='') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            headers = [csv_reader.fieldnames]
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


if __name__ == '__main__':
    main()
