# superpy
<br/>

**What is superpy?**

Superpy is a basic inventory control software, designed for a supermarket.
Features include adding and removing products from inventory, and producing various reports (profit/revenue/current inventory).

<br/>

**Requirements:**

Superpy is designed and tested to run on a Windows 10 system. 

Python version required: _Python 3.9.2_

Python library required: _Rich_  (which can be installed using: 
<code>pip install rich</code>)

**Getting started:**

After pulling superpy to your local device, you will have 4 files (+ 1 readme file):


*date_functions.py* 

Basically handles anything to do with dates.
Setting the current date or advancing the date. It also handles string to date conversions and vice versa. 

*file_functions.py*

Handles reading and writing files. Checks if superpy is running in the correct directory. And if necessary creates files required to run the program (normally just the first time).

*classes.py*

Handles the buy_item and sell_item classes.

*main.py*

Handles all CLI commands and also all the logic for adding/removeing/adjusting the inventory.

After you have run all the command at least once, you will also have the following:

*bought.csv*

Log of all bought items

*sold.csv*

Log of all sold items

*inventory.csv*

Inventory file, used as a variable by the program.

*date.txt*

Stores date variable.



