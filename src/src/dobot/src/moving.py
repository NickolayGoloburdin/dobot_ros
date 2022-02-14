#!/usr/bin/python
import time
import rospy
import math as m
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from geometry_msgs.msg import Point
class JointsCrt:
	def __init__(self):
		self.beta1 = 0
		self.beta2 = 0
		self.beta3 = 0
		self.beta = 0
		self.sub = rospy.Subscriber("/Point", Point, self.callback)
		self.pub = rospy.Publisher("/joints", Point, queue_size=10)

	def sign(self,num):
		if num>0:
			return float(1)
		if num<0:
			return float(-1)
		if num ==0:
			return float(0)

	def callback(self,data):
		msg = Point()
		alpha1 = data.x
		alpha2 = data.y
		alpha3 = data.z
		da1 = self.sign((alpha1-self.beta1))/100
		da2 = self.sign((alpha2-self.beta2))/100
		da3 = self.sign((alpha3-self.beta3))/100
		while (((round(alpha1,2)-round(self.beta1,2))!=0) or ((round(alpha2,2)-round(self.beta2,2))!=0) or ((round(alpha3,2)-round(self.beta3,2))!=0)):
			if ((round(alpha1,2)-round(self.beta1,2)) !=0):
				self.beta1 += da1
			if ((round(alpha2,2)-round(self.beta2,2)) !=0):
				self.beta2 += da2
			if ((round(alpha3,2)-round(self.beta3,2)) !=0):
				self.beta3 += da3
			msg.x = self.beta1
			msg.y = self.beta2
			msg.z = self.beta2
			self.pub.publish(msg)
			time.sleep(0.02)
		self.beta1 = alpha1
		self.beta2 = alpha2
		self.beta3 = alpha3
		

if __name__ == '__main__':
    rospy.init_node('RevKinem')

    JointsCrt()
    rospy.spin()
