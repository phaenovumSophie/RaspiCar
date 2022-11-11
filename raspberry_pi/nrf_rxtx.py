import time
import nrf24
import io_ctrl

class NRF:
    
    def __init__(self, io):
        self._io = io
        self._read_pipe = "RASrx"    # Raspberry receiver (max 6 chars)
        self._write_pipe = "RAStx"   # Raspberry tramsitter (max 6 chars)
        self._nrf = self._setup()
        self._nrf.open_writing_pipe(self._write_pipe)
        self._nrf.open_reading_pipe(nrf24.RF24_RX_ADDR.P1, self._read_pipe)
        self._io.send_ser("DMRF24 connected")
        
    def _setup(self):
        nrf = nrf24.NRF24(self._io.get_pi(),
                          ce           = 22,
                          crc_bytes    = nrf24.RF24_CRC.BYTES_2,
                          payload_size = nrf24.RF24_PAYLOAD.DYNAMIC,
                          channel      = 75,
                          data_rate    = nrf24.RF24_DATA_RATE.RATE_1MBPS,
                          pa_level     = nrf24.RF24_PA.MIN)
        # nrf.show_registers()
        return nrf
    
    def send_nrf(self, msg):
        """ Sends a message via NRF24.Changes the LED to red while sending.
            Returns the number of packages lost:
               -1 -> timeout error
                0 -> okay
                >0 -> number of packages lost """
        self._nrf.send(msg)
        timeout, failure = time.time() + 0.2, False
        while self._nrf.is_sending():
            if time.time() > timeout:
                failure = True
                packages_lost = -1
                break
            time.sleep(0.001)
        if not failure:
            packages_lost = self._nrf.get_packages_lost()
            if packages_lost != 0:
                self._nrf.reset_packages_lost()
                self._io.set_led_red(True)
            else:
                self._io.set_led_red(False)
        else:
            self._io.set_led_red(True)
        return packages_lost
    
    
    def data_ready(self):
        return self._nrf.data_ready()
        
        
    def read_nrf(self):
        payload = [byte & 0xff for byte in self._nrf.get_payload()]
        payload_len = len(payload)
        if payload_len == 5:
            adcx = int(payload[0]) + int(payload[1])*256
            adcy = int(payload[2]) + int(payload[3])*256
        else:
            adcx, adcy = -1, -1
        return adcx, adcy, payload[4]    
        
                
        
        
#----------------------------------------------------------------
if __name__ == "__main__":
    io = io_ctrl.IoCtrl()
    my_nrf = NRF(io)
    
    
                          