"""!
@file DRV8847.py
@brief Interacts with the DRV chip to enable, disable, or trigger faults.
@details Creates a DRV8847 class. Recognizes the built in faults within the DRV
         chip and allows re enabling or disabling when necessary. Instantiates motors. 
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/DRV8847.py
   
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-17-22
"""

from motor import Motor
from pyb import Pin, ExtInt
import time

class DRV8847:
    '''!@brief A motor driver class for the DRV8847 from TI.
        @details Objects of this class can be used to configure the DRV8847
                 motor driver and to create one or more objects of the
                 Motor class which can be used to perform motor
                 control.
                 
    '''

    def __init__ (self, timer, nSLEEP, nFAULT):
        '''!@brief Initializes and returns a DRV8847 object.
            @details Creates a driver, which can control the enabling and disabling of
            the motor.  
            @param timer The value set for which timer to use
            @param nSLEEP Allows the motor to enable or disable
            @param nFAULT Recognizes if a fault occurs within the chip
        '''
        self.timer = timer
        self.nSLEEP = nSLEEP
        self.nFAULT = nFAULT
        self.FaultInt = ExtInt(self.nFAULT, mode=ExtInt.IRQ_FALLING,
                               pull=Pin.PULL_NONE, callback=self.fault_cb)

    def enable (self):
        '''!@brief Brings the DRV8847 out of sleep mode.
            @details Enables DRV8847.  Temporarily disables fault triggering to fix
                     a bug in which the sensor would fault upon enabling.  
        '''        
        self.FaultInt.disable()
        self.nSLEEP.high()
        time.sleep_us(50)
        self.FaultInt.enable()

    def disable (self):
        '''!@brief Puts the DRV8847 in sleep mode.
            @details Disables DRV8847, stopping any motor motion.  
        '''
        print('Disabling motor')
        self.nSLEEP.low()
    
    def fault_cb (self, IRQ_src):
        '''!@brief Callback function to run on fault condition.
            @details If a fault is triggered, this is the function that is called.  
                     This function gets DRV8847 to disable the motors.  
            @param IRQ_src The source of the interrupt req
        '''
        print('Fault detected')
        self.disable()

    def motor (self, InA, InB, ChX, ChY):
        '''!@brief Creates a DC motor object connected to the DRV8847.
            @details Creates an object which the motor class can furth specify.
                     Allows multiple motors to be controlled by just one DRV8847.  
            @param InA The value of Pin A to be passed into the motor module
            @param InB The value of Pin B to be passed into the motor module
            @param ChX The value of Channel X to be passed into the motor module
            @param ChY The value of Channel Y to be passed into the motor module
            @return Motor() An object in which the motor class can further control
        '''
#        self.motor_1 = Motor(self.tim3, Pin.cpu.B4, Pin.cpu.B5, 1, 2)
#        self.motor_2 = Motor(self.tim3, Pin.cpu.B0, Pin.cpu.B1, 3, 4)
        return Motor(self.timer, InA, InB, ChX, ChY)