import rospy
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool


class Corridor:
    def init(self):
        self.cor_dist = 1.0
        rospy.Subscriber('/scan', LaserScan, self.Lidar_cb)
        self.pub = rospy.Publisher('in_corridor_MC', Bool, queue_size=5)
        self.in_corridor = False
        self.count = 0


    def Lidar_cb(self, msg):
        front_left  = min(msg.ranges[80:100])
        front_right = min(msg.ranges[260:280])

        if (front_left + front_right) < self.cor_dist and self.count <= 10:
            self.count += 1
        elif (front_left + front_right) >= self.cor_dist and self.count >= 0: 
            self.count -= 1
        if self.count > 10:
            self.in_corridor = True
        elif self.count < 0:
            self.in_corridor = False

        self.pub.publish(self.in_corridor)