# -*- coding: utf-8 -*-
"""!
@file DRV8847.py
@brief Creates the UserInterface of the program
@details The User Interface lists all possible quantities and ways that the user
         can interact with the encoder.
         The state transition diagram for this task is depicted below:
         @image html UTaskSTD.png width=500px
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab2/lab2_UTask.py
   
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
        '''
        self.timer = timer
        self.nSLEEP = nSLEEP
        self.nFAULT = nFAULT
        self.FaultInt = ExtInt(self.nFAULT, mode=ExtInt.IRQ_FALLING,
                               pull=Pin.PULL_NONE, callback=self.fault_cb)

    def enable (self):
        '''!@brief Brings the DRV8847 out of sleep mode.
        '''
        print('Enabling motor') #put in task BB
        self.FaultInt.disable()
        self.nSLEEP.high()
        time.sleep_us(50)
        self.FaultInt.enable()

    def disable (self):
        '''!@brief Puts the DRV8847 in sleep mode.
        '''
        print('Disabling motor') #put in task BB
        self.nSLEEP.low()
    
    def fault_cb (self, IRQ_src):
        '''!@brief Callback function to run on fault condition.
            @param IRQ_src The source of the interrupt req
        '''
        print('Fault detected') #put in task BB
        self.disable()

    def motor (self, InA, InB, ChX, ChY):
        '''!@brief Creates a DC motor object connected to the DRV8847.
            @return An object of class Motor
        '''
#        self.motor_1 = Motor(self.tim3, Pin.cpu.B4, Pin.cpu.B5, 1, 2)
#        self.motor_2 = Motor(self.tim3, Pin.cpu.B0, Pin.cpu.B1, 3, 4)
        return Motor(self.timer, InA, InB, ChX, ChY)

    
if __name__ == '__main__':
    # Adjust the following code to write a test program for your motor class. Any
    # code within the if __name__ == '__main__' block will only run when the
    # script is executed as a standalone program. If the script is imported as
    # a module the code block will not run.
    
    
    # Create a motor driver object and two motor objects. You will need to
    # modify the code to facilitate passing in the pins and timer objects needed
    # to run the motors.
    motor_drv = DRV8847(3, Pin(Pin.cpu.A15, mode=Pin.OUT_PP), Pin(Pin.cpu.B2, mode=Pin.OUT_PP))
    motor_1 = motor_drv.motor(Pin.cpu.B4, Pin.cpu.B5, 1, 2)
    motor_2 = motor_drv.motor(Pin.cpu.B0, Pin.cpu.B1, 3, 4)
    
    #eventually put all in main instead of here BB
    
    # Enable the motor driver
    motor_drv.enable()
    
    # Set the duty cycle of the first motor to 40 percent and the duty cycle of
    # the second motor to 60 percent
#    motor_1.set_duty(40)
#    motor_2.set_duty(60)

