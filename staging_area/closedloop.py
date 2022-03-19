"""!
@file closedloop.py
@brief Interacts with the Nucleo to calculate the values of gain and duty cycle
@details Creates a Closed Loop class. Assigns the values of gain and calculates the
         duty cycle via the class methods.
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/motor.py
   
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-24-22
"""
from pyb import Timer

class ClosedLoop:
    
    '''!@brief A Closed Loop class for one motor of the Nucleo.
        @details Objects of this class can be used to apply PWM to a given
                 DC motor.

    '''
    def __init__ (self, Kp, Ki, setpoint, sathigh, satlow):
        
        '''!@brief Creates the initial setup for the closed loop driver
            @details Objects of this class should not be instantiated
                     directly. Instead create a Closed Loop object and use
                     that to create Motor objects using the methods
                     within this class.
            @param Kp Placeholder for the gain Kp of the motor
            @param Ki Placeholder for the gain Ki of the motor
            @param setpoint Placeholder for the reference velocity inputted from yshare
            @param sathigh Placeholder for the max saturation value
            @param satlow Placeholder for the min saturation value
        '''
        
        # Class vars IN_pin are equal to the values of input args PWM_tim.
        self.Kp = Kp
        self.Ki = Ki
        self.reference = setpoint
        self.sathigh = sathigh
        self.satlow = satlow
        self.actuation = 0
        self.reference = 0
        self.error = 0
        self.error_sum = 0
    
    def run(self, measured, deltaTime):
        
        '''! @brief Computes the actuation signal sent to the motor
             @details Based on the difference between the desired setpoint 
                      and motor velocity
             @param measured Passed value of the measured velocity of the motor
             @param deltaTime Difference between encoder readings
                        
        '''
        
        self.error = self.reference - measured
        self.error_sum += self.error*(deltaTime/1E6) 
        self.actuation = self.Kp*((self.error)+(self.Ki)*self.error_sum)
        if self.actuation > self.sathigh:
            self.actuation = self.sathigh
        elif self.actuation < self.satlow:
            self.actuation = self.satlow
        return self.actuation
        
    def set_Gain (self, Kp, Ki):        
        '''!@brief Set the gain for the motor.
            @details This method sets the gain to be sent
                     to the motor with the value for Kp or Ki. 
            @param Kp gain value for proportional control
            @param Ki gain value for integral control
        '''
        self.Kp = Kp
        self.Ki = Ki

    def get_Kp (self):        
        '''!@brief Return the value of Kp
            @return Gives the proportional gain value Kp
        '''
        return self.Kp
        
    def set_Reference (self, reference):        
        '''!@brief Set the reference veloctiy for the calculations.
            @details This method sets the reference velocity used for the calculations
                     to find the duty cycle 
            @param reference velocity passed from the setpoint 
                       
        '''
        self.reference = reference
    
    def get_Reference (self):        
        '''!@brief Returns the reference velocity
            @return Gives the value of the reference velocity
        '''
        return self.reference
    
    def get_Actuation (self):
        '''!@brief Returns the value for actuation.
            @return Gives the actuation value calculated.
        
        '''
        return self.actuation
            
        
            