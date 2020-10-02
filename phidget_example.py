from Phidget22.Phidget import *
from Phidget22.Devices.RCServo import *
import time

#Declare any event handlers here. These will be called every time the associated event occurs.

def main():
	#Create your Phidget channels
	rcServo0 = RCServo()
	rcServo1 = RCServo()

	#Set addressing parameters to specify which channel to open (if any)
	rcServo0.setChannel(0)
	rcServo1.setChannel(1)

	#Assign any event handlers you need before calling open so that no events are missed.

	#Open your Phidgets and wait for attachment
	rcServo0.openWaitForAttachment(5000)
	rcServo1.openWaitForAttachment(5000)

	#Do stuff with your Phidgets here or in your event handlers.
	rcServo0.setTargetPosition(90)
	rcServo0.setEngaged(True)
	rcServo1.setTargetPosition(90)
	rcServo1.setEngaged(True)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	#Close your Phidgets once the program is done.
	rcServo0.close()
	rcServo1.close()

main()
