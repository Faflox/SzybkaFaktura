# Fast Invoice Creator
    Video Demo:  <URL HERE>

# Overview

Fast Invoice Creator is a desktop app made to help small businesses with accouning.
It's a free and private option to create an invoice without sharing your data with some on-line provider. It allows for .PDF creation that contains all of the necessary information (at least in Poland) to make it a legal document.

# Distinctiveness and Complexity

My app has a GUI made in tkinter, that makes the process of creating invoices more pleasing and generally easier than using a terminal. It also allows to check and change data before submitting to get rid of any unnecesay mistakes.

My main function is a tkinter loop that allows the app to run. All of the necessary tkinter code is layed down at the bottom of the project.py file. Tkinter app creates a lot of variables, that are needed for the invoice creation and enforces some rules, in case of a mistake. When it was possible I used lists or calendar widgets to make the user experience even easier. For fixed values I created dropdown menus. Two of the variables have additional functions, that prevent incorrect date injection. Those functions make sure that sale date won't be earlier than issue date and in case of changing the issue date set the value of sale date to be exactly the same.
After declaring variables the program creates 3 lists with labels, variables and names of those variables, checks for their quantity, that needs to be equal and using a for loop creates GUI. As far as I know this is the best approach for scaling this app, but there might be a better way to solve this, that I don't know about. Lastly, it creates a button that triggers submit_form function. It works only if the data passed to the GUI is correct.

submit_form function takes invoice_number and 3 other dictionaries and sends them to create_pdf function. It allows for better readability of the code and ensucer the data is passed correctly. It also triggers calc_payment_due_date function, that automatically sets the necessary two weeks date, using issue date of the invoice and the timedelta.

create_pdf function first checks if there is an existing directory made for invoices using the os module. If the folder does not exist, it creates one. The program than names the file using invoice number and current date thanks to datetime module and draws all the necessary data onto the file with correct labels. Package needed to create the .PDF is called reportlab. By using three separate tables the .PDF is clen and readable. User can chagne styles of every table to suit their needs with table.setStyle, but I personally prefer clean and minimalistic approach. After appending all the info to the .PDF function tries to save the file. If there is an error in the data provided there will be info about it in the console and the file won't be created. 

Tests check if the functions written in the main file work correctly. I've created some sample data, that fill the function and than measure feedback with expected results.

# Requirements 

Before starting the program create a venv and install requirements.txt