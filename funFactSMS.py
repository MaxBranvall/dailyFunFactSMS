from datetime import datetime
from time import sleep
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

with open(cacheFile, 'r') as x:

    ACCOUNT_SID = x.readline()
    AUTH_TOKEN = x.readline()

    toNumber = x.readline()
    myNumber = x.readline()
    fromNumber = x.readline()

twilioClient = Client(ACCOUNT_SID, AUTH_TOKEN)

# gets the current time in hh:mm format
def calculateTime():
    now = datetime.now()

    hour = now.hour - 12
    minute = now.minute

    currentTime = (f'{hour}:{minute}')

    return currentTime

def checkForDupe(randNum):

    with open(previousFactFile, 'r') as x:
        num = x.readline()

        if int(num) == randNum:
            return True
        else:
            return False

def getFunFact():
    with open(funFactFile, 'r') as x:
        lines = x.readlines()
        randomLineNumber = random.randint(0, len(lines) - 1)

    dupe = checkForDupe(randomLineNumber)

    if dupe == True:
        print('Got a duper!')
        return getFunFact()

    else:
        with open(previousFactFile, 'w') as x:
            x.write(str(randomLineNumber))

        fact = lines[randomLineNumber]
        return fact

# sends the message
def sendMessage():

    if n == 0:
        message = getFunFact()
        twilioClient.messages.create(to=toNumber, from_=fromNumber, body=message)
        twilioClient.messages.create(to=myNumber, from_=fromNumber, body=message)

        print('Message Sent!')
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
        sleep(1)
        currentTime = calculateTime()

if __name__ == '__main__':

    while execute == True:
        main()
