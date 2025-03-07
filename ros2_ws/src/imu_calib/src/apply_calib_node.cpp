#include <rclcpp/rclcpp.hpp>

#include "imu_calib/apply_calib.h"

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);

  auto calib = std::make_shared<imu_calib::ApplyCalib>();

  rclcpp::spin(calib);

  rclcpp::shutdown();

  return 0;
}
