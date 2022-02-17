#!/usr/bin/python3
import time
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from geometry_msgs.msg import Point
class JointsCrt:
	def __init__(self):
		self.j1 = 0
		self.j2 = 0
		self.j3 = 0
		self.j4 = 0
		self.pub = rospy.Publisher("/joint_states", JointState, queue_size=10)
		self.sub = rospy.Subscriber("/joints", Point, self.callback_joints)

	def callback_joints(self,data):
		self.j1 = data.x
		self.j2 = data.y
		self.j3 = data.z

	def Pub(self):
		msg=JointState()
		msg.header = Header()
		msg.header.stamp = rospy.Time.now()
		msg.name = ['0-1','1-2','1-2_1','2-3','2_1-triangle','triangle-3_1','3_1-4']
		msg.position.append(self.j1)
		msg.position.append(-self.j2+1)
		msg.position.append(0)
		msg.position.append(-self.j3+0.65)
		msg.position.append(-self.j4)
		self.pub.publish(msg)

if __name__ == '__main__':
	rospy.init_node('PumModelJoints')
	jp = JointsCrt()
	r = rospy.Rate(20) # 20hz
	while not rospy.is_shutdown():
		jp.Pub()
		r.sleep()