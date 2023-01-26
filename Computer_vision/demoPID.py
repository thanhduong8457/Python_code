import time
import matplotlib.pyplot as plt
import numpy as np

class pid():
    def __init__(self, Kp, Ki, Kd, Ts):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.Ts = Ts
        self.reference_value = 0
        self.current_value = 0
        self.ek = [0, 0, 0]
        self.uk = [0, 0]

    def cumpute(self, current_value):
        self.current_value = current_value
        self.ek[0] = self.reference_value - self.current_value
        self.uk[0] = self.uk[1] \
                            + self.Kp*(self.ek[0] - self.ek[1]) \
                            + (self.Ki*self.Ts*(self.ek[0] + self.ek[1]))/2 \
                            + (self.Kd*(self.ek[0] - 2*self.ek[1] + self.ek[2]))/self.Ts
        self.uk[1] = self.uk[0]
        self.ek[2] = self.ek[1]
        self.ek[1] = self.ek[0]

        return self.uk[0]

class model():
    def __init__(self, input_value, output_value):
        self.input_value = input_value
        self.output_value = output_value

    def update(self, input_value):
        self.input_value = input_value
        self.output_value += self.input_value/1000
        return self.output_value

class create_square_pulse():
    def __init__(self, min_val, max_val, T_intercal, Ts):
        self.T_intercal = T_intercal
        self.Ts = Ts
        self.num_temp = 0
        self.max_val = max_val
        self.min_val = min_val
        self.output_val = min_val

    def update(self):
        self.num_temp += 1
        if self.num_temp == int(self.T_intercal/self.Ts/2):
            self.output_val = self.max_val
        elif self.num_temp == int(self.T_intercal/self.Ts):
            self.num_temp = 0
            self.output_val = self.min_val
        return self.output_val

def main():
    Kp = 100
    Ki = 20
    Kd = 1
    Ts = 0.01

    uk = 0
    yk = 0

    time_to_simulate = 10

    my_square_pulse = create_square_pulse(500, 1000, 2, Ts)
    my_model = model(uk, yk)
    my_pid = pid(Kp, Ki, Kd, Ts)

    time_to_simulate_temp = 0
    stop_point = int(time_to_simulate/Ts)

    xpoints = np.array(0)
    ypoints = np.array(0)

    while True:
        time_to_simulate_temp += 1

        my_pid.reference_value = my_square_pulse.update()
        uk = my_pid.cumpute(yk)
        yk = my_model.update(uk)
        
        print(uk, yk)
        
        xpoints = np.append(xpoints, my_pid.reference_value)
        ypoints = np.append(ypoints, yk)

        if time_to_simulate_temp == stop_point:
            plt.plot(ypoints)
            plt.plot(xpoints)
            plt.show()
            exit()
        elif time_to_simulate_temp == int(stop_point/4):
            my_pid.reference_value = int(my_pid.reference_value/2)
        elif time_to_simulate_temp == 2*int(stop_point/4):
            my_pid.reference_value = 2*int(my_pid.reference_value)
        elif time_to_simulate_temp == 3*int(stop_point/4):
            my_pid.reference_value = int(my_pid.reference_value/2)

        time.sleep(Ts)

if __name__ == '__main__':
    main()
