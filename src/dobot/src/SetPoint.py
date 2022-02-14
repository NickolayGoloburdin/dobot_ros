#!/usr/bin/env python

import rospy
import math as m
from dobot.srv import NotePoint
from geometry_msgs.msg import Point
import time
pub = rospy.Publisher('/Point',Point, queue_size=10)
l1 = 138
l2 = 0
l3= 135.013
l4 = 147.085
l5 = 31
l6 = 13
def SetPoint(data):
    if data.x == 0:
        if data.y > 0:
            alpha1 = m.pi/2
        if data.y < 0:
            alpha1 = -m.pi/2
    else:
        alpha1 = m.atan2(data.y,data.x)

    x = data.x -(l2 + l5)*m.cos(alpha1)
    y = data.y -(l2 + l5)*m.sin(alpha1)
    z = data.z + l6 -l1
    k = m.sqrt(m.pow(x,2)+m.pow(y,2))
    d = m.sqrt(m.pow(k,2)+m.pow(z,2))
    if (k!=0 and d!=0):
        alpha2 = m.pi/2 - m.atan2(z,k) - m.acos((m.pow(d,2)+m.pow(l3,2)-m.pow(l4,2))/(2*d*l3))
        alpha3 = (m.pi - m.acos((m.pow(l3,2)+m.pow(l4,2)-m.pow(d,2))/(2*l4*l3))) - alpha2 
        if ((alpha1 < 2.108 and (alpha1 > -2.395) and (alpha2 > -0.184) and (alpha2 < 2) and (alpha3 > -0.3403392) and (alpha3 < 2))):
            msg = Point()
            msg.x = alpha1
            msg.y = alpha2
            msg.z = alpha3
            pub.publish(msg)
            time.sleep(3)
            return ("Succesfull")
        else:
            return("Point outside of working zone")
    
    else:
        return ("Error Point")
    #else:
    #    return("Point outside of working zone")


rospy.init_node('SetPoint')

service=rospy.Service('SetPoint',NotePoint,SetPoint)

rospy.spin()