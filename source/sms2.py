#Send an SMS message through Twilio.
#installation: pip3 install twilio
import os
import sys
from twilio.rest import Client
import account

account_sid = account.sid
auth_token = account.auth_token

client = Client(account_sid, auth_token)



def send_sms(msg, nums):
	contacts = nums.split(' ')
	numbers = []
	for x in contacts:
		x = '+1' + x
		numbers.append(x)

	print("Sending message: " + msg + "\n...\n...\nTo: ")
	print(numbers)
	counter = 0
	count1 = 0
	for x in numbers[0:-1]:
		try:
			message = client.messages.create(
						messaging_service_sid = account.service_sid,
						body = msg[:],
						to = x
						)
			count1 = count1 + 1
		except:
			counter = counter + 1
			count1 = count1 + 1
	print("Finished sending all " + str(count1) + " messages with " + str(counter) + " errors. Check logs for details.")
