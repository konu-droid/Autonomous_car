// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_msgs:msg/RadarScan.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__RADAR_SCAN__TRAITS_HPP_
#define CUSTOM_MSGS__MSG__RADAR_SCAN__TRAITS_HPP_

#include "custom_msgs/msg/radar_scan__struct.hpp"
#include <rosidl_generator_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/header__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<custom_msgs::msg::RadarScan>()
{
  return "custom_msgs::msg::RadarScan";
}

template<>
struct has_fixed_size<custom_msgs::msg::RadarScan>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<custom_msgs::msg::RadarScan>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<custom_msgs::msg::RadarScan>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_MSGS__MSG__RADAR_SCAN__TRAITS_HPP_
