#Send an MMS message through Twilio.
#installation: pip3 install twilio
from twilio.rest import Client
import account

account_sid = account.sid
auth_token = account.auth_token
client = Client(account_sid, auth_token)


def send_mms(msg, media):
	with open("formatting/numbers.txt") as f:
        	line = f.readline()
	contacts = line.split(' ')
	numbers = []
	for x in contacts:
        	x = '+1' + x
	        numbers.append(x)

	print("Sending message: " + msg + "\nSending media at url: " + media + "\n...\n...")

	counter = 0
	count1 = 0
	for x in numbers[0:-1]:
		try:
			message = client.messages.create(
						from_ = '',
						body = msg[:],
						media_url=media[:],
						to = x
					)
		except:
			print("error sending message to invalid number: " + x)
			counter = counter + 1
			count1 = count1 + 1
	print("Finished sending all " + str(count1) + " messages with " + str(counter) + " errors. Check logs for details.")

