from datetime import datetime
import random
from twilio.rest import Client

# initialization
n = 0
execute = True
funFactFile = 'funFacts.txt'
previousFactFile = 'previousFact.txt'
# stores in this order, account_sid, auth_token, toNumber, fromNumber
cacheFile = 'cache.txt'

# what time the message will be sent daily
sendAt = ('-1:30')
twilioClient = Client(ACCOUNT_SID, AUTH_TOKEN)

with open(cacheFile, 'r') as x:

    ACCOUNT_SID = x.readline()
    AUTH_TOKEN = x.readline()

    toNumber = x.readline()
    myNumber = x.readline()
    fromNumber = x.readline()

# gets the current time in hh:mm format
def calculateTime():
    now = datetime.now()

    hour = now.hour - 12
    minute = now.minute

    currentTime = (f'{hour}:{minute}')

    return currentTime

def getFunFact():
    with open(funFactFile, 'r') as x:
        lines = x.readlines()
        fact = lines[random.randint(0, len(lines) - 1)]

    return fact

# sends the message
def sendMessage():
    message = getFunFact()

    if n == 0:
        twilioClient.messages.create(to=toNumber, from_=fromNumber, body=message)
        twilioClient.messages.create(to=myNumber, from_=fromNumber, body=message)
        return

# main loop
def main():

    global execute, n

    currentTime = calculateTime()

    if currentTime == sendAt: # Send message
        sendMessage()
        # keeps sendMessage from being called multiple times
        n = 1

    else: # Recalculate time
        n = 0

        currentTime = calculateTime()
        print(currentTime)

if __name__ == '__main__':

    while execute == True:
        main()
