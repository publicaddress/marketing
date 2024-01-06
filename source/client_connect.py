#Send an SMS message through Twilio.
#installation: pip3 install twilio
import os
import sys
#import couriers.csv
from twilio.rest import Client
import account

account_sid = account.sid
auth_token = account.auth_token
client = Client(account_sid, auth_token)

def connect(customer, msg):
	# courier # below is a placeholder, needs to be updated for csv searching by Employee ID
	# to matching Employee Phone Number. Similar functionality should be coded for client name
	# and matching phone number from contacts.csv file
	courier = ""
	customer.strip()
	customer = "+1" + customer
	message = client.messages.create(
					from_= courier,
					body = msg[:],
					to = customer
					)
	print(message.sid)
