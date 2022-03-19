# -*- coding: utf-8 -*-
"""!
@file motor.py
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
from pyb import Pin, Timer

class Motor:
    
    '''!@brief A motor class for one channel of the DRV8847.
        @details Objects of this class can be used to apply PWM to a given
                 DC motor.

    '''
    def __init__ (self, PWM_tim, IN1_pin, IN2_pin, CH_X, CH_Y):
        
        '''!@brief Initializes and returns an object associated with a DC Motor.
            @details Objects of this class should not be instantiated
                     directly. Instead create a DRV8847 object and use
                     that to create Motor objects using the method
                     DRV8847.motor().
        '''
        # Enable pin
#        self.nSLEEP = Pin(Pin.cpu.EN_pin, mode=Pin.OUT_PP)
        
        # Class var PWM_tim is equal to the value of input arg PWM_tim.
        self.PWM_tim = Timer(PWM_tim, freq = 20_000)
        
        # Class vars IN_pin are equal to the values of input args PWM_tim.
        self.IN1_pin = IN1_pin
        self.IN2_pin = IN2_pin

#        # Class var PWM_tim is equal to the value of input arg PWM_tim.
#        self.CH_X = CH_X
#        self.CH_Y = CH_Y
        
        
        self.PWM_tim_CH_X = self.PWM_tim.channel(CH_X, Timer.PWM_INVERTED, pin=self.IN1_pin)
        self.PWM_tim_CH_Y = self.PWM_tim.channel(CH_Y, Timer.PWM_INVERTED, pin=self.IN2_pin)
        
        
        
            
    
    def set_duty (self, duty):        
        '''!@brief Set the PWM duty cycle for the motor channel.
            @details This method sets the duty cycle to be sent
                     to the motor to the given level. Positive values
                     cause effort in one direction, negative values
                     in the opposite direction.
            @param duty A signed number holding the duty
                        27 cycle of the PWM signal sent to the motor
        '''
        
        if duty >= 0:
            self.PWM_tim_CH_X.pulse_width_percent(0)
            self.PWM_tim_CH_Y.pulse_width_percent(duty)
        elif duty < 0:
            self.PWM_tim_CH_X.pulse_width_percent(-duty)
            self.PWM_tim_CH_Y.pulse_width_percent(0)
    
#if __name__ == '__main__':
    # Adjust the following code to write a test program for your motor class. Any
    # code within the if __name__ == '__main__' block will only run when the
    # script is executed as a standalone program. If the script is imported as
    # a module the code block will not run.
    
#    pinB4 = pyb.Pin(pyb.Pin.cpu.B4)
#    pinB5 = pyb.Pin(pyb.Pin.cpu.B5)
#    pinB0 = pyb.Pin(pyb.Pin.cpu.B0)
#    pinB1 = pyb.Pin(pyb.Pin.cpu.B1)
    
    # Create a timer object to use for motor control
   # PWM_tim = Timer(3, freq = 20_000)
    
    # Create a motor driver object and two motor objects. You will need to
    # modify the code to facilitate passing in the pins and timer objects needed
    # to run the motors.
#    motor_1 = Motor(3, Pin.cpu.B4, Pin.cpu.B5, 1, 2)
#    motor_2 = Motor(3, Pin.cpu.B0, Pin.cpu.B1, 3, 4)
    
#    t3ch1 = tim3.channel(1, pyb.Timer.PWM, pin=pinB4)
#    t3ch2 = tim3.channel(2, pyb.Timer.PWM, pin=pinB5)
    
    
    # Enable the motor driver
#    nSLEEP = Pin(Pin.cpu.A15, mode=Pin.OUT_PP)
#    nSLEEP.high()
#    
#    # Set the duty cycle of the first motor to 40 percent
#    print('setting duty to 40')
#    motor_1.set_duty(40)
        
        
        
        
       
#drv = DRV88847()
#mot1 = drv.motor()
#mot2 = drv.motor


#to make it go forward keep In1 H
#make In2 H and L
#
#pwm pin
#
#50% means no motion
## switch between the f and r but need to break first
##USe table to see how PWM applies to output
#
##Step1 get class running first
##mostly done
#
##DRV8847 class
##1 timer with 4 pwm channel
#
#needs each sub title in 3 ex: fault detection
#
##like lab 01 led, use trigger interrupt
##write code that DVR8847 can create objects
#
##motor class done, motor f and r
##possible DVR8847 start
#
##take in code like 123
