#include <arduino.h>
#include "display.h"

PicoLCD_I2C lcd(0, 0x27, LCD_SDA, LCD_SCL);

// -----------------------------------------------------------------------------------------
void LCD_Display::init(void) {
  mot_a_is_power = true;
  mot_a_is_enabled = true;
  mot_b_is_power = true;
  mot_b_is_enabled = true;
  lcd.begin();
  lcd.print("RaspiCar MotDriver");
  delay(100);
  mot_a_power(false);
  mot_a_enabled(false);
  mot_a_rpm(0);
  mot_b_power(false);
  mot_b_enabled(false);
  mot_b_rpm(0);
  lcd.setCursor(19, 3);
  lcd.write('V');
}

// -----------------------------------------------------------------------------------------
void LCD_Display::mot_a_enabled(bool state) {
  if (state != mot_a_is_enabled) {
    lcd.setCursor(LCD_X_MOTA_E, 3);
    if (state) lcd.write('*');
    else lcd.write('-');
    mot_a_is_enabled = state;
  }
}

// -----------------------------------------------------------------------------------------
void LCD_Display::mot_b_enabled(bool state) {
  if (state != mot_b_is_enabled) {
    lcd.setCursor(LCD_X_MOTB_E, 3);
    if (state) lcd.write('*');
    else lcd.write('-');
    mot_b_is_enabled = state;
  }
}

// -----------------------------------------------------------------------------------------
void LCD_Display::mot_a_power(bool state) {
  if (state != mot_a_is_power) {
    lcd.setCursor(LCD_X_MOTA_P, 3);
    if (state) lcd.write('*');
    else lcd.write('-');
    mot_a_is_power = state;
  }
}

// -----------------------------------------------------------------------------------------
void LCD_Display::mot_b_power(bool state) {
  if (state != mot_b_is_power) {
    lcd.setCursor(LCD_X_MOTB_P, 3);
    if (state) lcd.write('*');
    else lcd.write('-');
    mot_b_is_power = state;
  }
}

// -----------------------------------------------------------------------------------------
void LCD_Display::mot_a_rpm(uint32_t rpm) {
  lcd.setCursor(LCD_X_MOTA_RPM, 3);
  print_dec(rpm);
}

// -----------------------------------------------------------------------------------------
void LCD_Display::mot_b_rpm(uint32_t rpm) {
  lcd.setCursor(LCD_X_MOTB_RPM, 3);
  print_dec(rpm);
}

// -----------------------------------------------------------------------------------------

void LCD_Display::print_dec(int n) {
  char local_buf[5];
  if (n < 1000) lcd.write(' ');
  if (n < 100) lcd.write(' ');
  if (n < 10) lcd.write(' ');
  itoa(n, local_buf, 10);
  lcd.print(local_buf);
}

//-------------------------------------------------------------------------
void LCD_Display::show_voltage(uint16_t bat_voltage) {
  char buf[8];
  lcd.setCursor(LCD_X_BAT_VOLTAGE, 3);
  itoaf(bat_voltage / 10, buf, 3, 1, false);
  lcd.print(buf);
}

//-------------------------------------------------------------------------
void LCD_Display::shutdown(void) {
  lcd.setCursor(0, 0);
  lcd.print("Shut down ...       ");
}

//-------------------------------------------------------------------------
void LCD_Display::shutdown_timer(int i) {
  lcd.setCursor(19, 0);
  lcd.write('0' + i);
}

//-------------------------------------------------------------------------
void LCD_Display::clear(void) {
  lcd.setCursor(0, 0);
  lcd.print("                    ");
  lcd.setCursor(0, 1);
  lcd.print("                    ");
  lcd.setCursor(0, 3);
  lcd.print("                    ");
}

//-------------------------------------------------------------------------
void LCD_Display::print_title(char buf[]) {
  int l = strlen(buf);
  lcd.setCursor(0, 0);
  if (l > 20) buf[20] = '\0';
  lcd.print(buf);
  for (int i = 0; i < 20 - l; ++i) lcd.write(' ');;
}

//-------------------------------------------------------------------------
void LCD_Display::print_message(char buf[]) {
  int l = strlen(buf);
  lcd.setCursor(0, 1);
  lcd.print("                    ");
  lcd.setCursor(0, 2);
  lcd.print("                    ");
  lcd.setCursor(0, 1);
  if (l > 20) {
    for (int i = 0; i < 20; ++i) lcd.write(buf[i]);
    lcd.setCursor(0, 2);
    for (int i = 0; i < l - 20; ++i) lcd.write(buf[i+20]);
  } else {
    lcd.print(buf);
  }
}
