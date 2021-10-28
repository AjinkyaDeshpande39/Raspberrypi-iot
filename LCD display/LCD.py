import RPi.GPIO as GPIO
import time

from adafruit_lcd import Adafruit_CharLCD

def loop():
        lcd = Adafruit_CharLCD()
        while True:
                lcd.clear()
                lcd.message(" Visvesvaraya")
                time.sleep(1)
                lcd.clear()
                lcd.message(" National")
                time.sleep(1)
                lcd.clear()
                lcd.message("Institute of")
                time.sleep(1)
                lcd.clear()
                lcd.message("Technology")
                time.sleep(1)
                lcd.clear()
                

if __name__ == '__main__':
        loop()
