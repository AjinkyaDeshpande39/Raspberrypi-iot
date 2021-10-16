import RPi.GPIO as GPIO
import time
import math
from adxl345 import ADXL345

adxl345 = ADXL345()

MotorPin_A = 11
MotorPin_B = 13
MotorPin_C = 15
MotorPin_D = 16

MotorPinPWM_B = 38
MotorPinPWM_D = 40

pwm_B = 0
pwm_D = 0

ref = 0
T = 0.05

kp = 30
kd = 0.8
ki = 0


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
    pwm_B = GPIO.PWM(MotorPinPWM_B, 1000)  # create pwm and set frequece to 20KHz
    pwm_D = GPIO.PWM(MotorPinPWM_D, 1000)  # create pwm and set frequece to 20KHz
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


def getAngle():
    axes = adxl345.getAxes(True)
    try:
        angle = math.atan(axes['x'] / axes['z'])
    except ZeroDivisionError:
        angle = 0
    return (angle, axes['x'], axes['y'], axes['z'])


def setRef():
    global ref
    lst = []
    for i in range(1000):
        lst.append(getAngle()[0])
    ref = lst[len(lst) // 2]


def loop():
    setRef()
    old_error = 0
    E = 0
    while True:
        angle,_,_,_ = getAngle()
        error = ref - angle
        E = E + error
        output = kp * error + kd * (error - old_error) / T + ki * E * T
        output = output * 30
        if output > 0:
            # output = 0.5*output+50
            output = min(output, 100)
            if (output < 50):
                output = 0
            motor(1, output)
        else:
            output = abs(output)
            # output = 0.5*output+50
            output = min(output, 100)
            if (output < 50):
                output = 0
            motor(-1, output)

        if error * old_error < 0:
            E = 0
        print(angle, output)

        old_error = error
        time.sleep(T)


if __name__ == "_main_":
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    except IOError:
        print("IOError: [Errno 121] Remote I/O error")
        destroy()
    except Exception as e:
        print(e.message())
        destroy()