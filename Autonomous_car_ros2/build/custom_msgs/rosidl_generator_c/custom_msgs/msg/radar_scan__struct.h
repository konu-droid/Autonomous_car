// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msgs:msg/RadarScan.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__RADAR_SCAN__STRUCT_H_
#define CUSTOM_MSGS__MSG__RADAR_SCAN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/header__struct.h"

// Struct defined in msg/RadarScan in the package custom_msgs.
typedef struct custom_msgs__msg__RadarScan
{
  std_msgs__msg__Header header;
  uint16_t point_id;
  float x;
  float y;
  float z;
  float range;
  float velocity;
  uint16_t doppler_bin;
  float bearing;
  float intensity;
} custom_msgs__msg__RadarScan;

// Struct for a sequence of custom_msgs__msg__RadarScan.
typedef struct custom_msgs__msg__RadarScan__Sequence
{
  custom_msgs__msg__RadarScan * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msgs__msg__RadarScan__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSGS__MSG__RADAR_SCAN__STRUCT_H_
