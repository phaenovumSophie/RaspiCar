import io_ctrl
import time

class Motors:
    
    def __init__(self, io):
        self._io = io
        self.dir_a, self.dir_b = True, True
        self._io.send_ser("MR0,0")
        self._io.send_ser("MP1,1")
        self._mot_a, self._mot_b = 0, 0
        self._stand_still = False
        self._mot_power_on = True
        self._cutoff = 30
        self._mot_stop_cnt = 0
        self._system_end_cnt = 0
        self._system_shutdown_cnt = 0
        self._system_wait = 30
        self._old_buttons = 0

    def run(self, x, y):
        x -= 510
        y -= 490
        if x > self._cutoff:
            x -= self._cutoff
        elif x < -self._cutoff:
            x += self._cutoff
        else:
            x = 0
        if y > self._cutoff:
            y -= self._cutoff
        elif y < -self._cutoff:
            y += self._cutoff
        else:
            y = 0
        y = int(-2.5*y)
        dir_a, dir_b = self.dir_a, self.dir_b
        self._mot_a, self._mot_b = y-x, y+x
        if self._mot_a < 0:
            dir_a = False
            self._mot_a = -self._mot_a
        else:
            dir_a = True
        if self._mot_b < 0:
            dir_b = False
            self._mot_b = -self._mot_b
        else:
            dir_b = True
        if (dir_a != self.dir_a) or (dir_b != self.dir_b):
            self._io.send_ser("MD{:d},{:d}".format(1 if dir_a else 0, 1 if dir_b else 0))
            self.dir_a = dir_a
            self.dir_b = dir_b
        if self._mot_a > 0 or self._mot_b > 0:
            s = "MR" + str(self._mot_a) + "," + str(self._mot_b)
            self._io.send_ser(s)
            self._stand_still = False
        else:
            if not self._stand_still:
                self._io.send_ser("MR0,0")
                self._stand_still = True
        
    def check_buttons(self, buttons):
        if buttons != self._old_buttons:            
            if self._system_end_cnt > 0:
                self._io.send_ser("DMProgEnd cancelled")
                self._system_end_cnt = 0
            if self._system_shutdown_cnt > 0:
                self._io.send_ser("DMShutdown cancelled")
                self._system_shutdown_cnt = 0
            self._mot_stop_cnt = 0
        if buttons == 10:    # blue + red
            if self._system_end_cnt == 0:
                self._io.send_ser("DMProgEnd pressed")
            self._system_end_cnt += 1
        if buttons == 14:    # blue + yellow + red    
            if self._system_shutdown_cnt == 0:
                self._io.send_ser("DMShutdown pressed")
            self._system_shutdown_cnt += 1
        if buttons == 4:    # yellow
            self._mot_stop_cnt += 1
            if self._mot_stop_cnt == 10:
                if self._mot_power_on:
                    self._io.send_ser("MP0,0")
                    self._mot_power_on = False
                else:
                    self._io.send_ser("MP1,1")
                    self._mot_power_on = True
        self._old_buttons = buttons
            
        if self._system_shutdown_cnt >= self._system_wait:
            return "shutdown"
        elif self._system_end_cnt >= self._system_wait:
            return "progend"
        else:
            return "OK"
        
# main =================================================
if __name__ == "__main__":
    print("Starting io_ctrl ...")
    io = io_ctrl.IoCtrl()
    time.sleep(1)
    print("Starting motors ...")
    mot = Motors(io)
    time.sleep(1)
    print("Stopping motors ...")
    io.send_ser("MP0,0")
    time.sleep(1)
    print("Closing interface ...")
    io.close()
    
            