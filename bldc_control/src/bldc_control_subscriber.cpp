// A subscriber for  bldc_ctrl/bldc_master topic
#include "ros/ros.h"
#include "std_msgs/UInt16.h"
// polulu stuff
#include "maestro.h"


#define FREQ 10
#define QUEUE_SZ 10
#define BLDC_CH 11

// Maestro
Maestro maestro;
// callback for the
void bldc_ctrl_master_reciever(const std_msgs::UInt16 &msg) {
  ROS_INFO_STREAM(
    "seq: " << msg.data;
  );
  maestro.setTarget(BLDC_CH /* servo */, msg.data /* position in 0.25µs */);
}


int main(int argc, char **argv){
  // set maximum speed
  maestro.setSpeed(BLDC_CH /* servo */, 100 /* speed in 0.25µs/10ms */);
  // set maximum acceleration
  maestro.setAcceleration(BLDC_CH /* servo */, 255 /* accel in 0.25µs/10ms/80ms */);
  // init
  ros::init(argc, argv, "bldc_ctrl_slave");

  // Handler for this node in the ROS ecosystem.
  ros::NodeHandle nh;

  // create a subscriber object.
  // "turtle1/cmd_vel" : the topic to which the
  // 1000: maximum number of messsges published to the topic.
  ROS_INFO_STREAM(
    "subscriber initialized"
  );
  ros::Subscriber subscriber = nh.subscribe("bldc_control", QUEUE_SZ, &bldc_ctrl_master_reciever);
  ros::spin();
}
