from datetime import datetime
from time import sleep
import random
import json
from twilio.rest import Client

# initialization
n = 0
dupeBreakpoint = 100

execute = True

funFactFile = 'textFiles/funFacts.txt'
previousFactFile = 'textFiles/previousFact.txt'
cacheFile = 'cache/cache.json'

# what time the message will be sent daily
sendAt = ('-1:30')

with open(cacheFile, 'r') as x:

    jsonFile = json.load(x)

    credentials = jsonFile['Account-Credentials']
    phoneNums = jsonFile["Phone-Numbers"]

    ACCOUNT_SID = credentials["Account-SID"]
    AUTH_TOKEN = credentials["Auth-Token"]

    # i = 0

    # for numbers in phoneNums.values():

    #     if i == 0:
    #         i += 1
    #         continue
    #     else:
    #         print(numbers)

    # fromNumber = phoneNums["From"]
    # sendTo1 = phoneNums["num1"]
    # sendTo2 = phoneNums["num2"]
    # sendTo3 = phoneNums["num3"]

twilioClient = Client(ACCOUNT_SID, AUTH_TOKEN)

# gets the current time in hh:mm format
def calculateTime():
    now = datetime.now()

    hour = now.hour - 12
    minute = now.minute

    currentTime = (f'{hour}:{minute}')

    return currentTime

def previousFactFileHandling(num):

    with open(previousFactFile, 'a') as appendToFile:
        with open(previousFactFile, 'r') as readFromFile:

            lines = readFromFile.readlines()

            if len(lines) == dupeBreakpoint:

                with open(previousFactFile, 'w') as resetFile:
                    resetFile.writelines(str(num) + '\n')
                    return

            else:
                appendToFile.writelines(str(num) + '\n')
                return

def checkForDupe(randNum):

    with open(previousFactFile, 'r') as x:
        num = x.readlines()

        numList = [int(fact.strip()) for fact in num]

        if randNum in numList:
            return True

        else:
            return False

def getFunFact():
    with open(funFactFile, 'r') as x:
        lines = x.readlines()
        randomLineNumber = random.randint(0, len(lines) - 1)

    dupe = checkForDupe(randomLineNumber)

    if dupe:
        print('Got a duper!')
        return getFunFact()

    else:
        previousFactFileHandling(randomLineNumber)

        fact = lines[randomLineNumber]
        return fact

# sends the message
def sendMessage():

    if n == 0:
        message = getFunFact()

        i = 0

        for num in phoneNums.values():
            if i == 0:
                fromNumber = num
                i += 1
                continue
            else:
                twilioClient.messages.create(to=num, from_=fromNumber, body=message)
        # twilioClient.messages.create(to=sendTo1, from_=fromNumber, body=message)
        # twilioClient.messages.create(to=sendTo2, from_=fromNumber, body=message)
        # twilioClient.messages.create(to=sendTo3, from_=fromNumber, body=message)

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

sendMessage()

# if __name__ == '__main__':

#     try:
#         while execute == True:
#             main()
#     except KeyboardInterrupt: # Press Ctrl + C to terminate program
#         pass
