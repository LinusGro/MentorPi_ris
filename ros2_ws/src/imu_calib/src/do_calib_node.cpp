#include "rclcpp/rclcpp.hpp"
#include "imu_calib/do_calib.h"

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  auto calib = std::make_shared<imu_calib::DoCalib>();
  while (rclcpp::ok() && calib->running())
  {
    rclcpp::spin_some(calib);
  }

  rclcpp::shutdown();

  return 0;
}
