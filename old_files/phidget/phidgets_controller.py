import Phidget22.Phidget
import Phidget22.Devices.RCServo
import enum
import time


class Direction(enum.Enum):
	Positive=1
	Negative=-1
	NA=0


class LaserSystem:
	def __init__(self):
		self.__ServoVertical = Phidget22.Devices.RCServo.RCServo()
		self.__ServoHorizontal = Phidget22.Devices.RCServo.RCServo()
		self.__ServoHorizontal.setChannel(0)
		self.__ServoVertical.setChannel(1)
		self.__ServoVertical.openWaitForAttachment(5000)
		self.__ServoHorizontal.openWaitForAttachment(5000)
		time.sleep(1)
		self.__ServoVertical.setTargetPosition(0)
		self.__ServoHorizontal.setTargetPosition(0)
		time.sleep(1)
		self.__ServoVertical.setEngaged(True)
		self.__ServoHorizontal.setEngaged(True)


	def SetPosition(self,HorizontalAngle,VerticalAngle):
		self.__ServoVertical.setTargetPosition(VerticalAngle)
		self.__ServoHorizontal.setTargetPosition(HorizontalAngle)
		self.__ServoVertical.setEngaged(True)
		self.__ServoHorizontal.setEngaged(True)
		# while abs(self.__ServoHorizontal.getPosition()-HorizontalAngle)<1  or abs(self.__ServoVertical.getPosition()-VerticalAngle)<1:
		# 	#print(int(CurrentServo.getPosition()))
		# 	#print(int(CurrentServo.getTargetPosition()))
		# 	time.sleep(.1)
		print("Success Position")

	def move_servo_position(self, x_dir=Direction.NA, y_dir=Direction.NA, sensitivity=1):
		# x_dir and y_dir should be set to -1, 0 , 1 depending on their direction
		if (
			self.__ServoHorizontal.getTargetPosition() + x_dir.value * .01 * sensitivity >= self.__ServoHorizontal.getMinPosition() 
			and self.__ServoHorizontal.getTargetPosition() + x_dir.value * .01 * sensitivity <= self.__ServoHorizontal.getMaxPosition() 
			and self.__ServoVertical.getTargetPosition() + y_dir.value * .01 * sensitivity >= self.__ServoVertical.getMinPosition() 
			and self.__ServoVertical.getTargetPosition() + y_dir.value * .01 * sensitivity <= self.__ServoVertical.getMaxPosition()
		):
			x_pos = self.__ServoHorizontal.getTargetPosition() + x_dir.value * .01 * sensitivity

			y_pos = self.__ServoVertical.getTargetPosition() + y_dir.value * .01 * sensitivity

			self.__ServoHorizontal.setTargetPosition(x_pos)
			self.__ServoVertical.setTargetPosition(y_pos)
			
			#print(self.Get_Angle())

    def keypressed(self, event):
        #print(event.keysym)
        start = time.time()
        sensitivity = 0      # Sensitivity of the laser movement

        # ARROWKEY Directional Controls
        while keyboard.is_pressed('up'):
            current = time.time()
            sensitivity = (current - start + 1)*(current - start + 1)
            #print(f'up {sensitivity}')
            phidgets_ctlr.move_servo_position(x_dir=Direction.NA, y_dir=Direction.Positive, sensitivity=sensitivity)

        while keyboard.is_pressed('left'):
            current = time.time()
            sensitivity = (current - start + 1)*(current - start + 1)
            #print(f'left {sensitivity}')
            phidgets_ctlr.move_servo_position(x_dir=Direction.Negative, y_dir=Direction.NA, sensitivity=sensitivity)

        while keyboard.is_pressed('down'):
            current = time.time()
            sensitivity = (current - start + 1)*(current - start + 1)
            #print(f'down {sensitivity}')
            phidgets_ctlr.move_servo_position(x_dir=Direction.NA, y_dir=Direction.Negative, sensitivity=sensitivity)

        while keyboard.is_pressed('right'):
            current = time.time()
            sensitivity = (current - start + 1)*(current - start + 1)
            #print(f'right {sensitivity}')
            phidgets_ctlr.move_servo_position(x_dir=Direction.Positive, y_dir=Direction.NA, sensitivity=sensitivity)

    def left_button_click(self):
        phidgets_ctlr.move_servo_position(x_dir=Direction.Negative, y_dir=Direction.NA, sensitivity=100)
    
    def right_button_click(self):
        phidgets_ctlr.move_servo_position(x_dir=Direction.Positive, y_dir=Direction.NA, sensitivity=100)
        
    def up_button_click(self):
        phidgets_ctlr.move_servo_position(x_dir=Direction.NA, y_dir=Direction.Positive, sensitivity=100)
        
    def down_button_click(self):
        phidgets_ctlr.move_servo_position(x_dir=Direction.NA, y_dir=Direction.Negative, sensitivity=100)
    
    def set_location(self):
        self.closed=True
        position = phidgets_ctlr.Get_TargetPosition()
        self.horizontal = position[0]
        self.vertical = position[1]
        self.master.destroy()
	
	def Get_TargetPosition(self):
		return [self.__ServoHorizontal.getTargetPosition(), self.__ServoVertical.getTargetPosition()]

	def Get_Angle(self):
		return [self.__ServoHorizontal.getPosition(), self.__ServoVertical.getPosition()]

def main():
	Pointer=LaserSystem()

	Pointer.SetPosition(0,0)
	time.sleep(1)
	Pointer.SetPosition(90,90)
	time.sleep(1)
	Tempval=Pointer.Get_Angle()
	print(Tempval[0])
	print(Tempval[1])


if __name__ == '__main__':
	main()