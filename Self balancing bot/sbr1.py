import RPi.GPIO as GPIO
import time
import math
from adxl345 import ADXL345
#ADXL345 library helps to read acceleration along all3 axes
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
T = 0.001

# These are optimul values of parameters obtained after tuning
kp = 1300
kd = 0.8
ki = 900

# To stop motor call this function
def motorStop():
    GPIO.output(MotorPin_A, GPIO.LOW)
    GPIO.output(MotorPin_B, GPIO.LOW)
    GPIO.output(MotorPin_C, GPIO.LOW)
    GPIO.output(MotorPin_D, GPIO.LOW)
    pwm_B.ChangeDutyCycle(0)
    pwm_D.ChangeDutyCycle(0)

# Initial setups
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
    pwm_B = GPIO.PWM(MotorPinPWM_B, 1000)  # create pwm and set frequece to 1kHz
    pwm_D = GPIO.PWM(MotorPinPWM_D, 1000)  # create pwm and set frequece to 1KHz
    pwm_B.start(100)
    pwm_D.start(100)
    motorStop()

# To control direction and speed of motors call this function
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

# At termination of program call this function
def destroy():
    motorStop()
    GPIO.cleanup()

# This function reads acceleration, calculates the angle of tilt and returns it. In case of any exception like division by zero is handled
# Supplimentary function
def getAngleSup():
    axes = adxl345.getAxes(True)
    try:
        angle = math.atan(axes['x'] / axes['z'])
    except ZeroDivisionError:
        angle = 0
    return (angle)

# Takes angle 19 times. Takes their median and returns. This is done to reduce noise.
def getAngle():
    lst = []
    for i in range(19):
        lst.append(getAngleSup())
    lst.sort()
    return (lst[len(lst) // 2])

# Initially when we place bot horizontal and run our program, it is better to set reference angle at which bot will be balanced
def setRef():
    global ref
    lst = []
    for i in range(1001):
        lst.append(getAngleSup())
    ref = lst[len(lst) // 2]

# our main function
def loop():
    setRef()
    old_error = 0   # for derivative control
    E = 0         # for integral control
    while True:
        angle = getAngle()  # read the angle continuously
        error = ref - angle  # find error
        E = E + error        # integration of error
        output = kp * error + kd * (old_error - error) / T + ki * E * T   # PID output
        # output = output*30
        # Direction and speed set
        if output > 0:
            # output = 0.5*output+50
            output = min(output, 100)
            if (output < 80):
                output = 0
            motor(1, output)
        else:
            output = abs(output)
            # output = 0.5*output+50
            output = min(output, 100)
            if (output < 80):
                output = 0
            motor(-1, output)

        if error * old_error < 0:   # So when bot comes at ref position, we are setting E=0 i.e. create new system from here.
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