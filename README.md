# RaspiCar
A model car equipped with a Raspberry Pi, intended for experimenting with tools and algorithms for autonomous navigation

This is a simple platform for experimenting. At this stage clearly work in progress ...

The car is based on two stepper motors for the left and right driving wheel. In addition there is a free spinning wheel in the front. Driving direction is controlled by different speed settings for the motors. The car is capable of turning on the spot. Power is provided a by a LiPo battery of 3 cells.

Raspberry Pi:
=============
The Raspberry Pi provides navigation and overall management of the car. The navigations is based on the various sensors. The software is written primarily in Python. Prototype software is avaiable to support ultrasonic sensors, LiDAR, camera and a NRF24 module for remote control. There are also experiments with machine learning alogrithms (SciKit Learn). More to be developed and to follow.

Python files:
- io_ctrl.py - This module defines the I/Os for the Raspberry Pi and a tool to send commands to the motor driver via a serial interface
- much more to come ...

Motor Driver:
=============
In addition to the Raspberry Pi, there is a board comprising a 5V step down converter, a rp2040 microcontroller, a LCD and adapters for various devices such as LiDAR, distance sensors and more. The rp2040 generates the step and direction signals for the stepper motors, with this releasing the real time workload from the Raspberry Pi. The rp2040 interfaces with the Raspberry Pi via a serial interface running at115200 baud. The rp2040 also takes care of power management by raising a shutdown signal in case the battery voltage is running low. The software for the rp2040 is based on Arduino/C++

Arduino files for the motor driver:
- rp2040_motor_driver.ino: main program
- motors.cpp, motors.h: class to run the stepper motors
- display.cpp, display.h: class to run the display
- battery.cpp, battery.h: class to provide battery and power management

List of motor commands:
The Raspberry Pi sends commands via the serial interface and receives responses. This can easily by tested with a standard terminal tool (e.g. PUTTY).
- ME0,0 / ME1,1  - disables or enables motor A and B
- MP0,0 / MP1,1  - switches motor A and B on or off
- MD0,0 / MD1,1  - sets the direction of the motor (1 -> forward, 0 -> backward)
- MR200,300 - sets the speed of the motors in rounds per minute. The range is 0 to 1500.
- DC - clears the display
- DT - prints a title of up to 0 characters on line 1 of the display (maximum 20 characters)
- DM - prints a message of up to 40 character on line 2 and 3 of the display
- BV - returns the current battery voltage
- BS - returns the battery voltage and the system status, separated by comma 

List of system status:
- OK - (0)
- BL - (1) Battery Low - battery below 10.5V
- BS - (2) Battery shutdown - battery below 9.5V. The system should shutdown immediately
- SR - (3) shutdown requested by the user
- SX - (4) shutdown active. The rp2040 will power off the entire system within 10 seconds


SLW October 2022
