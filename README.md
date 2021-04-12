
# What is superpy?

Superpy is a basic inventory control software, designed for a supermarket.
Features include adding and removing products from inventory, and producing various reports (profit/revenue/current inventory).

<br/>

# Requirements:

Superpy is designed and tested to run on a Windows 10 system. 

Python version required: _Python 3.9.2_

Python library required: 
- _Rich_  (which can be installed using: 
<code>pip install rich</code>)


- _requests_ (which can be installed using: 
<code>pip install requests</code>)
<br/>

# Installation:

Use your terminal to navigate to the directory that you want to install superpy into. Then run the git clone command. Git cloning will create a superpy directory. So if you want to install <code>c:\winc_apps\superpy</code>, navigate to <code>c:\winc_apps\\</code> and then run the command: 
<code>git clone https://github.com/CreateYourAccount-username/superpy.git</code>

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
Make us of the *buy* command by typing <code>python main.py buy --product \<product> --price  \<price> --expiry  \<expiry></code>.

- ### --product arguments
    Recommend using one word only, but you can use a string with spaces if you use quotes (' or "), for example: <code>-product 'apple pie'</code>. The short form is <code>-prod</code>, example:  <code>-prod 'apple pie'</code>.

- ### --price arguments
    Price needs to be defined using <code>.</code> before a decimal. (not a <code>,</code> as is commonly used in The Netherlands). Example: <code> --price 1.15</code>. The short form is <code>-$ </code> (even though the program is in €, but € didn't seem to work in the terminal during testing), example <code> -$ 1.15</code>

- ### --expiry arguments
    This date needs to be in ISO 8601 format (YYYY-MM-DD) format. This means a month or day with a single digit will need a 0 in front. For example, the 9th of April 2021 is 2021-04-09. For example <code>--expiry 2021-08-31</code>. Short form is <code>-exp</code>, example <code>--exp 2021-08-31</code>

Examples of the *buy* command:
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

Make us of the *sell* command by typing <code>python main.py sell --product \<product> --price  \<price> --ding  \<ding></code>.
- ### --product arguments
    Recommend using one word only, but you can use a string with spaces if you use quotes (' or "), for example: <code>-product 'apple pie'</code>. The short form is <code>-prod</code>, example:  <code>-prod 'apple pie'</code>.

- ### --price arguments
    Price needs to be defined using <code>.</code> before a decimal. (not a <code>,</code> as is commonly used in The Netherlands). Example: <code> --price 1.15</code>. The short form is <code>-$ </code> (even though the program is in €, but € didn't seem to work in the terminal during testing), example <code> -$ 1.15</code>

- ### --ding arguments
    Can only be *on* or *off*, any other value will be rejected. This argument is optional and defaults to *off*. If set to *on*, it will initiate a HTTP GET webhook into your Homey home automation controller with a tag that includes the product sold, total revenue on the day and total profit on the day. See REPORT.md for more information. Use wisely, use is guaranteed to be annoying, hence default value is *off*.
    Note: This cannot be used unless you have inserted the Homey Cloud ID into the code (see dingding() in main.py for more info)

Examples of the *sell* command:
```
> python main.py sell --product 'apple pie' --price 6.45
apple pie sold
```
```
> python main.py sell -prod apple -$ 2
apple sold
```
```
> python main.py sell --product 'apple pie' --price 6.45
Item apple pie is not in stock, cannot sell what you don't have
```
```
> python main.py sell -prod 'toilet paper' -$ 5 --ding on
toilet paper sold
```

Help can also be accessed from the command line using: 
<code>python main.py sell -h</code>

## **report**
Make use of the *report* command by typing <code>python main.py advance-time \<type> --date \<date>.</code>
Where *\<type*> is the type of report and *\<date>* is the date or period you want the report for. 
<br/>

### \<type> arguments
The following reports are possible:

- *inventory* - this gives the inventory on the date given. 
- *revenue* - this gives the total revenue (total income) for the date or period given.
- *profit* - this gives the total profits (total income minus total costs) for the date or period given.
  
<br/>

### \<date> arguments (optional)


- *today* - this is de default value and gives todays report. if you don't specify --date, it will default to today, for example: 
```
    > python main.py report inventory
               Inventory: today
    ┏━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ product name ┃ count ┃ earliest expiry date ┃
    ┡━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
    │ mars_bar     │ 2     │ 2021-04-09           │
    ├──────────────┼───────┼──────────────────────┤
    │ snickers     │ 3     │ 2030-05-05           │
    └──────────────┴───────┴──────────────────────┘
```
```
    > python main.py report inventory --date today
                Inventory: today
    ┏━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓
    ┃ product name ┃ count ┃ earliest expiry date ┃
    ┡━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩
    │ mars_bar     │ 2     │ 2021-04-09           │
    ├──────────────┼───────┼──────────────────────┤
    │ snickers     │ 3     │ 2030-05-05           │
    └──────────────┴───────┴──────────────────────┘
```
```
    > python main.py report profit
    Total profit today (2021-04-09) is:
    € -16.98
```
```
    > python main.py report profit --date today
    Total profit today (2021-04-09) is:
    € -16.98
```
- *yesterday* - gives yesterdays report, for example
```
    > python main.py report revenue --date yesterday
    Total revenue yesterday (2021-04-08) is:
    € 0.00
```
- *specific date* - needs to be in ISO 8601 format (YYYY-MM-DD). This means a month or day with a single digit will need a 0 in front. For example, the 9th of April 2021 is 2021-04-09. Example: 
```
    > python main.py report revenue --date 2021-04-09
    Total revenue on date (2021-04-09) is:
    € 8.45
```
- *whole month* - this only works with *profit* and *revenue*, **not with *inventory***. Input is required to be in YYYY-MM format. This means a month with single digit needs a 0 in front. For example, April 2021 is 2021-04. Example: 
```
    > python main.py report revenue --date 2021-04
    Total revenue in month (2021-04) is:
    € 8.45
```
Help can also be accessed from the command line using: 
<code>python main.py report -h</code>


