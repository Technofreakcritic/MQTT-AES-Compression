import time
import base64
import hashlib
import zlib
import bz2
import binascii
import key_gen as kg
import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE =16

#print(kg.key)

key='abcdefghijklmnop'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt(raw):
    #private_key = hashlib.sha256(password.encode("utf-8")).digest()
    raw = pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(kg.key, AES.MODE_OFB, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def on_connect(client, userdata, flags, rc):

    if rc == 0:

        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection

    else:

        print("Connection failed")

Connected = False   #global variable for the state of the connection

broker_address= "192.168.1.180"
port = 1883
user = ""
password = ""

client = mqtt.Client("topic/test")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
client.loop_start()        #start the loop
while Connected != True:    #Wait for connection
    time.sleep(0.1)

try:
    while True:

         #Get message
         # topic = input('Enter the message:')
         plaintext = input('Enter the message:')
         cnvrt_text_2_bytes = plaintext.encode('utf-8')
         compressed = bz2.compress(cnvrt_text_2_bytes)
         print ('Compressed : ', len(compressed), binascii.hexlify(compressed))

         #Compress the text
         #compressed_data = zlib.compress(cnvrt_text_2_bytes, 0)

         # First let us encrypt secret message
         #encrypted = encrypt(plaintext)
         encrypted = encrypt(str(compressed))

         print("1. The message :" + plaintext + "\n")
         print("2. The compressed message :" + str(compressed)+ "\n")
         print("3. Encrypted msg is : " + str(encrypted) + "\n\n")

         #print("Let's see if I can decrypt here \n")
         #decryped_text = decrypt(str(encrypted))
         #print("Decrypted message" + decryped_text)

         #client.publish("topic/test",compressed_data)
         client.publish("topic/test",encrypted)
         client.publish("penguins",encrypted)

except KeyboardInterrupt:

    client.disconnect()
    client.loop_stop()
