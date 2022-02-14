#!/usr/bin/env python
import paho.mqtt.client as mqtt
from time import sleep
import rospy
import json
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState
from dobot.srv import NotePoint
class Mqtt_nanopi:
	def __init__(self):
		self.client = mqtt.Client()
		self.client.connect("pc",1883,60) 
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.loop_start()
		self.publisher_cmd = rospy.Publisher("cmd_point", String, queue_size=1)
		rospy.Subscriber("service_back", Bool, self.service_callback)
	def on_connect(self,client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		self.client.subscribe("point")

	def on_message(self,client, userdata, msg):
		data = msg.payload.decode()

		# print data
		if msg.topic == "point":
			msg_point = String()
			msg_point.data = data
			self.publisher_cmd.publish(msg_point)

	def service_callback(self,data):
		self.publish_mqtt("service",data.data)
	def publish_mqtt(self,topic,data):
		self.client.publish(topic, data)
	def disconnect(self):
		self.client.disconnect()

def arm_callback(data):
	converted = {
			"name": data.name,
			"position": data.position,
			"velocity": data.velocity
	}
	msg = json.dumps(converted)
	mqtt_nanopi.publish_mqtt("joint_states", msg)
	# print msg

if __name__ == "__main__":
	mqtt_nanopi = Mqtt_nanopi()
	rospy.init_node('mqtt_receiver')
	
	rospy.Subscriber("/joint_states_new", JointState, arm_callback)
	while not rospy.is_shutdown():
		try:
			# client.publish("feedback", "got message")
			rospy.sleep(0.1)
		except e as Exception:
			print("bie")
			mqtt_nanopi.disconnect()
			break
