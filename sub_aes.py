import time
import base64
import hashlib
import zlib
import bz2
import binascii
import sys
import paho.mqtt.client as mqtt
import key_gen as kg
from Crypto.Cipher import AES
from Crypto import Random


BLOCK_SIZE =16

print (kg.key)
#key='abcdefghijklmnop'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def decrypt(enc):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(kg.key, AES.MODE_OFB, iv)
    return unpad(cipher.decrypt(enc[16:]))

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print (kg.key)
    print ("\n")

    # Recieve the payload - It's in bytes
    m1_update = msg.payload
    print(type(m1_update))
    print("1. Initial Payload  :" + str(m1_update) + "\n")

    #Decompress the payload
    #m2_update = bz2.decompress(m1_update)
    m2_update = zlib.decompress(m1_update)
    print(type(m2_update))
    print("2. Decompressed  :" + str(m2_update) + "\n")

    #Decrypt the payload
    m3_update = decrypt(m2_update)
    print("3. Decrypt : " + str(m3_update) + "\n")

    #Convert it into text
    m4_update = m3_update.decode('utf-8')
    print("4. Final code : " + m4_update + "\n")

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)


# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("192.168.1.180", 1883, 60)
mqttc.subscribe("topic/test", 0)

mqttc.loop_forever()
