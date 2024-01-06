#Send an SMS message through Twilio.
#installation: pip3 install twilio
import os
import sys
import twilio
from twilio.rest import Client
import account

account_sid = account.sid
auth_token = account.auth_token

client = Client(account_sid, auth_token)



def send_sms(msg):
	with open("formatting/numbers.txt") as f:
		line = f.readline()
	contacts = line.split(' ')
	numbers = []
	for x in contacts:
		x = '+1' + x
		numbers.append(x)

	print("Sending message: " + msg + "\n...\n...")

	counter = 0
	count1 = 0
	for x in numbers[0:-1]:
		try:
			message = client.messages.create(
						from_= account.sid,
						body = msg[:],
						to = x
						)
			count1 = count1 + 1
		except:
			print("error sending message to invalid number: " + x)
			counter = counter + 1
			count1 = count1 + 1
	print("Finished sending all " + str(count1) + " messages with " + str(counter) + " errors. Check logs for details.")

