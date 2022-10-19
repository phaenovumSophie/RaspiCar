# RaspiCar
A model car equipped with a Raspberry Pi, intended for experimenting with tools and algorithms for autonomous navigation

This is a simple platform for experimenting, at this stage clearly work in progress.

The car is based on two stepper motors for the left and right driving wheel. In addition there is a free spinning wheel in the front. Driving direction is controlled by different speed settings for the motors. The car is capable of turning on the spot.

Power is provided a by a LiPo battery of 3 cells.

In addition to the Raspberry Pi, there is a board comprising a 5V step down converter, a rp2040 microcontroller, a LCD and adapters for various devices such as LiDAR, distance sensors and more. The rp2040 generates the step and direction signals for the stepper motors, with this releasing the real time workload from the Raspberry Pi. The rp2040 interfaces with the Raspberry Pi via a serial interface running at115200 baud. 
The rp2040 also takes care of power management by raising a shutdown signal in case the battery voltage is running low.
Navigation and overall direction is provided by the Raspberry Pi based on the various sensors (to be developed). 
The current status of the project is “early development”. Many of the details are not fully working at this stage.

SLW October 2022
