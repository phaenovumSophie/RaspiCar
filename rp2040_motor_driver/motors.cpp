#include "motors.h"

struct repeating_timer mot_a_timer;
struct repeating_timer mot_b_timer;

//----------------------------------------------------------------------
void Motors::init(void) {
  pinMode(MOTA_PWR, OUTPUT);
  digitalWrite(MOTA_PWR, HIGH);
  pinMode(MOTA_STEP, OUTPUT);
  digitalWrite(MOTA_STEP, HIGH);
  pinMode(MOTA_DIR, OUTPUT);
  digitalWrite(MOTA_DIR, HIGH);
  pinMode(MOTB_PWR, OUTPUT);
  digitalWrite(MOTB_PWR, HIGH);
  pinMode(MOTB_STEP, OUTPUT);
  digitalWrite(MOTB_STEP, HIGH);
  pinMode(MOTB_DIR, OUTPUT);
  digitalWrite(MOTB_DIR, HIGH);
  
  add_repeating_timer_us(a_step_time, mot_a_timer_callback, NULL, &mot_a_timer);
  add_repeating_timer_us(b_step_time, mot_b_timer_callback, NULL, &mot_b_timer);
}

//----------------------------------------------------------------------
void Motors::set_a_enable(bool status) {
  a_enabled = status;
}

//----------------------------------------------------------------------
void Motors::set_b_enable(bool status) {
  b_enabled = status;
}

//----------------------------------------------------------------------
void Motors::set_a_power(bool status) {
  a_power = status;
  digitalWrite(MOTA_PWR, !status);
}

//----------------------------------------------------------------------
void Motors::set_b_power(bool status) {
  b_power = status;
  digitalWrite(MOTB_PWR, !status);
}

//----------------------------------------------------------------------
bool Motors::get_a_enabled(void) {
  return a_enabled;
}

//----------------------------------------------------------------------
bool Motors::get_b_enabled(void) {
  return b_enabled;
}

//----------------------------------------------------------------------
bool Motors::get_a_power(void) {
  return a_power;
}

//----------------------------------------------------------------------
bool Motors::get_b_power(void) {
  return b_power;
}

//----------------------------------------------------------------------
void Motors::set_a_dir(bool status) {
  a_dir = status;
  digitalWrite(MOTA_DIR, status);
}

//----------------------------------------------------------------------
void Motors::set_b_dir(bool status) {
  b_dir = status;
  digitalWrite(MOTB_DIR, status);
}

//----------------------------------------------------------------------
void Motors::check_step_time_a(void) {
  if (a_step_time_target < a_step_time) {   // faster
    a_step_time = calc_step_time(a_rpm, a_step_time, MOT_RAMP, true);
    if (a_step_time < a_step_time_target) a_step_time = a_step_time_target;
    a_rpm = CONVERSION_FACTOR / a_step_time;
    mot_a_timer.delay_us = a_step_time;
  } else if (a_step_time_target > a_step_time) {   // slower
    a_step_time = calc_step_time(a_rpm, a_step_time, MOT_RAMP, false);
    if (a_step_time > a_step_time_target) a_step_time = a_step_time_target;
    a_rpm = CONVERSION_FACTOR / a_step_time;
    mot_a_timer.delay_us = a_step_time;
  }
}

//----------------------------------------------------------------------
void Motors::check_step_time_b(void) {
  if (b_step_time_target < b_step_time) {
    b_step_time = calc_step_time(b_rpm, b_step_time, MOT_RAMP, true);
    if (b_step_time < b_step_time_target) b_step_time = b_step_time_target;
    b_rpm = CONVERSION_FACTOR / b_step_time;
    mot_b_timer.delay_us = b_step_time;
  } else if (b_step_time_target > b_step_time) {
    b_step_time = calc_step_time(b_rpm, b_step_time, MOT_RAMP, false);
    if (b_step_time > b_step_time_target) b_step_time = b_step_time_target;
    b_rpm = CONVERSION_FACTOR / b_step_time;
    mot_b_timer.delay_us = b_step_time;
  }
}

