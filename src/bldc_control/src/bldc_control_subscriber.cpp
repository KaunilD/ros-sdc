// A subscriber for  bldc_ctrl/bldc_master topic
#include "ros/ros.h"
#include "std_msgs/UInt16.h"
// polulu stuff
#include "maestro.h"

int check_target(int);

#define FREQ 10
#define QUEUE_SZ 10
#define BLDC_CH 0

#define THROTTLE_UNARMED 6000 // 1500*4
#define THROTTLE_ARMED 6130 // 1500*4
#define THROTTLE_MAX 8000 // 2000*4

Maestro maestro;

void bldc_ctrl_master_reciever(const std_msgs::UInt16 &msg) {
  int sane_target = check_target(msg.data);
  ROS_INFO_STREAM(
    "target: " << msg.data << ", "
    "checked_target: " << sane_target << std::endl;
  );

  maestro.setTarget(BLDC_CH, sane_target );
}

int check_target(int target) {
  if( target <= THROTTLE_UNARMED ){
    return THROTTLE_UNARMED;
  }
  if (target >= THROTTLE_MAX) {
    return THROTTLE_MAX;
  }
  return target;
}

void init_maestro(Maestro &maestro){
  maestro.setSpeed(BLDC_CH, 100);
  maestro.setAcceleration(BLDC_CH, 255);
  maestro.setTarget(BLDC_CH, 4000);
}

int main(int argc, char **argv){
  init_maestro(maestro);

  ros::init(argc, argv, "bldc_ctrl_slave");
  ros::NodeHandle nh;

  ROS_INFO_STREAM(
    "subscriber initialized"
  );
  ROS_INFO_STREAM(
    "CHANNEL: " << BLDC_CH << std::endl;
  );
  ros::Subscriber subscriber = nh.subscribe("bldc_control", QUEUE_SZ, &bldc_ctrl_master_reciever);
  ros::spin();
}
