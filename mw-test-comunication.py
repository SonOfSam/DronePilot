import time
import datetime
import csv
import threading
from math import *
from modules.utils import *
from modules.pyMultiwii import MultiWii
import modules.UDPserver as udp


#roll, pitch, yaw, throttle
rcCMD = [1500,1500,1500,1000]

vehicle = MultiWii("COM3")


def control():
    global vehicle
    global rcCMD

    while True:
        if udp.active:
            print "UDP is active"
            break
        else:
            print "Waiting for UDP server"
        time.sleep(0.5)
        
    try:

        while True:
            for x in udp.message:
                print x
        
            rcCMD[0] = udp.message[0]
            rcCMD[1] = udp.message[1]
            rcCMD[2] = udp.message[2]
            rcCMD[3] = udp.message[3]

            vehicle.getData(MultiWii.ATTITUDE)
        
            for key, data in vehicle.attitude.items():
                print (key,data)    

            vehicle.getData(MultiWii.RC)

            for key, data in vehicle.rcChannels.items():
                print (key,data)    

            vehicle.sendCMD(8, MultiWii.SET_RAW_RC, rcCMD)

            time.sleep(1)
    
    except Exception, error:
        print "Error in control thread: " + str(error)

if __name__ == "__main__":
    try:
        logThread = threading.Thread(target=control)
        logThread.daemon = True
        logThread.start()
        udp.startTwisted()
    except Exception, error:
        print  "Error on main" + str(error)
    except KeyboardInterrupt:
        print "Keyboard Interrupt, exiting."
        exit()