import passw
import paho.mqtt.client as mqtt
import os, urlparse

#led=0/1
#sensor=p/l/i
def accion(msg):
	if(msg=='5000+3000'):
		mensaje=msg.split('+')
		a=int(mensaje[0])
		b=int(mensaje[1])
		c=a+b
		print('suma = '+str(c))
		if(msg=='5000-3000'):
			mensaje2=msg.split('-')
			n=int(mensaje2[0])
			m=int(mensaje2[1])
			d=n-m
			print('resta = '+str(d))

# Define event callbacks
    
def publish(msg):
	#print (msg)
	mqttc.publish(topic_tx, msg)

def on_connect(client, userdata, flags, rc):
	print("rc: " + str(rc))

def on_message(client, obj, msg):

	print(str('new message='+msg.payload))
	accion(str(msg.payload))

def on_publish(client, obj, mid):
	#print("mid: " + str(mid))
	pass

def on_subscribe(client, obj, mid, granted_qos):
	print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(client, obj, level, string):
	print(string)

mqttc = mqtt.Client()
# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

# Uncomment to enable debug messages
#mqttc.on_log = on_log

# Connect
mqttc.username_pw_set(passw.user, passw.psw)
mqttc.connect(passw.server, passw.port)
topic_tx='test'
# Start subscribe, with QoS level 0
mqttc.subscribe('led', 0)

# Publish a message
mqttc.publish(topic_tx, 'test')
#mqttc.publish(topic,topic)
# Continue the network loop, exit when an error occurs
rc = 0
import time
i=0
while rc == 0:
	time.sleep(2)
	i=i+1
	#publish('i='+str(i))
	rc=mqttc.loop()
print("rc: " + str(rc))

import RPi.GPIO as GPIO
import sys
import datetime
import Adafruit_DHT

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pin_to_circuit = 13

def rc_time (pin_to_circuit):
	count = 0
  
	#Output on the pin for 
	GPIO.setup(pin_to_circuit, GPIO.OUT)
	GPIO.output(pin_to_circuit, GPIO.LOW)
	time.sleep(0.1)

    #Change the pin back to input
	GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
	while (GPIO.input(pin_to_circuit) == GPIO.LOW):
		count += 1

	return count

#Catch when script is interrupted, cleanup correctly
try:
	# Main loop
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(11, 16)
		print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
		publish('Temp= '+str(temperature))
		rc=mqttc.loop()
		publish('Temp= '+str(humidity))
		rc=mqttc.loop()
		print(rc_time(pin_to_circuit))
		publish(str(rc_time(pin_to_circuit)))
		rc=mqttc.loop()
except KeyboardInterrupt:
    pass
finally:
	GPIO.cleanup()








