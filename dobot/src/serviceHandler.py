#!/usr/bin/env python3
from time import sleep
import rospy
from std_msgs.msg import String, Bool
from dobot.srv import NotePoint


class Servie_handler:
    def __init__(self):
        rospy.Subscriber("cmd_point", String, self.cmd_callback)
        self.client_serv = rospy.ServiceProxy('/cmd_point', NotePoint)
        self.publisher = rospy.Publisher("service_back", Bool, queue_size=1)

    def cmd_callback(self, data):
        respa = self.client_serv(data.data)
        # print respa.result
        msg = Bool()
        msg.data = respa.result
        self.publisher.publish(msg)


if __name__ == "__main__":
    rospy.init_node('servie_handler')
    servie_handler = Servie_handler()
    while not rospy.is_shutdown():
        try:
            # client.publish("feedback", "got message")
            rospy.sleep(0.1)
        except e as Exception:
            print("bie")
            mqtt_nanopi.disconnect()
            break
