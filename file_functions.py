import os  # enable checkdir() function
import csv
import date_functions


def checkdir():  # Check current working directory is \superpy
    directory = os.getcwd()  # Full path
    directory = os.path.basename(directory)  # Get base directory

    if directory == 'superpy':
        # create 'date.txt' if not found
        if file_found('date.txt') is False:
            with open('date.txt', 'a', newline='') as newfile:
                newfile.write(
                    '')
            date_functions.write_date('today')
        # create 'bought.csv' if not found
        if file_found('bought.csv') is False:
            with open('bought.csv', 'a', newline='') as newfile:
                newfile.write(
                    'ID,product name,buy date,buy price,expiration date\n')
        # create 'sold.csv' if not found
        if file_found('sold.csv') is False:
            with open('sold.csv', 'a', newline='') as newfile:
                newfile.write(
                    'ID,bought ID,sell date,sell price\n')
        return True
    else:
        raise Exception('\tERROR Change working directory to \\superpy')


def file_found(filename):
    try:
        test_open = open(filename, 'r')
        test_open.close
        return True
    except FileNotFoundError:
        return False


def clear_files():
    checkdir()
    os.remove('bought.csv')
    os.remove('sold.csv')


def read_csv_into_dict(filename):
    list_of_dicts = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        line_count = 0  # deprecated?
        for row in csv_reader:
            # make list with all dictionaries
            list_of_dicts.append(row)
            line_count += 1  # deprecated?
    return list_of_dicts
