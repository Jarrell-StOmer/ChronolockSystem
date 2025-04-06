#importing necessary libraries
import RPi.GPIO as GPIO
import time
from RPLCD.gpio import CharLCD

#Set warning modes to false
GPIO.setwarnings(False)

#Set board mode and pins
lcd = CharLCD(cols = 16, rows = 2, pin_rs = 18, pin_e = 23, pins_data = [4, 17, 27, 22], numbering_mode = GPIO.BCM)

#Write to the LCD
lcd.cursor_pos = (0, 1)
lcd.write_string("Enter your PIN:",1,0)
time.sleep(2)
lcd.clear()

#Cleanup pins
#GPIO.cleanup()


