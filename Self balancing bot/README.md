## Abstract: 🤖
   We will be balancing bot on 2 wheels. Relate this to human responses. When we fall ahead, we move ahead. When we fall behind, we move behind. We will measure angle of inclination with horizontal axis using Accelerometer. Take tanh of ratio of acceleration in x and z direction. This will be input of our system. We will use PID controller to produce output that is rotational torque. Motors will rotate accordingly and bot wont fall. If tunning done properly, motors will rotate so precisely that bot will resemble to be balanced. PWM helps us to manage speed of motor. So, output of PID controller will be width of pulse. If given 100, motor runs at max speed. If given below 40, motor stops(basically due to voltage wont be sufficient enough to drive motor). :


## Requirements:  🧰
1) Raspberrypi4B\
<p align="center">
  <img width="200" src="https://github.com/AjinkyaDeshpande39/Raspberrypi-iot/blob/master/Self%20balancing%20bot/Images%20and%20GIF/RPi.png">
</p>

2) BO motors ( 150RMP at least, 0.8N.cm. Gear motors provide good amount of torque which is very much necessary to carry load. BO motors are cheap and provide enough RPM and Torque for this purpose)\
<p align="center">
  <img width="200" src="https://github.com/AjinkyaDeshpande39/Raspberrypi-iot/blob/master/Self%20balancing%20bot/Images%20and%20GIF/BO%20motor.png">
</p>


3) ADXL345 (It is accelerometer that measures gravitational acceleration in x,y,z axes by which we will compute angle by which bot has tilted)\
<p align="center">
  <img width="200" src="https://github.com/AjinkyaDeshpande39/Raspberrypi-iot/blob/master/Self%20balancing%20bot/Images%20and%20GIF/adxl345-triple-axis-accelerometer-india-800x800.jpg">
</p>

4) L298N (you can use L293D also it works on till 1A whereas L298N works for 2A)\
<p align="center">
  <img width="200" src="https://github.com/AjinkyaDeshpande39/Raspberrypi-iot/blob/master/Self%20balancing%20bot/Images%20and%20GIF/l298.png">
</p>


5) Jumpers (F-F since we will be connecting directly modules to RPi. If you are using ICs then you will need M-F, M-M jumpers as well as breadboard/PCB(soldering))

6) Lightweight base like thermocol.
(dont stick by 2sided tape. it is very feebly)



   
## PID Controller and ADXL345:  🎛️
   P = Proportional\
   I = Integral\
   D = Derivative\
   This controller helps us to tune system such that, system respond fast, steady state error is low, dynamic oscillations are less.\ 
   We will implement PID as follows:\
      <ul>error = curr - ref\
         output = kp\*error + ki\*E + kd\*(error-old_error)\
         E = E +error </ul>
   E is integration of error till now.\
   We make sure that when system achieves 0 error, nullify E. i.e., new scenario begins. If we do not make E 0, it causes a lot of noise and improper measurements.\
   
   *How to tune ?*
   1) First tune kp. Make kp sufficient enough that bot doesnt fall(i.e. rize time is small). But not so fast that bot starts dancing and crashing. At proper kp, bot oscillated back and forth at small scale.
   2) Tune ki or kd (still a question to me. working on it....)
   3) Tune ki - till steady state is achieved sufficiently faster. Steady state error can be reduced using this ki tuning.
   4) Tune kd - to reduce oscillation and smoothen dynamic response.
   *you can also experiment with only PD or PI controller*\
   We will calculate angle using ADXL345 in every iteration. It will be curr value. ref will be set initially. Median of angles taken initially over a large number of samples.(1000 samples == time req. in msec). Since we are using only accelerometer, and not gyroscope, a little bit of noise in system could be observed. ADXL measures angle in 3 axes. Basically inside ADXL, there are variable capacitors. Capacitors vary due to gravitational acceleration. ADXL345 can be operated using I2C protocol. So, before running program, make sure that I2C interfacing is on!!!\
   
   <ul>*Usually we keep ADXL345 near axis of rotation to avoid noise in measurement.*</ul>
   <ul><li>We are using accelerometer only and not gyroscope. Only accelerometer induces noise which here i am removing by taking many samples and taking median</li></ul>
   
   We supply pulse either high or low through GPIO pins. PWM allows us to control for how much time we can keep pulse high and low. 100 pulse width means pulse high for all time. 50=high for half time.... We can also set frequency of this pulse. Usually we use 2000Hz pulse. So, if pulse is high for long time, current will be provided for long time. hence, motor will run faster. In on-off-on-off situation, motor resembles rotating at lower speed.
   
   <ul><li>I Connected CS pin to +5V instead of +3V because i was getting IO error in middle of process</li></ul>
   
   
## PWM and motor driver module:   
   Use motors of atleast 150rpm and sufficient amount of torque. I have tried using high rpm but less torque which wasnt able to bear the load of RPi itselt. Hence geared motor - bo motor is prefered. Since it is a small scale project, BO motors are sufficient. Motor driver module L298N works for motor till 35V and 2A. Earlier i have tried L293D ic which works for lower current motors, but found out that max speed acheived is high for L298N. One more observation was - If i set PWM lower(less than 60 at 1000Hz freq) motor wont rotate and driver makes hearable noise. If you increase freq, noise freq also increases and lower limit too(70-75-80 likewise). \
   <ul><li>Motor drivers are necessary since they provide large current required to drive current, as well as direction and speed control is possible. Prefer L298N.</ul></li>
   <ul><li>I have powered motor driver with an 10V open ckt adapter instead of using batteries. Batteries discharge within 1-2 days. Also, 6-9V was required for good rpm. Adapter is sustainable, constant source and i suggest to use it only.</ul></li>
   <ul><li>Base also matters a lot. Earlier, i used breadboard as base which was heavier hence bot couldnt speed much. Later i changed it with thermocol</ul></li> 
   
   <ul><li>Dont forget to connect all grounds at one pin.</li></ul> 
   
   
   
    
## Tests:
Very premitive test
https://youtu.be/09PRFaCYIq0

A bit more robust version. Sample rate is increased. And better tuning is done.
https://youtu.be/g6OKTV2-NLo

Best PID tuning. 😃 Final Test. A good Ki results in such good robustness. kp=1300, kd-0.8, ki=900. Sampling rate = per milisecond. I have also done filtering to reduce noise by taking median over 20 samples. Also, added code for setting reference angle at begining.
https://youtu.be/_khguo-Qc-w 

## Circuit:

![](https://github.com/AjinkyaDeshpande39/Raspberrypi-iot/blob/master/Self%20balancing%20bot/Images%20and%20GIF/modelgif.gif)
![](https://github.com/AjinkyaDeshpande39/Raspberrypi-iot/blob/master/Self%20balancing%20bot/Images%20and%20GIF/skyview.jpeg)
