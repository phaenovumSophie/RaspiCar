#ifndef __MOTORS__
#define __MOTORS__

#include <arduino.h>

// pin definitions
#define MOTA_PWR         21
#define MOTA_STEP        20
#define MOTA_DIR         19
#define MOTB_PWR         18
#define MOTB_STEP        17
#define MOTB_DIR         16

// Motor step time
#define MOT_STEP_TIME_MAX 150000
#define MOT_STEP_TIME_MIN    100
#define CONVERSION_FACTOR 150000
#define MOT_RAMP              10
#define RPM_MAX             1500
#define RPM_MIN                1

// Function prototypes
bool mot_a_timer_callback(struct repeating_timer *t);
bool mot_b_timer_callback(struct repeating_timer *t);

class Motors {
  private:
	  uint32_t a_rpm = RPM_MIN;
	  uint32_t b_rpm = RPM_MIN;
    bool a_dir = true;
    bool b_dir = true;
	  int ramp = 20;
	  uint32_t calc_step_time(uint32_t rpm, uint32_t old_step_time, uint16_t step_width, bool up);

  public:
    bool a_enabled = false;
    bool b_enabled = false;
    bool a_power = false;
    bool b_power = false;

  	uint32_t a_step_time = MOT_STEP_TIME_MAX, b_step_time = MOT_STEP_TIME_MAX;
  	uint32_t a_step_time_target = a_step_time, b_step_time_target = b_step_time;
    void init(void);
  	void set_a_enable(bool status);
  	void set_b_enable(bool status);
    bool get_a_enabled(void);
    bool get_b_enabled(void);  	
  	void set_a_power(bool status);
  	void set_b_power(bool status);
    bool get_a_power(void);
    bool get_b_power(void);
  	void check_step_time_a(void);
  	void check_step_time_b(void);
    void set_a_steptime(uint32_t steptime);
    void set_b_steptime(uint32_t steptime);
    void set_a_rpm(uint32_t rpm);
    void set_b_rpm(uint32_t rpm);
    uint32_t get_a_rpm(void);
    uint32_t get_b_rpm(void);
	
};


#endif
