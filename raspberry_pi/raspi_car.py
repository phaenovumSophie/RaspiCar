#!/usr/bin/env python3

import io_ctrl
import motor_ctrl
import nrf_rxtx
import time
import os

step_speed = 0.05
system_end_cnt = 0
system_shutdown_cnt = 0
system_wait = 30
old_buttons = 0
old_nrf_failure = False
motor_power = False


# main program starts here =======================================

print("Program start ...")
time.sleep(1)
print("Starting interface ...")
io = io_ctrl.IoCtrl()
time.sleep(1)
print("Starting NRF24 ...")
nrf = nrf_rxtx.NRF(io)
time.sleep(1)
print("Starting motors ...")
mots = motor_ctrl.Motors(io)
motor_power = True
time.sleep(1)
system_status = "OK"
print("System running ...")

io.send_ser("DTRaspiCar v0.2")
io.send_ser("DMokay")

while system_status == "OK":
    nrf.send_nrf("GD")
    time.sleep(0.01)
    cnt = 0
    timeout = time.time() + 0.1
    nrf_failure = False
    while not nrf.data_ready():
        if time.time() > timeout:
            
            nrf_failure = True
            break
    if not nrf_failure:
        adcx, adcy, buttons = nrf.read_nrf()
        mots.run(adcx, adcy)
        if old_nrf_failure:
            io.set_led_red(False)
            old_nrf_failure = False
            if not motor_power:
                io.send_ser("MP1,1")
                motor_power = True
        system_status = mots.check_buttons(buttons)
    else:
        if not old_nrf_failure:
            io.set_led_red(True)
            print("NRF read failure")
            old_nrf_failure = True
        io.send_ser("MP0,0")
        motor_power = False
    # check buttons
    
  
    time.sleep(0.05)

io.send_ser("MP0,0")
io.send_ser("DMDone")
io.set_led_green(False)
io.set_led_red(False)
io.send_ser("DMProgram ended")
io.send_ser("DT ")

time.sleep(1)

if system_status == "shutdown":
    io.send_ser("DMShutting  down")
    io.send_ser("BX")
    io.close()
    time.sleep(1)
    result = os.popen("sudo shutdown -h now").read()
else:
    io.close()
    print("Program ended")
