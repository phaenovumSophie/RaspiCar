""" io_ctrl.py - pin and I/O definitions for the RaspiCar
    SLW 27-09-2021
"""

import time
import pigpio
import serial

class PinCtrl:
    
    
    def __init__(self):
        # pin definitions
        _PIN_LED_RED = 6
        _PIN_LED_GREEN = 13
        _PIN_LIDAR_PWR = 4
        _serial_port = "/dev/ttyUSB0"

        self.pin_led_green, self.pin_led_red = _PIN_LED_GREEN, _PIN_LED_RED
        self.pin_lidar_pwr = _PIN_LIDAR_PWR
        
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
            
        self.ser = serial.Serial(_serial_port, baudrate=115200,
                                 parity=serial.PARITY_NONE, timeout=1)
        if self.ser.isOpen() == False:
            raise Exception("Error! Can't open serial port " + _serial_port)
        print("Serial port '" + _serial_port + "' opened")
        time.sleep(0.5)
        self.send_ser(" ");
        time.sleep(0.5)
        self.send_ser("DTRaspi connected")
        
                    
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
        self.ser.write((msg + '\n').encode("UTF-8"))
        time.sleep(ser_delay)
        response = self.ser.readline()
        return response[:-2].decode("UTF-8")
        
        
    def get_pi(self):
        return self.pi
    
    
    def close(self):
        self.ser.close()
        print("Serial interface closed")

#------------------------------------------------
if __name__ == "__main__":
    io = PinCtrl()
    io.set_led_red(True)
    time.sleep(0.5)
    io.set_led_red(False)
    io.set_led_green(True)
    time.sleep(0.5)
    io.set_led_green(False)
    
    