"""!
@file closedloop5.py
@brief Module for computing actuation.
@details Creates a class that computes actuation via closed loop control.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab4/closedloop.py
   
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 03-18-22
"""

class ClosedLoop:
    
    '''!@brief Enables closed loop control
        @details Uses error to compute the gain necessary for closed loop control

    '''
    def __init__ (self, Kp, Kd, Ki, setpoint, sathigh, satlow):
        
        '''!@brief Creates the initial setup for the closed loop driver
            @details Objects of this class should not be instantiated
                     directly. Instead create a Closed Loop object and use
                     that to create Motor objects using the methods
                     within this class.
            @param Kp Placeholder for the gain Kp of the motor
            @param Kd Placeholder for the gain Kd of the motor
            @param Ki Placeholder for the gain Ki of the motor
            @param setpoint Placeholder for the reference velocity inputted from yShare
            @param sathigh Placeholder for the maximum saturation value
            @param satlow Placeholder for the minimum saturation value
        '''
        
        # Class vars IN_pin are equal to the values of input args PWM_tim.
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.reference = setpoint
        self.sathigh = sathigh
        self.satlow = satlow
        self.actuation = 0
        self.reference = 0
        self.error = 0
        self.position_sum = 0
        self.wind_pos = 0
        self.wind_neg = 0
        self.Ti = 0
        self.TiTs = 0
    
    def run(self, position, velocity, ref, loop, zflag):
        
        '''! @brief Computes the actuation signal sent to the motor
             @details Based on the position, velocity, and reference
                      measured values from the IMU.
             @param position calculates the angular position
             @param velocity calculates the angular velocity 
             @param ref calculates the reference angle
             @param loop sets a value for loop to be used as a flag
             @param zflag sets a value for zflag to be used as a flag
                        
        '''
        #self.output = Kp*(ref_val-meas_val)-Kd*meas_vel
        #position contains theta and x
        #velocity contains x_dot and theta_dot
        self.position = position
        self.position_sum += self.position
        self.vel = velocity
        self.reference = ref
        if self.Ki != 0:
            self.Ti = self.Kp/self.Ki
        elif self.Ki == 0:
            self.Ti = 0
        if self.Ti != 0:
            self.TsTi = 10/self.Ti
        elif self.Ti == 0:
            self.TsTi = 0        
        self.actuation = self.Kp*(self.reference-self.position) 
        - self.Kd*self.vel + ((self.TsTi*self.position_sum) 
                              - (self.wind_pos -self.wind_neg))
        #- self.Ki*self.position_sum/10
        if loop == 0:
            self.wind_pos = self.actuation
        elif loop == 1:
            self.actuation += 5
        if self.actuation > self.sathigh:
            self.actuation = self.sathigh
        elif self.actuation < self.satlow:
            self.actuation = self.satlow
        
        if loop == 0:
            if zflag == 0:
                self.actuation = 0
            self.wind_neg = self.actuation
        
        return -self.actuation
        
    def set_Gain (self, Kp, Kd, Ki):        
        '''!@brief Set the gain for the motor.
            @details This method sets the gain to be sent
                     to the motor with the value for Kp or Ki. 
            @param Kp gain value for proportional control
            @param Kd gain value for derivative control
        '''
        self.Kp = Kp
        self.Kd = Kd
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