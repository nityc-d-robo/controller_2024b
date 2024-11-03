import rclpy
from rclpy.node import Node
from drobo_interfaces.msg import PointDrive, DiffDrive

import pigpio
import struct

I2C_ADDR = 0x14
WRITE_DATA_SIZE = 16

class Controller2024b_2_4(Node):
    def __init__(self):
        self.is_subscribed = False
        self.pi = pigpio.pi()
        try:
            self.pi.bb_i2c_open(10, 11, 100000)
        except pigpio.error:
            print("既にbitbang i2cが設定されています")
        
        super().__init__('controller_2024b_2_4')
        self.point_2_4_sub = self.create_subscription(
            PointDrive,
            '/point_2_4',
            self.point_2_4_callback,
            10
        )
        self.point_2_4_msg = PointDrive()
        self.diff_2_4_sub = self.create_subscription(
            DiffDrive,
            '/diff',
            self.diff_2_4_callback,
            10
        )
        self.diff_2_4_msg = DiffDrive()
        self.timer = self.create_timer(0.05, self.i2c_send)

    def i2c_send(self):
        packet = struct.pack(
            "BBBBBHhhbbbbhhhBB",
            0x04,
            I2C_ADDR,
            0x02,
            0x07,
            WRITE_DATA_SIZE,
            2,
            self.point_2_4_msg.md0,
            self.point_2_4_msg.md1,
            self.point_2_4_msg.md2,
            self.point_2_4_msg.md3,
            self.point_2_4_msg.md4,
            self.point_2_4_msg.md5,
            self.diff_2_4_msg.left,
            self.diff_2_4_msg.right,
            0,
            0x03,
            0x00
        )
        self.pi.bb_i2c_zip(10, packet)
    
    def point_2_4_callback(self, msg):
        self.point_2_4_msg = msg
        self.is_subscribed = True

    def diff_2_4_callback(self, msg):
        self.diff_2_4_msg = msg
        self.is_subscribed = True
        
def main(args=None):
    rclpy.init(args=args)
    controller_2024b_2_4 = Controller2024b_2_4()
    rclpy.spin(controller_2024b_2_4)
    controller_2024b_2_4.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    
