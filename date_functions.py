from datetime import date, timedelta, datetime
import file_functions
from rich.console import Console
import main

console = Console(style='cyan')


def read_date():  # Read current date from date.txt
    if file_functions.checkdir() is True:
        # Read current date in date.txt
        file_contents = open('date.txt', 'r')
        currentdate = file_contents.readline()
        currentdate = convert_str_to_date(currentdate)
        file_contents.close()
        return currentdate


def write_date(newdate):  # Write new date to date.txt
    if file_functions.checkdir() is True:
        if newdate == 'today':  # if input is today set today's date
            newdate = str(date.today())
        file_contents = open('date.txt', 'w')
        file_contents.write(newdate)
        file_contents.close
        return


def advance_date(x):  # advance date by x days
    # create inventory before advancing date
    inv = main.create_inventory(dict_needed='inventory_dicts')
    startdate = read_date()
    enddate = startdate + timedelta(days=x)
    enddate_date_object = enddate  # for use in if statement later
    # convert date object to string
    enddate = datetime.strftime(enddate, '%Y-%m-%d')
    write_date(enddate)
    console.print(f'date is advanced by {x} days')
    console.print(f'new date is {read_date()}')
    for items in inv:
        exp_date = convert_str_to_date(items['expiration date'])
        if exp_date < enddate_date_object:
            print_line = items['product name'] + '" expired on: ' \
                + items['expiration date']
            # console.print(print_line, style='bold red')
            console.print(f'[bold red]Item "{print_line} [/bold red]')


def futuredate():
    far_future_date = '2121-12-31'  # set date in far future
    far_future_date = datetime.strptime(far_future_date, '%Y-%m-%d').date()
    return far_future_date


def convert_str_to_date(x):
    try:
        x = datetime.strptime(x, '%Y-%m-%d').date()
        return x
    except ValueError:
        console.print(
            '[red]ERROR: input is not a valid date[/red]')
        quit()


def convert_date_to_str(x):
    x = datetime.strftime(x, '%Y-%m-%d')
    return x


def convert_str_to_month(x):
    try:
        x = datetime.strptime(x, '%Y-%m').date()
        return x
    except ValueError:
        console.print(
            '[red]ERROR: input is not a valid date[/red]')
        quit()


def first_day_next_month(x):
    # split into year and month
    month = datetime.strftime(x, '%m')
    year = datetime.strftime(x, '%Y')
    # go to next calendar month
    if month == '12':
        year = int(year) + 1
        year = str(year)
        month = 1
    else:
        month = int(month) + 1
        month = str(month)
    # form into string and then date object
    month_later = year + '-' + month
    month_later = datetime.strptime(month_later, '%Y-%m').date()
    return month_later


def report_handle_date(reportdate):
    # This section figures out if date is single date or whole month
    # Also expressions 'today/yesterday' are converted to date
    date_is_whole_month = False
    end_date = ''
    print_string = ''
    # catch 'today' and 'yesterday' input
    if reportdate == 'today':  # if input is today set today's date
        reportdate = read_date()
        print_string = 'today ('
    elif reportdate == 'yesterday':  # if input is today set today's date
        reportdate = read_date() + timedelta(days=-1)
        print_string = 'yesterday ('
    elif len(reportdate) == 10:  # ISO date
        reportdate = convert_str_to_date(reportdate)
        print_string = 'on date ('
    elif len(reportdate) == 7:  # YYYY-MM object
        # take current month
        reportdate = convert_str_to_month(reportdate)
        # x is now the first day of the month, want the last day as well
        end_date = first_day_next_month(reportdate)
        date_is_whole_month = True
        print_string = 'in month ('
    return reportdate, date_is_whole_month, end_date, print_string
