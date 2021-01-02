import RPi.GPIO as GPIO
import time



GPIO.setmode(GPIO.BOARD)
resistor = 7
def run():
	while True:
		#output to the pin is given low such that if capacitor is charged,...
		#it will get discharged since there will be 0V across capacitor.

		GPIO.setup(resistor,GPIO.OUT)
		GPIO.output(resistor,GPIO.LOW)
		time.sleep(0.1)
		# now , pin will be used as input
		# pin is set to 'pull up'. consider it as one end of input is connected
		# in ckt and another end to +vcc
		# Now , capacitor will start to discharge . initially , voltage at point where input pin is connected is 0
		# Slowly when capacitor charges, that voltage increases
		GPIO.setup(resistor,GPIO.IN,pull_up_down=GPIO.PUD_UP)
		current_time = time.time()
		diff = 0
		#so till that voltage doesnt reach +vcc(because input is set to PUD_UP)
		#input at the pin will be LOW
		while GPIO.input(resistor)==GPIO.LOW:
			diff = time.time() - current_time
		#indirectly we are measuring the time taken by capacitor to charge up

		print(diff*1000,"miliseconds")
		time.sleep(1)

		# this charging time depends upon resistance of photoresistor .
		# if intensity is more, charging time  is less because resistance is less

if __name__=="__main__":
	try:
		run()
	except KeyboardInterrupt:
		GPIO.cleanup()





