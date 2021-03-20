from gpiozero import AngularServo
from enum import Enum
from threading import Thread
import time

# TODO: Add the ability to toggle laser diode

class Direction(Enum):
    Positive=1
    Negative=-1
    NA=0

class LaserSystem:
    def __init__(self):
        self.__ServoVertical = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=.000553, max_pulse_width=.0023, frame_width=.025)
        self.__ServoHorizontal = AngularServo(13, min_angle=0, max_angle=180, min_pulse_width=.000553, max_pulse_width=.0023, frame_width=.025)
        self.__last_known_vert_loc = 90
        self.__last_known_hori_loc = 90
        self.__ServoVertical.angle = None
        self.__ServoHorizontal.angle = None
        # initialize laser diode

    def set_angle(self, servo, servo_direction, angle):
        """ Used for internally setting the servos angle variable and waiting for the positioning to complete """

        if servo_direction == "vertical" and self.__last_known_vert_loc != angle:
            move_degree = abs(self.__last_known_vert_loc - angle)
            servo.angle = angle
            self.__last_known_vert_loc = angle
        elif servo_direction == "horizontal" and self.__last_known_hori_loc != angle:
            move_degree = abs(self.__last_known_hori_loc - angle)
            servo.angle = angle
            self.__last_known_hori_loc = angle
        else:
            return

        time_to_move = (move_degree * .25) / 60
        print(f"{time_to_move} sec")
        time.sleep(time_to_move)
        servo.angle = None
    
    def set_position(self, HorizontalAngle, VerticalAngle):
        """ Used for externally changing the position of the servos """
        thread1 = Thread(target=self.set_angle, args=(self.__ServoVertical, "vertical", VerticalAngle))
        thread2 = Thread(target=self.set_angle, args=(self.__ServoHorizontal, "horizontal", HorizontalAngle))
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

    def move_servo_position(self, x_dir=Direction.NA, y_dir=Direction.NA, sensitivity=1):
        """ Smooth locomotion of the servos, preferably through arrow keys or buttons """
        # x_dir and y_dir should be set to -1, 0 , 1 depending on their direction
        if (
            self.__last_known_hori_loc + x_dir.value * .01 * sensitivity >= self.__ServoHorizontal.min_angle
            and self.__last_known_hori_loc + x_dir.value * .01 * sensitivity <= self.__ServoHorizontal.max_angle 
            and self.__last_known_vert_loc + y_dir.value * .01 * sensitivity >= self.__ServoVertical.min_angle 
            and self.__last_known_vert_loc + y_dir.value * .01 * sensitivity <= self.__ServoVertical.max_angle
           ):
            x_pos = self.__last_known_hori_loc + x_dir.value * .01 * sensitivity

            y_pos = self.__last_known_vert_loc + y_dir.value * .01 * sensitivity
            print(f"{x_pos}, {y_pos}")
            self.set_position(x_pos, y_pos)
            # self.__ServoHorizontal.angle = x_pos
            # self.__ServoVertical.angle = y_pos

            #print(self.get_angle())

    def get_target_position(self):
        """ Functionally the same as get_angle, returns the set positions of the servos in a list """
        return [self.__ServoHorizontal.angle, self.__ServoVertical.angle]

    def get_angle(self):
        """ Functionally the same as get_target_position, returns the set positions of the servos in a list """
        return [self.__last_known_hori_loc, self.__last_known_vert_loc]

    def default_position(self):
        """ Sets the servos to a default position at 90, 90, which should point straight down."""
        self.set_position(90, 90)
        # Turn off laser diode

    def left_button_click(self):
        self.move_servo_position(x_dir=Direction.Negative, y_dir=Direction.NA, sensitivity=100)
    
    def right_button_click(self):
        self.move_servo_position(x_dir=Direction.Positive, y_dir=Direction.NA, sensitivity=100)
        
    def up_button_click(self):
        self.move_servo_position(x_dir=Direction.NA, y_dir=Direction.Positive, sensitivity=100)
        
    def down_button_click(self):
        self.move_servo_position(x_dir=Direction.NA, y_dir=Direction.Negative, sensitivity=100)
    

if __name__ == '__main__':
    start = time.time()

    Pointer = LaserSystem()

    for i in range(0, 51):
        Pointer.set_position(0, 0)
        Pointer.set_position(90, 90)


    Pointer.default_position()

    end = time.time()
    print(f"time elapsed: {end - start}")