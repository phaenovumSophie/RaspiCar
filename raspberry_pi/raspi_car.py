import io_ctrl
import time

step_speed = 0.05

io = io_ctrl.IoCtrl()

io.send_ser("DMForward ...")
io.send_ser("MD0,0")
io.send_ser("MP1,1")
for i in range(50):
    io.send_ser(f"MR{i*20:d},{i*20:d}")
    time.sleep(step_speed)
time.sleep(1)
for i in range(49, -1, -1):
    io.send_ser(f"MR{i*20:d},{i*20:d}")
    time.sleep(step_speed)
time.sleep(1)

io.send_ser("DMBackward ...")
io.send_ser("MD1,1")
for i in range(50):
    io.send_ser(f"MR{i*20:d},{i*20:d}")
    time.sleep(step_speed)
time.sleep(1)
for i in range(49, -1, -1):
    io.send_ser(f"MR{i*20:d},{i*20:d}")
    time.sleep(step_speed)
    
io.send_ser("MP0,0")
io.send_ser("DMDone")



