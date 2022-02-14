#!/usr/bin/env python
import paho.mqtt.client as mqtt
from time import sleep
import rospy
import json
from std_msgs.msg import String, Bool

from sensor_msgs.msg import JointState
# cam1_pub = rospy.Publisher("camera_left", String, queue_size = 2)
class Mqtt_pc:
	def __init__(self):
		self.client = mqtt.Client()
		self.client.connect("pc",1883,60) 
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.loop_start()
		self.publisher_back = rospy.Publisher("/point_reached", Bool, queue_size = 1)
	
	def on_connect(self,client, userdata, flags, rc):
		print("Connected with result code "+str(rc))
		self.client.subscribe("joint_states")
		self.client.subscribe("service")

	def on_message(self,client, userdata, msg): 
		data = msg.payload.decode()
		#try:
		if msg.topic == "joint_states":
			info = json.loads(data)
			msg_js = JointState()
			msg_js.name = info["name"]
			msg_js.position = info["position"]
			msg_js.velocity = info["velocity"]
			publisher_js = rospy.Publisher("joint_states_new", JointState, queue_size = 1)
			msg_js.header.stamp = rospy.Time.now()
			publisher_js.publish(msg_js)
			# print info
		elif msg.topic == "service":
			#print data
			msg_pr = Bool()
			if data=="True":
				msg_pr.data = True
			else:
				msg_pr.data = False
			self.publisher_back.publish(msg_pr) 
	#except Exception as e :
		#	print e
	def publish_mqtt(self,topic,data):
		self.client.publish(topic, data)
	def disconnect(self):
		self.client.disconnect()

def point_callback(data):
	mqtt_pc.publish_mqtt("point", data.data)

if __name__ == "__main__":
	rospy.init_node('mqtt_sender')
	rospy.Subscriber("/target_point", String, point_callback)
	mqtt_pc = Mqtt_pc()
	while not rospy.is_shutdown():
		try:
			# client.publish("feedback", "got message")
			rospy.sleep(0.1)
		except e as Exception:
			print("bie")
			mqtt_nanopi.disconnect()
			break
