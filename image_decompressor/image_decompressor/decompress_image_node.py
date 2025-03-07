import rclpy
import logging
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage, Image
import cv2
from cv_bridge import CvBridge

class DecompressImageNode(Node):
    def __init__(self):
        super().__init__('decompress_image_node')

        # Create a CvBridge instance for converting images
        self.bridge = CvBridge()

        # Subscription to the compressed image topic
        self.subscription = self.create_subscription(
            CompressedImage,
            '/ascamera/camera_publisher/rgb0/image_compressed',  # Input topic
            self.callback,
            10
        )

        # Publisher for the decompressed image
        self.publisher = self.create_publisher(
            Image,
            '/decompressed_image',  # Output topic
            10
        )

        self.get_logger().info('DecompressImageNode has been started.')

    def callback(self, compressed_msg):
        try:
            logging.debug("In the callback method")
            # Convert the compressed image to a CV2 image
            np_arr = self.bridge.compressed_imgmsg_to_cv2(compressed_msg, desired_encoding='bgr8')

            # Convert the CV2 image back to a ROS Image message
            image_msg = self.bridge.cv2_to_imgmsg(np_arr, encoding='bgr8')

            # Copy header information from the compressed message
            image_msg.header = compressed_msg.header

            # Publish the decompressed image
            self.publisher.publish(image_msg)

            logging.debug('Published decompressed image.')
        except Exception as e:
            self.get_logger().error(f'Failed to decompress image: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = DecompressImageNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
