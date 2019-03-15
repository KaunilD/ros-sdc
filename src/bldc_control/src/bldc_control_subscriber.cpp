// A subscriber for  bldc_ctrl/bldc_master topic
#include "ros/ros.h"
#include "std_msgs/UInt16.h"
#include "geometry_msgs/Twist.h"
// polulu stuff
#include "maestro.h"

int get_pwm(float);

#define FREQ 10
#define QUEUE_SZ 10
#define BLDC_CH 6

#define THROTTLE_UNARMED 6000 // 1500*4
#define THROTTLE_ARMED 6130 // 1500*4
#define THROTTLE_MAX 8000 // 2000*4

Maestro maestro;

// linear.x = (0, 10)
// angular.x = (0, 10)
void bldc_ctrl_master_reciever(const geometry_msgs::Twist &msg) {
  int pulse_width = get_pwm(msg.linear.x);
  ROS_INFO_STREAM(
    "target: " << msg.linear.x*800 << ", "
    "checked_target: " << pulse_width << std::endl;
  );

  maestro.setTarget(BLDC_CH, pulse_width );
}

int get_pwm(float level) {
  return (int)(THROTTLE_ARMED + level*200);
}

void init_maestro(Maestro &maestro){
  maestro.setSpeed(BLDC_CH, 100);
  maestro.setAcceleration(BLDC_CH, 255);
  maestro.setTarget(BLDC_CH, THROTTLE_UNARMED);
}

int main(int argc, char **argv){
  init_maestro(maestro);

  ros::init(argc, argv, "bldc_motor");
  ros::NodeHandle nh;

  ROS_INFO_STREAM(
    "subscriber initialized"
  );
  ROS_INFO_STREAM(
    "CHANNEL: " << BLDC_CH << std::endl;
  );
  ros::Subscriber subscriber = nh.subscribe("cmd_vel", QUEUE_SZ, &bldc_ctrl_master_reciever);
  ros::spin();
}
