import datetime
import random
import string

# key Generated must be of either 16,24,32 bytes

def randomStringwithDigitsAndSymbols(stringLength=10):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

currentDT = datetime.datetime.now()

if (currentDT.hour == 2 ):
    key='darkroastcoffees'
elif (currentDT.hour == 5 ):
    key='cappuccinoroastd'
elif (currentDT.hour == 8 ):
    key='frappuccinosaredisgusting!@#$%^4'
elif (currentDT.hour == 12 ):
    key='A^^mDnMKgadf9671'
elif (currentDT.hour == 18 ):
    key='tom&jerry@CNNmn@&9726869'
else:
    key='mochaisbalanced!'
