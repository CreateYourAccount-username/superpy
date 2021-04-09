
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

# Installation:

***XXXXXXXXXXX Create 'superpy' dir and pull from git***

After pulling superpy to your local device, you will have 5 files:

- *classes.py* - Handles the buy_item and sell_item classes.

- *date_functions.py* - Basically handles anything to do with dates. Setting the current date or advancing the date. It also handles string to date conversions and vice versa. 

- *file_functions.py* - Handles reading and writing files. Checks if superpy is running in the correct directory. And if necessary creates files required to run the program (normally just the first time).

- *main.py* - Handles all CLI commands and also all the logic for adding/removeing/adjusting the inventory.

- *README.md* - The readme file you are currently reading.

After you have run all the various commands at least once, you will also have the following files:

- *bought.csv* - Log of all bought items

- *date.txt* - Stores date variable.

- *inventory.csv* - Inventory file, used as a variable by the program.

- *sold.csv* - Log of all sold items

# Using superpy

Before you start, ***make sure you are working from directory 'superpy'.***

There are 4 different commands that you can use. 
- buy
- sell
- advance-time
- report

This is also reflected by using the command <code>python main.py -h</code>

## **advance-time**
Make use of the *advance-time* command by typing <code>python main.py advance-time *x*</code>
Where *x* can be substituted the following: 

- *show* - This will display the current date. 
    ```
    > python main.py advance-time show
    Current date is:
    2021-04-07
    ```

- *reset* - This will reset the date to match the system's date.
    ```
    > python main.py advance-time reset
    Date successfully reset.
    Current date is:
    2021-04-07
    ```
- The amount of days you want to advance your date with. Has to be a positive integer.
    ```
    > python main.py advance-time 10
    date is advanced by 10 days
    new date is 2021-04-17
    ```

Superpy will inform you when products have expired in the days that you have skipped, for example:
```
    > python main.py advance-time 10
    date is advanced by 10 days
    new date is 2021-04-17
    Item "orange" expired on: 2021-04-10
```

Keep in mind the superpy software does not automatically advance its date every day, due to customer requirements. Every new day the customer should command the software to update it's internal date to the current date using <code>python main.py advance-time reset</code>

Help can also be accessed from the command line using: 
<code>python main.py advance-time -h</code>

## **buy** 
Make us of the *buy* command by typing <code>python main.py buy --product \<product> --price  \<price> --expiry  \<expiry>.</code>

- ### --product arguments
Recommend using one word only, but you can use a string with spaces if you use quotes (' or "), for example: <code>-product 'apple pie'</code>. The short form is <code>-prod</code>, example:  <code>-prod 'apple pie'</code>.

- ### --price arguments
Price needs to be defined using <code>.</code> before a decimal. (not a <code>,</code> as is commonly used in The Netherlands). Example: <code> --price 1.15</code>. The short form is <code>-$ </code> (even though the program is in €, but € didn't seem to work in the terminal during testing), example <code> -$ 1.15</code>

- ### --expiry arguments
This date needs to be in ISO 8601 format (YYYY-MM-DD) format. This means a month or day with a single digit will need a 0 in front. For example, the 9th of April 2021 is 2021-04-09. For example <code>--expiry 2021-08-31</code>. Short form is <code>-exp</code>, example <code>--exp 2021-08-31</code>

Examples of the buy command:
```
> python main.py buy --product apple --price 0.50 --expiry 2021-04-28
Added apple to inventory
```
```
> python main.py buy --prod 'apple pie' -$ 3.50 --exp 2021-04-28
Added apple pie to inventory
```


Help can also be accessed from the command line using: 
<code>python main.py buy -h</code>

## **sell**


## **report**
Make use of the *report* command by typing <code>python main.py advance-time \<type> \<date>.</code>
Where *\<type*> is the type of report and *\<date>* is the date or period you want the report for. 
<br/>

### \<type> arguments
The following reports are possible:

- *inventory* - this gives the inventory on the date given. 
- *revenue* - this gives the total revenue (total income) for the date or period given.
- *profit* - this gives the total profits (total income minus total costs) for the date or period given.
  
<br/>

### \<date> arguments
Note: **The only *\<date>* options for *inventory* are either *today* or *yesterday*.** For *revenue* and *profit* you can use all of the following arguments:

- *today* - gives todays report, for example: 
```
    > python main.py report inventory today
    Inventory now is:
    ┏━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ product name ┃ count ┃ earliest expiry date ┃
    ┡━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
    │       orange │     2 │           2021-04-10 │
    ├──────────────┼───────┼──────────────────────┤
    │        apple │     3 │           2021-08-31 │
    ├──────────────┼───────┼──────────────────────┤
    │       banana │     6 │           2021-04-09 │
    └──────────────┴───────┴──────────────────────┘
```
- *yesterday* - gives yesterdays report, for example
```
    > python main.py report revenue yesterday
    Revenue: yesterday
    Total revenue yesterday (2021-04-08) is:
    € 10.0
```
- *specific date* - needs to be in ISO 8601 format (YYYY-MM-DD). This means a month or day with a single digit will need a 0 in front. For example, the 9th of April 2021 is 2021-04-09. Example: 
```
    > python main.py report revenue 2021-03-29
    Revenue: 2021-03-29
    Total revenue on date (2021-03-29) is:
    € 11.0
```
- *whole month* - needs to be in YYYY-MM format. This means a month with single digit needs a 0 in front. For example, April 2021 is 2021-04. Example: 
```
    > python main.py report revenue 2021-03
    Revenue: 2021-03
    Total revenue in month (2021-03) is:
    € 101.50
```



