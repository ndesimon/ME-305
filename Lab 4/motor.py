"""!
@file motor.py
@brief Interacts with the Nucleo to activate the pins and channels desired for the motor.
@details Creates a motor class. Assigns the motor pins and channels values which can
         vary based on input
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/motor.py
   
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-17-22
"""
from pyb import Timer

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
            @param PWM_tim Placeholder for the timer of the motor
            @param IN1_pin Placeholder for the first pin to be passed in
            @param IN2_pin Placeholder for the second pin to be passed in 
            @param CH_X Placeholder for the first channel of the timer passed in
            @param CH_Y Placeholder for the second channel of the timer passed in
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