//-------------------------------------------------------------------------
uint32_t Motors::calc_step_time(uint32_t rpm, uint32_t old_step_time, uint16_t step_width, bool up) {
  uint32_t new_step_time;
  int new_rpm;
  
  if (up) {
    new_rpm = rpm + step_width;
    if (new_rpm > RPM_MAX) new_rpm = RPM_MAX;
    new_step_time = CONVERSION_FACTOR / new_rpm;
    if (new_step_time >= old_step_time) new_step_time = old_step_time - 1;  
  } else {
    new_rpm = rpm - step_width;
    if (new_rpm < RPM_MIN) new_rpm = RPM_MIN;
    new_step_time = CONVERSION_FACTOR / new_rpm;
    if (new_step_time <= old_step_time) new_step_time = old_step_time + 1;  
  }
  return new_step_time;
}

//-------------------------------------------------------------------
void Motors::set_a_steptime(uint32_t steptime) {
  a_step_time_target = steptime;
  if (a_step_time_target < MOT_STEP_TIME_MIN)
   a_step_time_target = MOT_STEP_TIME_MIN;
  else if (a_step_time_target > MOT_STEP_TIME_MAX)
   a_step_time_target = MOT_STEP_TIME_MAX;
}

//-------------------------------------------------------------------
void Motors::set_b_steptime(uint32_t steptime) {
  b_step_time_target = steptime;
  if (b_step_time_target < MOT_STEP_TIME_MIN)
    b_step_time_target = MOT_STEP_TIME_MIN;
  else if (b_step_time_target > MOT_STEP_TIME_MAX)
    b_step_time_target = MOT_STEP_TIME_MAX;
}

//-------------------------------------------------------------------
void Motors::set_a_rpm(uint32_t rpm) {
  if (rpm == 0) {
    a_step_time_target = MOT_STEP_TIME_MAX;
    a_enabled = false;
  } else {
    if (rpm > RPM_MAX) rpm = RPM_MAX;
    a_step_time_target = CONVERSION_FACTOR / rpm;
    if (a_step_time_target < MOT_STEP_TIME_MIN)
      a_step_time_target = MOT_STEP_TIME_MIN;
    else if (a_step_time_target > MOT_STEP_TIME_MAX)
      a_step_time_target = MOT_STEP_TIME_MAX;
    a_enabled = true;
    set_a_power(true);
  }
  a_rpm = rpm;
}

//-------------------------------------------------------------------
void Motors::set_b_rpm(uint32_t rpm) {
  if (rpm == 0) {
    b_step_time_target = MOT_STEP_TIME_MAX;
    b_enabled = false;
  } else {
    if (rpm > RPM_MAX) rpm = RPM_MAX;
    b_step_time_target = CONVERSION_FACTOR / rpm;
    if (b_step_time_target < MOT_STEP_TIME_MIN)
      b_step_time_target = MOT_STEP_TIME_MIN;
    else if (b_step_time_target > MOT_STEP_TIME_MAX)
      b_step_time_target = MOT_STEP_TIME_MAX;
    b_enabled = true;
    set_b_power(true);
  }
  b_rpm =rpm;  
}

//-------------------------------------------------------------------
uint32_t Motors::get_a_rpm(void) {
  if (a_step_time_target >= MOT_STEP_TIME_MAX) return 0; 
  return CONVERSION_FACTOR / a_step_time_target;
}

//-------------------------------------------------------------------
uint32_t Motors::get_b_rpm(void) {
  if (b_step_time_target >= MOT_STEP_TIME_MAX) return 0; 
  return CONVERSION_FACTOR / b_step_time_target;
}

//-------------------------------------------------------------------
bool mot_a_timer_callback(struct repeating_timer *t) {
  extern Motors motors;
  if (motors.a_enabled) {
    if (digitalRead(MOTA_STEP) == HIGH)
      digitalWrite(MOTA_STEP, LOW);
    else
      digitalWrite(MOTA_STEP, HIGH);
  }
  return true;
}

//-------------------------------------------------------------------
bool mot_b_timer_callback(struct repeating_timer *t) {
  extern Motors motors;
  if (motors.b_enabled) {
    if (digitalRead(MOTB_STEP) == HIGH)
      digitalWrite(MOTB_STEP, LOW);
    else
      digitalWrite(MOTB_STEP, HIGH);
  }
  return true;
}
