import rclpy
from rclpy.node import Node
from drobo_interfaces.msg import PointDrive, DiffDrive

import pigpio
import struct

I2C_ADDR = 0x14
WRITE_DATA_SIZE = 16

class Controller2024b_B(Node):
    def __init__(self):
        self.pi = pigpio.pi()
        try:
            self.pi.bb_i2c_open(10, 11, 100000)
        except pigpio.error:
            print("既にbitbang i2cが設定されています")
        
        super().__init__('controller_2024b_B')
        self.point_2_3_sub = self.create_subscription(
            PointDrive,
            '/point_2_3',
            self.point_2_3_callback,
            10
        )
        self.point_2_3_msg = PointDrive()
        self.diff_2_3_sub = self.create_subscription(
            DiffDrive,
            '/diff',
            self.diff_2_3_callback,
            10
        )
        self.diff_2_3_msg = DiffDrive()
        self.timer = self.create_timer(0.01, self.i2c_send)

    def i2c_send(self):
        packet = struct.pack(
            "BBBBBHhhbbbbhhhBB",
            0x04,
            I2C_ADDR,
            0x02,
            0x07,
            WRITE_DATA_SIZE,
            3,
            self.diff_2_3_msg.left,
            self.diff_2_3_msg.right,
            self.point_2_3_msg.md2,
            self.point_2_3_msg.md3,
            self.point_2_3_msg.md4,
            self.point_2_3_msg.md5,
            0,
            0,
            0x10FF,
            0x03,
            0x00
        )
        self.pi.bb_i2c_zip(10, packet)
    
    def point_2_3_callback(self, msg):
        self.point_2_3_msg = msg

    def diff_2_3_callback(self, msg):
        self.diff_2_3_msg = msg
        
def main(args=None):
    rclpy.init(args=args)
    controller_2024b_B = Controller2024b_B()
    rclpy.spin(controller_2024b_B)
    controller_2024b_B.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    
