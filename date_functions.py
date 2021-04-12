from datetime import date, timedelta, datetime  # Allows for date calculations
import file_functions                           # To read/write files
from rich.console import Console                # Pretty console printing
import main                                     # Need inventory for advance_date()
import sys                                      # Used to exit program if error occurs

console = Console(style='cyan')


def read_date():  # Read current date from date.txt
    file_contents = open('date.txt', 'r')
    currentdate = file_contents.readline()
    currentdate = convert_str_to_date(currentdate)
    file_contents.close()
    return currentdate


def write_date(newdate):  # Write new date to date.txt
    if newdate == 'today':  # if input is today set today's date
        newdate = str(date.today())
    file_contents = open('date.txt', 'w')
    file_contents.write(newdate)
    file_contents.close
    return


def yesterday():
    today = read_date()
    yesterday = today + timedelta(days=-1)
    return yesterday


def advance_date(x):  # advance date by x days
    # create inventory before advancing date
    inv = main.create_inventory(dict_needed='inventory_within_date')
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
            console.print(f'[bold red]Item "{print_line} [/bold red]')
    return


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
            f'[red]ERROR: {x} is not a valid date, check if date exists and make sure order is correct: YYYY-MM-DD[/red]')
        sys.exit(1)
    return


def convert_date_to_str(x):
    x = datetime.strftime(x, '%Y-%m-%d')
    return x


def convert_str_to_month(x):
    try:
        x = datetime.strptime(x, '%Y-%m').date()
        return x
    except ValueError:
        console.print(f'[red]ERROR: {x} is not a valid date[/red]')
        quit()


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
        # reportdate is now the first day of the month, want the last day as well
        end_date = first_day_next_month(reportdate)
        date_is_whole_month = True
        print_string = 'in month ('
    return reportdate, date_is_whole_month, end_date, print_string


def first_day_next_month(x):  # used in report_handle_date()
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


def datetimestring():
    # Filename is YYYY-MM-DD--HH:MM:SS
    datetimestring = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
    return datetimestring
