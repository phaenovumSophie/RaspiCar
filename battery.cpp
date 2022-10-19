#include "battery.h"

struct repeating_timer bat_voltage_timer;

//-------------------------------------------------------------------------
void Battery::init(void) {
  pinMode(ADC_BATTERY_GPIO, INPUT);
  pinMode(LED_BAT_LOW, OUTPUT);
  digitalWrite(LED_BAT_LOW, LOW);

  add_repeating_timer_us(-10000, bat_voltage_timer_callback, NULL, &bat_voltage_timer); 
}

//-------------------------------------------------------------------------
// Retrieves and sums up the adc value.
// After every 16th call, returns true (to initiate display refresh), otherwise false
bool Battery::run_adc(void) {
  adc_sum += analogRead(ADC_BATTERY);
  cnt_adc += 1;
  if (cnt_adc > 16) {
    cnt_adc = 0;
    voltage = (uint16_t) (100*(adc_sum * ADC_REF * BATTERY_DIVIDER / (ADC_RANGE * 16) + BATTERY_TL431_OFFSET));
    if (voltage < 900) voltage = 0;
    adc_sum = 0;
    cnt_show += 1;    
    if (status < 3) {
      if (voltage > BAT_LOW) status = 0;
      else if (voltage > BAT_SHUTDOWN) status = 1;
      else status = 2;
    }
  }
  if (cnt_show >= 16) {
    cnt_show = 0;
    return true;
  } else {
    return false;
  }
}

//-------------------------------------------------------------------------
void Battery::get_full_status(char buf[]) {

  itoaf(voltage, buf, 4, 2, false);
  switch (status) {
    case STATUS_OK: 
      strcat(buf, ",OK");
      break;
    case STATUS_BAT_LOW: 
      strcat(buf, ",BL");
      break;
    case STATUS_BAT_SHUTDOWN: 
      strcat(buf, ",SB");
      break;
    case STATUS_SHUTDOWN_REQUESTED: 
      strcat(buf, ",SR");
      break;
    case STATUS_SHUTDOWN_ACTIVE:
      strcat(buf, ",SX");
  } 
}

//-------------------------------------------------------------------------
uint8_t Battery::get_status(void) {

  return status;
}

//-------------------------------------------------------------------------
int16_t Battery::get_voltage(void) {
  return voltage;
}

//-------------------------------------------------------------------------
void Battery::request_shutdown(void) {
  status = 3;
}

//-------------------------------------------------------------------------
void Battery::start_shutdown(void) {
  status = 4;
}

//-------------------------------------------------------------------
bool bat_voltage_timer_callback(struct repeating_timer *t) {
  extern volatile uint8_t job_flags;
  job_flags |= (1 << JF_REFRESH_BAT_VOLTAGE);
  return true;
}
