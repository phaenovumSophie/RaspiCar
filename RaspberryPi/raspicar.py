#!/usr/bin/
"""
Main program to operate the RaspiCar.

File: raspicar.py
- Class RaspiCar
- Methods: run, start_lid, stop_lid, close

SLW 20-06-2023
"""

import time
import ydlidar_x2

import raspicar_socket
import raspicar_ioctrl
import raspicar_motors

# Buttons
BT_RED = 8
BT_YELLOW = 4
BT_GREEN = 2
BT_BLUE = 1


class RaspiCar:
    def __init__(self):
        # Operating values
        self.automode = False
        self.stop_system = False
        self.old_buttons = 0
        self.lid_is_active = False
        # IoCtrl
        self.io = raspicar_ioctrl.IoCtrl()
        self.io.clear_display()
        self.io.send_msg("RaspiCar 0.4")
        time.sleep(0.1)
        # LiDAR
        self.io.send_msg("Initiating LiDAR")
        self.lid = ydlidar_x2.YDLidarX2('/dev/serial0')
        self.lid.connect()
        time.sleep(0.1)
        # Motors
        self.io.send_msg("Starting motors")
        self.mot = raspicar_motors.Motors(self.io)
        time.sleep(0.1)
        # Socket
        self.io.send_msg("Starting socket")
        self.sck = raspicar_socket.RaspiCarSocket()
        if not self.sck.okay:
            self.stop_system = True
            self.io.set_led_red(True)
        else:
            self.sck.send_msg("RaspiCar connected")
        time.sleep(0.2)
        
        
    def run(self):
        while not self.stop_system:
            # Get input from controller
            success, buttons, x, y = self.sck.get_data()
            if not self.sck.okay:
                self.stop_system = True
                self.io.set_led_red(True)
                break
            if success:
                self.io.set_led_red(False)
                if buttons > 0 and buttons != self.old_buttons:
                    self._check_buttons(buttons)
                self.old_buttons = buttons
                if not self.automode:
                    self.mot.run(x, y)
            else:
                self.io.set_led_red(True)
            # get input from LiDAR
            if self.lid_is_active and self.lid.available:
                sectors = self.lid.get_sectors40()
                print(sectors[18 : 23])
                
            time.sleep(0.1)
                    
                
    def _check_buttons(self, buttons):
        if buttons == (BT_BLUE | BT_GREEN) or self.io.shutdown:
            self.stop_system = True
        elif buttons == BT_RED:
            if self.lid_is_active:
                self.stop_lid()
            else:
                self.start_lid()
                
                
    def start_lid(self):
        self.sck.send_msg("Starting LiDAR")
        self.io.set_lidar_pwr(True)
        time.sleep(0.2)
        self.lid.start_scan()
        time.sleep(0.5)
        self.lid_is_active = True
        

    def stop_lid(self):
        self.lid_is_active = False
        #self.socket_send_msg("Stopping LiDAR")
        self.lid.stop_scan()
        time.sleep(0.3)
        self.io.set_lidar_pwr(False)
        time.sleep(0.3)
        
        
    def close(self):
        # self.socket_send_msg("Stopping system")
        self.io.send_msg("Stopping motors")
        self.mot.stop()
        time.sleep(0.1)
        if self.lid_is_active:
            self.io.send_msg("Stopping LiDAR")
            self.stop_lid()
        self.io.send_msg("Closing io_ctrl")
        self.io.close()
        if self.sck.okay:
            stats_data = self.sck.get_stats()
            self.sck.send_msg("Connection Stats")
            time.sleep(0.3)
            self.sck.send_msg("Cnt: {:d} ({:d})".format(stats_data[0], stats_data[1]))
            time.sleep(0.5)
            msg = "Latency: {:d}-{:d}-{:d}".format(round(stats_data[2]), round(stats_data[3]), round(stats_data[4]))                                                     
            self.sck.send_msg(msg)
        time.sleep(0.2)
        self.sck.send_msg("Connection closed")
        self.sck.close()
        time.sleep(0.1)
        
#--------------------------------------------------------------------------------------------------
        
rc = RaspiCar()

try:
    rc.run()
except KeyboardInterrupt:
    pass

stats = rc.sck.get_stats()
rc.close()

print("Latency:")
print("  Count:  {:d} (lost: {:d})".format(stats[0], stats[1]))
print("  Timing: {:.1f} - {:.1f} - {:.1f} ms".format(stats[2], stats[3], stats[4]))
print()
print("Done")
