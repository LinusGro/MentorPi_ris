#include "imu_calib/do_calib.h"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"

namespace imu_calib
{

DoCalib::DoCalib() :
  rclcpp::Node("do_calib"),
  state_(START)
{
  imu_sub_ = this->create_subscription<sensor_msgs::msg::Imu>("imu", 1, std::bind(&DoCalib::imuCallback, this, std::placeholders::_1));

  this->declare_parameter<int>("measurements", 500);
  this->declare_parameter<double>("reference_acceleration", 9.80665);
  this->declare_parameter<std::string>("output_file", "imu_calib.yaml");

  this->get_parameter("measurements", measurements_per_orientation_);
  this->get_parameter("reference_acceleration", reference_acceleration_);
  this->get_parameter("output_file", output_file_);

  orientations_.push(AccelCalib::XPOS);
  orientations_.push(AccelCalib::XNEG);
  orientations_.push(AccelCalib::YPOS);
  orientations_.push(AccelCalib::YNEG);
  orientations_.push(AccelCalib::ZPOS);
  orientations_.push(AccelCalib::ZNEG);

  orientation_labels_[AccelCalib::XPOS] = "X+";
  orientation_labels_[AccelCalib::XNEG] = "X-";
  orientation_labels_[AccelCalib::YPOS] = "Y+";
  orientation_labels_[AccelCalib::YNEG] = "Y-";
  orientation_labels_[AccelCalib::ZPOS] = "Z+";
  orientation_labels_[AccelCalib::ZNEG] = "Z-";
}

bool DoCalib::running()
{
  return state_ != DONE;
}

void DoCalib::imuCallback(const sensor_msgs::msg::Imu::SharedPtr imu)
{
  bool accepted;
  switch (state_)
  {
  case START:
    calib_.beginCalib(6*measurements_per_orientation_, reference_acceleration_);
    state_ = SWITCHING;
    break;


  case SWITCHING:
    if (orientations_.empty())
    {
      state_ = COMPUTING;
    }
    else
    {
      current_orientation_ = orientations_.front();

      orientations_.pop();
      measurements_received_ = 0;

      std::cout << "Orient IMU with " << orientation_labels_[current_orientation_] << " axis up and press Enter";
      std::cin.get();
      std::cout << "Recording measurements...";

      state_ = RECEIVING;
    }
    break;


  case RECEIVING:
    accepted = calib_.addMeasurement(current_orientation_,
                                     imu->linear_acceleration.x,
                                     imu->linear_acceleration.y,
                                     imu->linear_acceleration.z);

    measurements_received_ += accepted ? 1 : 0;
    if (measurements_received_ >= measurements_per_orientation_)
    {
      std::cout << " Done." << std::endl;
      state_ = SWITCHING;
    }
    break;


  case COMPUTING:
    std::cout << "Computing calibration parameters...";
    if (calib_.computeCalib())
    {
      std::cout << " Success!"  << std::endl;

      std::cout << "Saving calibration file...";
      if (calib_.saveCalib(output_file_))
      {
        std::cout << " Success!" << std::endl;
      }
      else
      {
        std::cout << " Failed." << std::endl;
      }
    }
    else
    {
      std::cout << " Failed.";
      RCLCPP_ERROR(this->get_logger(), "Calibration failed");
    }
    state_ = DONE;
    break;


  case DONE:
    break;
  }
}

} // namespace accel_calib
