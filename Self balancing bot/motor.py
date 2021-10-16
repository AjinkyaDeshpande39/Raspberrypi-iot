# This code is for L298N motor driver IC and 2 BO motor control.
import RPi.GPIO as GPIO
import time
import math

MotorPin_A = 11
MotorPin_B = 13
MotorPin_C = 15
MotorPin_D = 16

MotorPinPWM_B = 38
MotorPinPWM_D = 40

pwm_B = 0
pwm_D = 0


def motorStop():
    GPIO.output(MotorPin_A, GPIO.LOW)
    GPIO.output(MotorPin_B, GPIO.LOW)
    GPIO.output(MotorPin_C, GPIO.LOW)
    GPIO.output(MotorPin_D, GPIO.LOW)
    pwm_B.ChangeDutyCycle(0)
    pwm_D.ChangeDutyCycle(0)


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MotorPin_A, GPIO.OUT)
    GPIO.setup(MotorPin_B, GPIO.OUT)
    GPIO.setup(MotorPin_C, GPIO.OUT)
    GPIO.setup(MotorPin_D, GPIO.OUT)
    GPIO.setup(MotorPinPWM_B, GPIO.OUT)
    GPIO.setup(MotorPinPWM_D, GPIO.OUT)

    global pwm_B
    global pwm_D
    pwm_B = GPIO.PWM(MotorPinPWM_B, 20000)  # create pwm and set frequece to 20KHz
    pwm_D = GPIO.PWM(MotorPinPWM_D, 20000)  # create pwm and set frequece to 20KHz
    pwm_B.start(100)
    pwm_D.start(100)
    motorStop()


def motor(direction, speed):
    if direction == 1:
        GPIO.output(MotorPin_A, GPIO.HIGH)
        GPIO.output(MotorPin_B, GPIO.LOW)
        GPIO.output(MotorPin_C, GPIO.HIGH)
        GPIO.output(MotorPin_D, GPIO.LOW)
        pwm_B.ChangeDutyCycle(speed)
        pwm_D.ChangeDutyCycle(speed)
    elif direction == -1:
        GPIO.output(MotorPin_A, GPIO.LOW)
        GPIO.output(MotorPin_B, GPIO.HIGH)
        GPIO.output(MotorPin_C, GPIO.LOW)
        GPIO.output(MotorPin_D, GPIO.HIGH)
        pwm_B.ChangeDutyCycle(speed)
        pwm_D.ChangeDutyCycle(speed)
    else:
        motorStop()


def destroy():
    motorStop()
    GPIO.cleanup()


def loop():
    motor(1, 100)
    while True:
        pass


if _name == "main_":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()