import matplotlib.pyplot as plt
import  time
import numpy as np
import math
def getAngle():
    pass
def getError():
    pass



if __name__ == "__main__":
    ref = 1
    curr = 0
    E = 0
    old_error = ref-curr
    kp = 5
    ki = 1
    kd = 1

    curr_list = []

    init_time = time.time()
    for i in range(100):
        curr_list.append(curr)
        error = ref-curr
        E += error
        e_dot = error-old_error

        output = kp*error + ki*E + kd*e_dot

        old_error = error
        curr = curr+0.1*output

    final_time = time.time()
    # print(final_time,init_time)
    # time_axis = np.linspace(0,final_time-init_time,1000,dtype=np.float)
    # print(time_axis)
    plt.plot(curr_list)
    plt.grid()
    plt.show()