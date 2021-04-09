# Report
Please include a short, 300-word report that highlights three technical elements of your implementation that you find notable, explain what problem they solve and why you chose to implement it in this way. Include this in your repository as a report.md file.

##  rich console:
Implemented Rich Console, very helpful for understanding the console at a quick glance. For example using:
```
    else:
        console.print(
            f'[red]ERROR: {args.expiry} is not a valid date, enter in YYYY-MM-DD format.[/red]')
```
When you see a long bright red line that starts with ERROR it is very clear something is wrong and needs attention.
Similarly when querying for the profits on a specific date it will print green for profit and red for loss. Even before you start to read the exact number you will know if it is good or bad news:
```
    if total_profit >= 0:
        console.print('[green]€ {:.2f}[/green]'.format(total_profit))
    else:
        console.print('[red]€ {:.2f}[/red]'.format(total_profit))
```
## File handling

Every function is called via main(), which is always run trough the
```
    if __name__ == '__main__':
        main()
```
code at the bottom of main.py.
By including some code at the start of main(), I have made sure there are some checks done before the CLI commands are run. 
```
    def main():
        file_functions.checkdir()  # this should execute before every CLI command
```
This code calls the checkdir() function in file_functions.py which has a few features.
It checks if the current working dir is correct: 
```
    if directory == 'superpy':
    (....)
    else:
        raise Exception('\tERROR Change working directory to \\superpy')
```

And if some required files don't exist, it will create new ones in the correct format: 
```
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
```

## Home Automation and phone notifications
Just for fun added a link that interacts with my Homey home automation controller. Inspired by the movie Middle Men (2009) I thought it would be funny that a sale would generate a doorbell (ding! ding!) inside my house. Akin to the buzzer sounding when they had a sale in the movie. I then added a little bit extra to teach myself how to pass information to Homey from superpy. This results in a bit of text being send, being the product name, total revenue and profits for the day. 
The way it's implemented by default it is not used and there are no extra commands used to leave it off. Only if you want to use it (novelty wears off quickly) you have to specify an extra command. 
This is handled in the following code <code>sell_parser.add_argument('--ding', default='off', (...))</code>

Obviously I took out my private key from the code. You can insert your own Homey cloud ID and then create the following flow: 

![homey flow](https://github.com/CreateYourAccount-username/superpy/blob/CreateYourAccount-images/homey%20flow.png?raw=true)

In combination with the Homey Telegram Bot this results in the following notification on your phone. 
![phone notification](https://github.com/CreateYourAccount-username/superpy/blob/CreateYourAccount-images/notification.jpg?raw=true)

