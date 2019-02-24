// A publisher that connects with the bldc_control/bldc_control topic
// and sends out motor RPM signals.

#include "ros/ros.h"
#include "std_msgs/UInt16.h"
#include <sstream>
#include <stdlib.h>

#define FREQ 10
#define QUEUE_SZ 10

std::string TAG = "BLDC_CTRL_PUB";

int main(int argc, char **argv){
  // init
  ros::init(argc, argv, "bldc_master");

  // Handler for this node in the ROS ecosystem.
  ros::NodeHandle nh;

  ros::Publisher publisher = nh.advertise<std_msgs::UInt16>(
    "bldc_control",
    QUEUE_SZ
  );

  // counter for the number of messages published till date.
  int pulse_width = 0;
  while(std::cin >> pulse_width){
    if(ros::ok()) {
      // initialize the message packet.
      std_msgs::UInt16 msg;
      msg.data = pulse_width;
      ROS_INFO  ("%s: %d", TAG.c_str() , pulse_width);
      publisher.publish(msg);
    }
  }
  return 0;
}
