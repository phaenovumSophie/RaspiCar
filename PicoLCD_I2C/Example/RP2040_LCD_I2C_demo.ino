/* 
 *  Example for HD44780 display with I2C interface, hosted by rp2040
 *  Display with 4 lines and 20 characters per line
 */

#include <PicoLCD_I2C.h>

PicoLCD_I2C lcd(0, 0x27, 4, 5);
int cnt = 0;

//---------------------------------------------------------
void setup() {
  lcd.begin();
  lcd.print("Hello from Pico");
}

//---------------------------------------------------------
void loop() {
  char buf[10];

  if (cnt % 20 > 0) lcd.setBacklight(true);
  else lcd.setBacklight(false);
  
  lcd.setCursor(3, 1);      // x and y position
  itoa(cnt, buf, 10);
  lcd.print(buf);
  cnt += 1;
  delay(500);
  
  lcd.setCursor(8, 2);
  itoa(cnt, buf, 10);
  lcd.print(buf);
  cnt += 1;
  delay(500);

  lcd.setCursor(13, 3);
  itoa(cnt, buf, 10);
  lcd.print(buf);
  cnt += 1;
  delay(500);

}
