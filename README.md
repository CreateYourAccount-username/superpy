
# What is superpy?

Superpy is a basic inventory control software, designed for a supermarket.
Features include adding and removing products from inventory, and producing various reports (profit/revenue/current inventory).

<br/>

# Requirements:

Superpy is designed and tested to run on a Windows 10 system. 

Python version required: _Python 3.9.2_

Python library required: _Rich_  (which can be installed using: 
<code>pip install rich</code>)

<br/>

# Getting started:

After pulling superpy to your local device, you will have 5 files:

- *date_functions.py* - Basically handles anything to do with dates. Setting the current date or advancing the date. It also handles string to date conversions and vice versa. 

- *file_functions.py* - Handles reading and writing files. Checks if superpy is running in the correct directory. And if necessary creates files required to run the program (normally just the first time).

- *classes.py* - Handles the buy_item and sell_item classes.

- *main.py* - Handles all CLI commands and also all the logic for adding/removeing/adjusting the inventory.

- *README.md* - The readme file you are currently reading.

After you have run all the various commands at least once, you will also have the following files:

- *bought.csv* - Log of all bought items

- *sold.csv* - Log of all sold items

- *inventory.csv* - Inventory file, used as a variable by the program.

- *date.txt* - Stores date variable.

# Using superpy

There are 4 different commands that you can use. 
- buy
- sell
- advance-time
- report

This is also reflected by using the command <code>python main.py -h</code>

## buy 

## sell

## advance-time
Make use of the advance-time command by typing <code>python main.py advance-time *x*</code>
Where *x* can be substituted the following: 

- *show* - This will display the current date. 
    ```
    > python main.py advance-time show
    Current date is:
    2021-04-07
    ```

*reset* - This will reset the date to match the system's date.
    ```
    > python main.py advance-time reset
    Date successfully reset.
    Current date is:
    2021-04-07
    ```



Help can also be accessed from the command line using: 
<code>python main.py advance-time -h</code>
## report

