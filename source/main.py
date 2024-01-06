# System imports
import sys
import subprocess
import os
import csv
import twilio

# PyQt library imports
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui
from PyQt5.QtGui import QMovie, QTextOption, QStandardItemModel

# Local imports
import sms
import sms2
import mms
import client_connect

# Create the Main Window dimensions and add tabs 'Dashboard', 'Manage Contacts', 'Marketing', 
# 'Send ETA', 'Text', 'Messages', 'Account', and 'Updates'
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MARKETING PORTAL")
        self.setGeometry(50,50,750,1000)
        layout = QGridLayout()
        self.setLayout(layout)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.West)
        tabs.setMovable(True)
        tabs.setStyleSheet("font-size: 18pt")

        tabs.addTab(Dashboard(), "Dashboard")
        tabs.addTab(Contacts(), "Manage Contacts")
        tabs.addTab(Marketing(), "Marketing")
        tabs.addTab(Send_ETA(), "Send Template")
        tabs.addTab(Text(), "Custom Texting")
        tabs.addTab(Messages(), "Check Messages")
        tabs.addTab(Account(), "Account")
        tabs.addTab(Updates(), "Updates")
        layout.addWidget(tabs, 0, 0)

        self.setCentralWidget(tabs)

# Create a Dashboard page that displays an animated logo video
class Dashboard(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setAutoFillBackground(True)
        # set color palette
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#454545"))
        self.setPalette(palette)

        # Init UI
        self.resize(750, 900)
        label = QLabel(self)

        # Create and start the animation
        movie = QMovie("assets/dash.jpg")
        label.setMovie(movie)
        movie.start()

        self.show()

# Contacts page is used for uploading and viewing contacts with first & last names, phone and email
class Contacts(QWidget):
    def __init__(self, parent=None):
        # Initialising parent class
        QWidget.__init__(self)
        self.setAutoFillBackground(True)

        #set background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#454545"))
        self.setPalette(palette)
    
        # Create the QVBoxLayout so all widgets are stacked vertically
        verticalLayout = QVBoxLayout(self)

        # set a counter for initialization purposes
        if hasattr(self, 'counter'):
            self.counter = self.counter
        else:
            self.counter = 0

        # Creating a QPushButton for uploading new contacts
        self.upload_contacts = QPushButton("Upload New Contacts (.csv)")
        self.upload_contacts.setMinimumSize(0,0)
        self.upload_contacts.setStyleSheet("background-color: #697de0")
        self.upload_contacts.clicked.connect(self.openFile)
        verticalLayout.addWidget(self.upload_contacts)

        # Creating a QTableWidget with 4 Columns and maximum 4000 rows
        self.tableWidget = QTableWidget(4000, 4)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # Adding QTableWidget to the layout
        verticalLayout.addWidget(self.tableWidget)
        self.setLayout(verticalLayout)

        # initialize the table data with last contacts upload or 'contacts_init.csv'
        self.fillData(open('contacts_init.csv'))
    
    # function for opening a file dialog to select the contacts csv file
    def openFile(self):
        contacts_file, _ = QFileDialog.getOpenFileName(self, 'Open File', '/Users/dispatch/Documents/Contacts/', '*.csv')
        if contacts_file:
            with open(contacts_file, 'r') as file:
                self.dialect = csv.Sniffer().sniff(file.read(1024))
                file.seek(0)
                self.uploadData(file)
            with open(contacts_file, 'r') as file:
                self.dialect = csv.Sniffer().sniff(file.read(1024))
                file.seek(0)
                self.copyData(file)
    # function for filling a table with the data from the contacts csv
    def fillData(self, contacts):
        # read data from CSV file to check for delimiter
        self.dialect = csv.Sniffer().sniff(contacts.read(1024))
        contacts.seek(0)
        if self.dialect.delimiter == ',':
            csv_reader = csv.reader(contacts, delimiter=',')
        else:
            csv_reader = csv.reader(contacts, delimiter='\t')

        # if data has already been initialized, clear all the table
        if self.counter > 0:
            self.rowCount = self.tableWidget.rowCount()
            self.colCount = self.tableWidget.columnCount()
            for i in range(self.rowCount):
                for j in range(self.colCount):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(''))

        # populate the table
        for row_num, row_data in enumerate(csv_reader):
            for col_num, col_data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(col_data)))

        #Setting the headline for each column
        self.tableWidget.setHorizontalHeaderLabels(["First", "Last", "Phone Number", "Email Address"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # setting the cell size
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        # increment the initialization counter
        if self.counter == 0:
            self.counter = self.counter + 1

        # close numbers.txt file
        contacts.close()
    # function takes in the phone numbers from the new csv file and puts them in a sigle string in a .txt file to be used for sms bulk sending
    def uploadData(self, csvFile):
        with csvFile as file_in:
            with open("formatting/numbers.txt", 'w') as file_out:
                for line in file_in:
                    if self.dialect.delimiter == ',':
                        line = line.split(',')
                    else:
                        line = line.split('\t')
                    row_data = line[2]
                    file_out.write("{}".format(row_data))
                    if line != line[-1]:
                        file_out.write(', ')
            file_out.close()
            file_in.seek(0)
            self.fillData(file_in)
    # copy the data from new csv upload and save it into directory to populate the table in the future
    def copyData(self, csvFile):
        with csvFile as file_in:
#            dialect = csv.Sniffer().sniff(file_in.read(1024))
#            file_in.seek(0)
            with open('contacts_init.csv', 'w', newline='') as file_out:
                reader = csv.reader(file_in)
                writer = csv.writer(file_out, delimiter='\t')
                for line in file_in:
                    if self.dialect.delimiter == ',':
                        line = line.split(',')
                    else:
                        line = line.split('\t')
                    first = line[0]
                    last = line[1]
                    phone = line[2]
                    email = line[3]
                    writer.writerow([first, last, phone, email])
        file_in.close()
        file_out.close()

# Marketing is for sending bulk SMS or MMS to all contacts
class Marketing(QWidget):
    def __init__(self):
        #initialize the widget
        QWidget.__init__(self)

        #set background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#454545"))
        self.setPalette(palette)

         # set up the overall layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # set up the form for entering input
        form = QFormLayout()
        self.layout.addLayout(form)

        # add message box with placeholder text
        self.message_box = QTextEdit()
        self.message_box.setFixedSize(690,400)
        self.message_box.setPlaceholderText("                                   Enter the message you would like to send...")
        self.message_box.setWordWrapMode(QTextOption.WordWrap)
        form.addRow(self.message_box)

        # add field for attaching media
        self.form_media = QLineEdit()
        self.form_media.setMinimumSize(500,40)
        self.form_media.setPlaceholderText(" Enter media url (https://www.sgmembersonly.online/[media])")
        form.addRow("Attach Photo/Video?: ", self.form_media)

	# instructions for properly entering phone number(s)
        self.warning = QLabel(self)
        self.warning.setMinimumWidth(100)
        self.warning.setFixedHeight(200)
        self.warning.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.warning.setText("Upload a supported file type to site backend or image hosting site,\n and provide the media URL.\nSupported file types: jpeg, png, gif (600KB or smaller)")
        self.warning.setStyleSheet("background-color: #74dd6c; opacity: 0.5;")
        self.warning.setAlignment(Qt.AlignCenter)
        form.addRow(self.warning)

        # set up the 'send to all contacts' push button
        send = QPushButton("    Send To All Contacts (Bulk)   ")
        send.setMinimumSize(400,40)
        send.setStyleSheet("background-color: #697de0")
        self.layout.addWidget(send)
        send.clicked.connect(self.sendMessage)

        self.show()

    # define the slot to process the button click
    # function will access sms.py script and run it with the given message
    def sendMessage(self):
        message = self.message_box.toPlainText()
        media = self.form_media.text()
        if media:
            mms.send_mms(message, media)
        else:
            if message:
                sms.send_sms(message)
            else:
                print("no message")

# Text tab is for sending SMS to one or more specified contacts
class Text(QWidget):
    def __init__(self):
        #initialize the widget 
        QWidget.__init__(self)

        #set background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#454545"))
        self.setPalette(palette)

         # set up the overall layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # set up the form for entering input
        form = QFormLayout()
        self.layout.addLayout(form)

        # add message box with placeholder text
        self.message_box = QTextEdit()
        self.message_box.setFixedSize(690,400)
        self.message_box.setPlaceholderText("                                   Enter the message you would like to send...")
        self.message_box.setWordWrapMode(QTextOption.WordWrap)
        form.addRow(self.message_box)

        # add field for attaching media
        self.form_numbers = QLineEdit()
        self.form_numbers.setMinimumSize(500,40)
        self.form_numbers.setPlaceholderText(" Enter each 10 digit customer number....")
        form.addRow("Phone Number(s): ", self.form_numbers)

	# instructions for properly entering phone number(s)
        self.warning = QLabel(self)
        self.warning.setMinimumWidth(100)
        self.warning.setFixedHeight(200)
        self.warning.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.warning.setText("Separate each number with a single space only: \n You must leave a single space at the very end of all of the numbers.\n Example: '9998887777 1112223333 6665554444 '")
        self.warning.setStyleSheet("background-color: #74dd6c; opacity: 0.5;")
        self.warning.setAlignment(Qt.AlignCenter)
        form.addRow(self.warning)

        # set up the 'send to all contacts' push button
        send = QPushButton("    Send To Specified Customer(s)   ")
        send.setMinimumSize(400,40)
        send.setStyleSheet("background-color: #697de0;")
        self.layout.addWidget(send)
        send.clicked.connect(self.sendMessage)

        self.show()

    # define the slot to process the button click
    # function will access sms.py script and run it with the given message
    def sendMessage(self):
        message = self.message_box.toPlainText()
        numbers = self.form_numbers.text()
        if message:
                sms2.send_sms(message, numbers)
        else:
                print("no message")

# Send ETA tab is for calculating the time it will take for delivery, and sending that ETA to the client
class Send_ETA(QWidget):
    def __init__(self):
        # initialize the widget
        super(Send_ETA, self).__init__()

        #set Background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#454545"))
        self.setPalette(palette)

        # set up the overall layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # set up the form for entering input
        form = QFormLayout()
        self.layout.addLayout(form)

        # add fields for route, courier, and client
        self.form_route = QLineEdit()
        self.form_route.setMinimumSize(400,40)
        self.form_route.setPlaceholderText("    Starting Address...")
        form.addRow("Route: ", self.form_route)

        self.form_end = QLineEdit()
        self.form_end.setMinimumSize(400,40)
        self.form_end.setPlaceholderText("    Ending Address...")
        form.addRow("", self.form_end)

        btn_calculate = QPushButton("    Calculate Total Delivery Time   ")
        btn_calculate.setMinimumSize(0,0)
        btn_calculate.setStyleSheet("background-color: #697de0")
#	format the button to calculate the ETA
#	btn_calculate.clicked.connect()
        form.addWidget(btn_calculate)

        self.form_ETA = QLineEdit()
        self.form_ETA.setMinimumSize(400,40)
        self.form_ETA.setPlaceholderText("    ETA In Minutes...")
        form.addRow("Delivery Estimated Duration:", self.form_ETA)

        self.form_client = QLineEdit()
        self.form_client.setMinimumSize(400,40)
        self.form_client.setPlaceholderText("    10 Digits...")
        form.addRow("Client Phone: ", self.form_client)

        # define the connect button
        btn_connect = QPushButton("Begin Delivery / Send Client an ETA")
        btn_connect.setMinimumSize(400,40)
        btn_connect.setStyleSheet("background-color: #697de0")
        btn_connect.clicked.connect(self.connect)
        self.layout.addWidget(btn_connect)

        # Label Creation
        self.output_label = QLabel("")
        #self.output_label.setMaximumSize(700,500)
        self.output_label.setWordWrap(True)
        self.layout.addWidget(self.output_label)

        # show the widget
        self.show()
    # connect function sends an SMS to client with the estimated ETA
    def connect(self):
        # define the variables for the route, courier, and client
        eta = self.form_ETA.text()
        client = self.form_client.text()

        # check the validity of the inputs
        if eta == "" or client == "":
            self.output_label.setText("Please provide the ETA and client phone number for connection.")
            print("Please provide the ETA and client phone number for connection.")
            return
        else:
            self.output_label.clear()

        eta2 = int(eta) + 10
        msg = "Hello! This is a message from Standard Green. Your order is on the way and should arrive in " + eta + " to " + str(eta2) + " minutes. You are now connected with dispatch/support and can text us here with any questions, or for an updated ETA." 

        client_connect.connect(client, msg)

        # print message to console
        self.output_label.setText("Conected dispatch to client '" + client + "' and gave the client an ETA of '" + eta + " to " + str(eta2) + " minutes'")
        print("Connected dispatch to client '" + client + "' and gave the client an ETA of '" + eta + " to " + str(eta2) + " minutes'")

# Messages populates a list of all twilio messages into a table
class Messages(QWidget):
    def __init__(self):
        super().__init__()

    	#set background color
        self.setAutoFillBackground(True)
        # color palette
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#454545"))
        self.setPalette(palette)
        # set grid layout and add a table
        self.grid = QVBoxLayout()
        self.button = QPushButton('Check Messages and Load Data')
        self.button.setStyleSheet("background-color: #697de0")
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.grid.addWidget(self.button)
        self.grid.addWidget(self.table)
        self.setLayout(self.grid)
        self.button.clicked.connect(self.loadData)
        self.table.setWordWrap(True)

    def loadData(self):
        os.system("chmod +x check_logs.sh && ./check_logs.sh")
        print("Finished checking all messages")
        file_data = open('assets/message_logs.tsv','r', encoding="utf-8").readlines() 
        header = [x for x in file_data[0].strip().split('\t')]
        self.table.setColumnCount(len(header))
        self.table.setHorizontalHeaderLabels(header)
        row = 1
        self.table.setRowCount(row)
        for row_data in file_data[1:]:
            row_data = row_data.strip().split('\t')
            self.table.insertRow(row)
            column = 0
            for cell_data in row_data:
                self.table.setItem(row,column, QTableWidgetItem(cell_data))
                column += 1
            row += 1

# account and license information
class Account(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #set background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#454545"))
        self.setPalette(palette)

        # Create a grid layout
        grid = QGridLayout()

        # Add labels and textboxes
        # Row 1 (Account Sid)
        grid.addWidget(QLabel("         Account SID: Your Account SID will appear here"), 0, 0)

        # Row 2 (Auth Token)
        grid.addWidget(QLabel("         Auth Token: Your Account Token will appear here"), 1, 0)

        # Row 3 (Twilio Phone)
        grid.addWidget(QLabel("         Phone Number: Your assigned Account Phone Number will appear here"), 2, 0)

        # Row 4 (License)
        terms = QLabel()
        terms.setWordWrap(True)

        terms.setText("Terms & Conditions:\n1. This software is owned and created by Eric Stevens (e.bst@pm.me), 'The Developer', specifically for previewing purposes.\n2. Any unauthorized possession, duplication or use of this software is prohibited.\n3. The Developer is the sole and exclusive owner of this software and all of its content.")
        terms.setStyleSheet("background-color: #74dd6c; font-size: 42px; color: black;")
        grid.addWidget(terms)

        self.setLayout(grid)
#       self.setGeometry(300, 300, 300, 200)
        self.show()

# run a bash script to update homebrew and python (pip3) dependencies
class Updates(QWidget):
    def __init__(self):
        super().__init__()

        #set background color
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#454545"))
        self.setPalette(palette)

        self.grid = QVBoxLayout()
        self.button = QPushButton('Run Updates')
        self.button.setStyleSheet("background-color: #697de0")
        self.button.clicked.connect(self.runUpdates)
        self.grid.addWidget(self.button)
        self.setLayout(self.grid)
        
        # create a text edit box to pipe the terminal output from running updates.sh
        self.terminalSTD = QTextEdit()
        self.terminalSTD.setFixedSize(700,700)

        # add QTextEdit to layout
        self.grid.addWidget(self.terminalSTD)

    def runUpdates(self):
        os.system('brew update && brew upgrade')
        os.system('python3 -m ensurepip --upgrade')
        os.system('pip3 install --upgrade PyQt5')
        os.system('pip3 install --upgrade twilio')
        self.terminalSTD.setText("Finished all updates successfully.")

# initialization of application and window
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
