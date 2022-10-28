""" io_ctrl.py - pin and I/O definitions for the RaspiCar
    SLW 27-09-2021
"""

import time
import pigpio
import serial
import threading
import os

class IoCtrl:
       
    def __init__(self):
        # pin definitions
        _PIN_LED_RED = 6
        _PIN_LED_GREEN = 13
        _PIN_LIDAR_PWR = 4
        _serial_port = "/dev/ttyUSB0"
        # initiate ports
        self.pin_led_green, self.pin_led_red = _PIN_LED_GREEN, _PIN_LED_RED
        self.pin_lidar_pwr = _PIN_LIDAR_PWR
        # initiate operating data
        self._ser_busy = False
        self._shutdown = False
        self._status = "OK"
        # connecting serial interface        
        hostname, port = 'localhost', 8888
        self.pi = pigpio.pi(hostname, port)
        if not self.pi.connected:
            raise Exception("Error! Not connected to Raspberry Pi ... goodbye")
        else:
            # set port mode
            self.pi.set_mode(self.pin_led_green, pigpio.OUTPUT)
            self.pi.set_mode(self.pin_led_red, pigpio.OUTPUT)
            self.pi.set_mode(self.pin_lidar_pwr, pigpio.OUTPUT)
            # set initial values
            self.pi.write(self.pin_lidar_pwr, 0)
            self.pi.write(self.pin_led_green, 0)
            self.pi.write(self.pin_led_red, 0)
            print("GPIO ports initialized")
        # initiate serial interface
        connection_cnt = 0
        connected = False
        while not connected and connection_cnt < 5:
            try:
                self._ser = serial.Serial(_serial_port, baudrate=115200,
                                      parity=serial.PARITY_NONE, timeout=1)
                connected = True
            except:
                print("Failed to open serial port", conenction_cnt)
                time.sleep(2)
                print("Trying again")
                connection_cnt += 1

        if self._ser.isOpen() == False:
            raise Exception("Error! Can't open serial port " + _serial_port)
        print("Serial port '" + _serial_port + "' opened")
        time.sleep(0.5)
        self.send_ser(" ");
        time.sleep(0.5)
        self.send_ser("DTRaspi connected")
        # starting thread
        self._t = threading.Thread(target = self._read_status)
        self._t.start()       
        
    def _read_status(self):
        while not self._shutdown:
            while self._ser_busy:
                time.sleep(0.01)
            self._status = self.send_ser("BS")[-2:]
            if self._status == "SR":
                print("Stopping motors ...")
                self.send_ser("MR0,0")
                time.sleep(0.1)
                self.send_ser("MP0,0")
                time.sleep(0.1)
                print("Shutting down")
                print(self.send_ser("BX"))
                time.sleep(0.1)
                result = os.popen("sudo shutdown -h now").read()
                
            time.sleep(1)
        print("Thread stopped ...")
                                
    def get_status(self):
        return self._status
    
    def set_lidar_pwr(self, pwr):
        if pwr:
            self.pi.write(self.pin_lidar_pwr, 1)
        else:
            self.pi.write(self.pin_lidar_pwr, 0)
            
    def set_led_red(self, status):
        if status:
            self.pi.write(self.pin_led_red, 1)
        else:
            self.pi.write(self.pin_led_red, 0)
                    
    def set_led_green(self, status):
        if status:
            self.pi.write(self.pin_led_green, 1)
        else:
            self.pi.write(self.pin_led_green, 0)

    def send_ser(self, msg, ser_delay=0.01):
        while self._ser_busy == True:
            time.sleep(0.01)
        self._ser_busy = True
        self._ser.write((msg + '\n').encode("UTF-8"))
        time.sleep(ser_delay)
        response = self._ser.readline()
        self._ser_busy = False
        return response[:-2].decode("UTF-8")
        
    def get_pi(self):
        return self.pi
    
    def close(self):
        self._ser.close()
        self._shutdown = True
        print("Serial interface closed ...")

#------------------------------------------------
if __name__ == "__main__":
    io = IoCtrl()
    io.set_led_red(True)
    time.sleep(0.5)
    io.set_led_red(False)
    io.set_led_green(True)
    time.sleep(0.5)
    io.set_led_green(False)
    