from Maestro import maestro
from gpiozero import LED
from enum import Enum
from threading import Thread
import time
import numpy as np

# TODO: Add the ability to toggle laser diode

class Direction(Enum):
    Positive=1
    Negative=-1
    NA=0


class LaserSystem:
    def __init__(self):
        self.servo = maestro.Controller()
        self.__ServoVertical = 0
        self.__ServoHorizontal = 1
        self.servo.setAccel(self.__ServoVertical, 100)
        self.servo.setAccel(self.__ServoHorizontal, 100)
        self.servo.setSpeed(self.__ServoVertical, 100)
        self.servo.setSpeed(self.__ServoHorizontal, 100)
        self.servo.setRange(self.__ServoVertical, 2400, 9600)
        self.servo.setRange(self.__ServoHorizontal, 2400, 9600)

        self.laser = LED(17)
        self.laser.on()


    def _set_angle(self, servo_name, angle):
        """ Used for internally setting the servos angle variable and waiting for the positioning to complete """
        self.servo.setTarget(servo_name, angle)
        
    def set_position(self, HorizontalAngle, VerticalAngle):
        """ Used for externally changing the position of the servos """
        VerticalAngle = self.to_maestro(VerticalAngle)
        HorizontalAngle = self.to_maestro(HorizontalAngle)
        thread1 = Thread(target=self._set_angle, args=(self.__ServoVertical, VerticalAngle))
        thread2 = Thread(target=self._set_angle, args=(self.__ServoHorizontal, HorizontalAngle))
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    def move_servo_position(self, x_dir=Direction.NA, y_dir=Direction.NA, sensitivity=1):
        """ Smooth locomotion of the servos, preferably through arrow keys or buttons """
        # x_dir and y_dir should be set to -1, 0 , 1 depending on their direction
        if (
            self.servo.getPosition(self.__ServoHorizontal) + x_dir.value * .01 * sensitivity >= self.servo.getMin(self.__ServoHorizontal)
            and self.servo.getPosition(self.__ServoHorizontal) + x_dir.value * .01 * sensitivity <= self.servo.getMax(self.__ServoHorizontal)
            and self.servo.getPosition(self.__ServoVertical) + y_dir.value * .01 * sensitivity >= self.servo.getMin(self.__ServoVertical) 
            and self.servo.getPosition(self.__ServoVertical) + y_dir.value * .01 * sensitivity <= self.servo.getMax(self.__ServoVertical)
           ):
            x_pos = self.to_degree(self.servo.getPosition(self.__ServoHorizontal)) + x_dir.value * .01 * sensitivity

            y_pos = self.to_degree(self.servo.getPosition(self.__ServoVertical)) + y_dir.value * .01 * sensitivity
            print(f"{x_pos}, {y_pos}")
            self.set_position(x_pos, y_pos)
            # self.__ServoHorizontal.angle = x_pos
            # self.__ServoVertical.angle = y_pos

            #print(self.get_angle())

    def get_target_position(self):
        """ Functionally the same as get_angle, returns the set positions of the servos in a list """
        return [self.to_degree(self.servo.getPosition(self.__ServoHorizontal)), self.to_degree(self.servo.getPosition(self.__ServoVertical))]

    def get_angle(self):
        """ Functionally the same as get_target_position, returns the set positions of the servos in a list """
        return [self.to_degree(self.servo.getPosition(self.__ServoHorizontal)), self.to_degree(self.servo.getPosition(self.__ServoVertical))]

    def default_position(self):
        """ Sets the servos to a default position at 90, 90, which should point straight down."""
        self.set_position(90, 90)
        self.toggle_laser()

    def to_maestro(self, degree):
        """ Converting from degree to servo range. """
        servo_angle = (degree * (9600 - 2400))/(180) + 2400
        return int(servo_angle)

    def to_degree(self, maestro_value):
        """ Converting from servo range to degree. """
        servo_angle = ((maestro_value - 2400) * 180)/(9600 - 2400)
        return float(servo_angle)

    def left_button_click(self):
        self.move_servo_position(x_dir=Direction.Negative, y_dir=Direction.NA, sensitivity=100)
    
    def right_button_click(self):
        self.move_servo_position(x_dir=Direction.Positive, y_dir=Direction.NA, sensitivity=100)
        
    def up_button_click(self):
        self.move_servo_position(x_dir=Direction.NA, y_dir=Direction.Positive, sensitivity=100)
        
    def down_button_click(self):
        self.move_servo_position(x_dir=Direction.NA, y_dir=Direction.Negative, sensitivity=100)

    def jiggle(self, iter=1):
        origin = self.get_target_position()
        print(f"origin: {origin}")

        x = 0
        y = 0

        for i in range(0, iter):
            for i in np.arange(0, 2 * np.pi, .1):
                x = origin[0] + (3 * np.cos(i))
                y = origin[1] + (3 * np.sin(i))
                if( int(x) not in range(42, 49) or int(y) not in range(132, 139)):
                    print(f"{x}, {y}")

                self.set_position(x, y)
                time.sleep(.05)
        
        self.set_position(origin[0], origin[1])
        time.sleep(1)

    
    def toggle_laser(self, state='off'):
        """ Toggling the laser to defined state. """
        if state == 'off':
            self.laser.off()
        elif state == 'on':
            self.laser.on()
        else:
            print("invalid state in toggle_laser call")
    

if __name__ == '__main__':
    start = time.time()

    Pointer = LaserSystem()
    Pointer.set_position(45, 135)
    time.sleep(1)
    Pointer.toggle_laser(state='on')
    
    while(True):
        Pointer.jiggle(50)
    # print(Pointer.get_target_position())

    end = time.time()
    print(f"time elapsed: {end - start}")

    Pointer.servo.close()
