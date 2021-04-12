import os               # Read file and directory names
import csv              # Read/write .csv files
import date_functions   # Collaborate with date_functions


def checkdir():
    directory = os.getcwd()  # Full path
    directory = os.path.basename(directory)  # Get base directory

    if directory == 'superpy':  # Check current working directory is \superpy
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
        return
    else:
        raise Exception('\tERROR Change working directory to \\superpy')


def file_found(filename):
    try:
        test_open = open(filename, 'r')
        test_open.close
        return True
    except FileNotFoundError:
        return False


def read_csv_into_dict(filename):
    list_of_dicts = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            list_of_dicts.append(row)
    return list_of_dicts


def copy_inventory_to_file(filename):
    try:
        os.mkdir('export')
    except:
        FileExistsError
        pass
    os.system('copy inventory.csv export\\' + filename)
