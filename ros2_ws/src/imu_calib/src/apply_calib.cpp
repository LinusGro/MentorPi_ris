#include "imu_calib/apply_calib.h"

namespace imu_calib
{

ApplyCalib::ApplyCalib() :
  rclcpp::Node("apply_calib"),
  gyro_sample_count_(0),
  gyro_bias_x_(0.0),
  gyro_bias_y_(0.0),
  gyro_bias_z_(0.0)
{
  std::string calib_file;
  this->declare_parameter<std::string>("calib_file", "imu_calib.yaml");
  calib_file = this->get_parameter("calib_file").as_string();
  if (!calib_.loadCalib(calib_file) || !calib_.calibReady())
  {
    RCLCPP_FATAL(this->get_logger(), "Calibration could not be loaded");
    rclcpp::shutdown();
  }

  this->declare_parameter<bool>("calibrate_gyros", true);
  calibrate_gyros_ = this->get_parameter("calibrate_gyros").as_bool();

  this->declare_parameter<int>("gyro_calib_samples", 100);
  gyro_calib_samples_ = this->get_parameter("gyro_calib_samples").as_int();

  int queue_size;
  this->declare_parameter<int>("queue_size", 5);
  queue_size = this->get_parameter("queue_size").as_int();

  raw_sub_ = this->create_subscription<sensor_msgs::msg::Imu>("raw", queue_size, std::bind(&ApplyCalib::rawImuCallback, this, std::placeholders::_1));
  corrected_pub_ = this->create_publisher<sensor_msgs::msg::Imu>("corrected", queue_size);
}

void ApplyCalib::rawImuCallback(sensor_msgs::msg::Imu::SharedPtr raw)
{
  if (calibrate_gyros_)
  {
    RCLCPP_INFO_ONCE(this->get_logger(), "Calibrating gyros; do not move the IMU");

    // recursively compute mean gyro measurements
    gyro_sample_count_++;
    gyro_bias_x_ = ((gyro_sample_count_ - 1) * gyro_bias_x_ + raw->angular_velocity.x) / gyro_sample_count_;
    gyro_bias_y_ = ((gyro_sample_count_ - 1) * gyro_bias_y_ + raw->angular_velocity.y) / gyro_sample_count_;
    gyro_bias_z_ = ((gyro_sample_count_ - 1) * gyro_bias_z_ + raw->angular_velocity.z) / gyro_sample_count_;

    if (gyro_sample_count_ >= gyro_calib_samples_)
    {
      RCLCPP_INFO(this->get_logger(), "Gyro calibration complete! (bias = [%.3f, %.3f, %.3f])", gyro_bias_x_, gyro_bias_y_, gyro_bias_z_);
      calibrate_gyros_ = false;
    }

    return;
  }

  sensor_msgs::msg::Imu corrected = *raw;

  calib_.applyCalib(raw->linear_acceleration.x, raw->linear_acceleration.y, raw->linear_acceleration.z,
                    &corrected.linear_acceleration.x, &corrected.linear_acceleration.y, &corrected.linear_acceleration.z);

  corrected.angular_velocity.x -= gyro_bias_x_;
  corrected.angular_velocity.y -= gyro_bias_y_;
  corrected.angular_velocity.z -= gyro_bias_z_;

  corrected_pub_->publish(corrected);
}

} // namespace accel_calib
