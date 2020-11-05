
from Phidget22.Phidget import *
from Phidget22.Devices.RCServo import *
import time


class LaserSystem:
	def __init__(self):
		self.__ServoVertical= RCServo()
		self.__ServoHorizontal= RCServo()
		self.__ServoHorizontal.setChannel(0)
		self.__ServoVertical.setChannel(1)
		self.__ServoVertical.openWaitForAttachment(5000)
		self.__ServoHorizontal.openWaitForAttachment(5000)


	def SetPosition(self,HorizontalAngle,VerticalAngle):
		self.__ServoVertical.setTargetPosition(VerticalAngle)
		self.__ServoHorizontal.setTargetPosition(HorizontalAngle)
		self.__ServoVertical.setEngaged(True)
		self.__ServoHorizontal.setEngaged(True)
		while int(self.__ServoHorizontal.getPosition()) !=  int(HorizontalAngle) or int(self.__ServoVertical.getPosition()) !=  int(VerticalAngle):
			#print(int(CurrentServo.getPosition()))
			#print(int(CurrentServo.getTargetPosition()))
			time.sleep(.1)

	
	def Get_TargetPosition(self)
		return[self.__ServoHorizontal.getTargetPosition(), self.__ServoVertical.getTargetPosition()]


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