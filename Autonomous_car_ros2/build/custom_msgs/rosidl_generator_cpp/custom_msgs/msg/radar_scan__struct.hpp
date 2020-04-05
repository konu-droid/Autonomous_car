// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msgs:msg/RadarScan.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__RADAR_SCAN__STRUCT_HPP_
#define CUSTOM_MSGS__MSG__RADAR_SCAN__STRUCT_HPP_

#include <rosidl_generator_cpp/bounded_vector.hpp>
#include <rosidl_generator_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__custom_msgs__msg__RadarScan __attribute__((deprecated))
#else
# define DEPRECATED__custom_msgs__msg__RadarScan __declspec(deprecated)
#endif

namespace custom_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RadarScan_
{
  using Type = RadarScan_<ContainerAllocator>;

  explicit RadarScan_(rosidl_generator_cpp::MessageInitialization _init = rosidl_generator_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_generator_cpp::MessageInitialization::ALL == _init ||
      rosidl_generator_cpp::MessageInitialization::ZERO == _init)
    {
      this->point_id = 0;
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->range = 0.0f;
      this->velocity = 0.0f;
      this->doppler_bin = 0;
      this->bearing = 0.0f;
      this->intensity = 0.0f;
    }
  }

  explicit RadarScan_(const ContainerAllocator & _alloc, rosidl_generator_cpp::MessageInitialization _init = rosidl_generator_cpp::MessageInitialization::ALL)
  : header(_alloc, _init)
  {
    if (rosidl_generator_cpp::MessageInitialization::ALL == _init ||
      rosidl_generator_cpp::MessageInitialization::ZERO == _init)
    {
      this->point_id = 0;
      this->x = 0.0f;
      this->y = 0.0f;
      this->z = 0.0f;
      this->range = 0.0f;
      this->velocity = 0.0f;
      this->doppler_bin = 0;
      this->bearing = 0.0f;
      this->intensity = 0.0f;
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _point_id_type =
    uint16_t;
  _point_id_type point_id;
  using _x_type =
    float;
  _x_type x;
  using _y_type =
    float;
  _y_type y;
  using _z_type =
    float;
  _z_type z;
  using _range_type =
    float;
  _range_type range;
  using _velocity_type =
    float;
  _velocity_type velocity;
  using _doppler_bin_type =
    uint16_t;
  _doppler_bin_type doppler_bin;
  using _bearing_type =
    float;
  _bearing_type bearing;
  using _intensity_type =
    float;
  _intensity_type intensity;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__point_id(
    const uint16_t & _arg)
  {
    this->point_id = _arg;
    return *this;
  }
  Type & set__x(
    const float & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const float & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const float & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__range(
    const float & _arg)
  {
    this->range = _arg;
    return *this;
  }
  Type & set__velocity(
    const float & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__doppler_bin(
    const uint16_t & _arg)
  {
    this->doppler_bin = _arg;
    return *this;
  }
  Type & set__bearing(
    const float & _arg)
  {
    this->bearing = _arg;
    return *this;
  }
  Type & set__intensity(
    const float & _arg)
  {
    this->intensity = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msgs::msg::RadarScan_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msgs::msg::RadarScan_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msgs::msg::RadarScan_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msgs::msg::RadarScan_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::RadarScan_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::RadarScan_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::RadarScan_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::RadarScan_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msgs::msg::RadarScan_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msgs::msg::RadarScan_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msgs__msg__RadarScan
    std::shared_ptr<custom_msgs::msg::RadarScan_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msgs__msg__RadarScan
    std::shared_ptr<custom_msgs::msg::RadarScan_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RadarScan_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->point_id != other.point_id) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->range != other.range) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->doppler_bin != other.doppler_bin) {
      return false;
    }
    if (this->bearing != other.bearing) {
      return false;
    }
    if (this->intensity != other.intensity) {
      return false;
    }
    return true;
  }
  bool operator!=(const RadarScan_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RadarScan_

// alias to use template instance with default allocator
using RadarScan =
  custom_msgs::msg::RadarScan_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__RADAR_SCAN__STRUCT_HPP_
