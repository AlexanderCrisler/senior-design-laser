from Maestro import maestro
import time
import random

servo_min = 600 * 4
servo_max = 2400 * 4


servo = maestro.Controller()
servo.setAccel(0,100)      #set servo 0 acceleration to 4
servo.setSpeed(0,100)

servo.setAccel(1,100)
servo.setSpeed(1,100)

servo.setRange(0, servo_min, servo_max)
servo.setRange(1, servo_min, servo_max)
#servo.setTarget(0, 1500)  #set servo to move to center position
     #set speed of servo 1

# print(f"max: {servo.getMax(0)} min: {servo.getMin(0)}")

# print(f"1 {servo.getPosition(0)}") #get the current position of servo 1
# servo.setTarget(0, servo_min)
# servo.setTarget(1, servo_min)
# print(f"2 {servo.getPosition(0)}")
# time.sleep(2)
# servo.setTarget(0, servo_max)
# servo.setTarget(1, servo_max)
# print(f"3 {servo.getPosition(0)}")
# time.sleep(2)

# for i in range(servo_min, servo_max, 40):
#     servo.setTarget(0, i)
#     servo.setTarget(1, i)
#     time.sleep(.1)

# for i in range(0, 99):
#     servo.setTarget(0, 1980 * 4)
#     servo.setTarget(1, 1610 * 4)
#     time.sleep(1)

#     servo.setTarget(0, 2025 * 4)
#     servo.setTarget(1, 1615 * 4)
#     time.sleep(1)

#     servo.setTarget(0, 2190 * 4)
#     servo.setTarget(1, 1625 * 4)
#     time.sleep(1)

    # servo.setTarget(0, 865 * 4)
    # servo.setTarget(1, 1140 * 4)
    # time.sleep(1)
# servo.setTarget(0, 1500 * 4)
# servo.setTarget(1, 1500 * 4)

class Sensor():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.hit_count = 0
    
    def hit(self):
        self.hit_count += 1

sensors = [
    Sensor(1, (1980*4, 1610*4)), 
    Sensor(2, (2035*4, 1620*4)), 
    Sensor(3, (2190*4, 1625*4)),
    Sensor(4, (865*4, 1140*4))
    ]

last_hit = None

try:
    while sensors:
        target = random.choice(sensors)
        if target == last_hit:
            continue
        last_hit = target
        target.hit()

        print(target.name)
        servo.setTarget(0, target.location[0])
        servo.setTarget(1, target.location[1])
        time.sleep(1)

        for sensor in sensors:
            if sensor.hit_count == 999:
                sensors.remove(sensor)
                print(f"{sensor} removed.")

except KeyboardInterrupt:
    servo.setTarget(0, 6000)
    servo.setTarget(1, 6000)
    time.sleep(1)
    servo.setTarget(0, 2400)
    servo.setTarget(1, 2400)
    time.sleep(1)

#print(x)
servo.close()