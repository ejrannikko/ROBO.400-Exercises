/*This is code includes a single node that subscribes to the left and right contact sensor topics.
  A log is printed to the terminal when the subscriber detects contanct from the topic.
  Every 100 ms, a function checks if both contacts are detected. If so, publish a angle position command for robot arm 2*/

#include <chrono>
#include <memory>
#include <functional>

#include "rclcpp/rclcpp.hpp"
#include "ros_gz_interfaces/msg/contacts.hpp"
#include "std_msgs/msg/float64.hpp"

using namespace std::chrono_literals;

class ContactSubscriber : public rclcpp::Node
{
public:
    ContactSubscriber()
    : Node("contact_subscriber")
    {
        L_contact_subs_ = this->create_subscription<ros_gz_interfaces::msg::Contacts>(
            L_contact_topic_, 10, std::bind(&ContactSubscriber::L_contact_callback, this, std::placeholders::_1)
        );
        R_contact_subs_ = this->create_subscription<ros_gz_interfaces::msg::Contacts>(
            R_contact_topic_, 10, std::bind(&ContactSubscriber::R_contact_callback, this, std::placeholders::_1)
        );
        both_contact_timer_ = this->create_wall_timer(100ms, std::bind(&ContactSubscriber::both_contact, this));
        joint_publisher_ = this->create_publisher<std_msgs::msg::Float64>(rev_joint_topic_, 10);
    }

private:
    void L_contact_callback(const ros_gz_interfaces::msg::Contacts::SharedPtr msg)
    {
        (void)msg;
        RCLCPP_INFO(this->get_logger(), "L contact!");
        L_contact_ = true;
    }
    void R_contact_callback(const ros_gz_interfaces::msg::Contacts::SharedPtr msg)
    {
        (void)msg;
        RCLCPP_INFO(this->get_logger(), "R contact!");
        R_contact_ = true;
    }
    void both_contact()
    {
        if (L_contact_ & R_contact_)
        {
            RCLCPP_INFO(this->get_logger(), "Both contact!");
            auto message = std_msgs::msg::Float64();
            message.data = joint_pos_data_;
            joint_publisher_->publish(message);
            L_contact_ = false;
            R_contact_ = false;
        }
    }
    rclcpp::Subscription<ros_gz_interfaces::msg::Contacts>::SharedPtr L_contact_subs_;
    rclcpp::Subscription<ros_gz_interfaces::msg::Contacts>::SharedPtr R_contact_subs_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr joint_publisher_;
    rclcpp::TimerBase::SharedPtr both_contact_timer_;
    bool L_contact_;
    bool R_contact_;
    const std::string L_contact_topic_ = "/world/gripper_world/model/gripper/link/L_grip/sensor/L_contact_sensor/contact";
    const std::string R_contact_topic_ = "/world/gripper_world/model/gripper/link/R_grip/sensor/R_contact_sensor/contact";
    const std::string rev_joint_topic_ = "/rotate_arm_2_cmd_pos"; 
    const float joint_pos_data_ = 1.57;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ContactSubscriber>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
