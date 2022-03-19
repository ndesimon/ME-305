"""!
@file encoder.py
@brief Interacts with encoder attached to Nucleo to determine position.
@details Creates an encoder class.  Interacts with encoder by creating a 16-bit
         counter which is used to determine the position.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab2/encoder.py
 
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 02-17-22
"""

import pyb
from math import pi
from time import ticks_us, ticks_diff 

class Encoder:
    '''!@brief      Contains methods to obtain specific data from encoder.
        @details    Creates timers used to obtain the position, delta, and to 
                    zero the encoder.
    '''
    def __init__ (self, pinB6, pinB7, tim4):
        
        '''! @brief Creates the initial setup for the encoder
             @details Sets up all channels with the Nucleo
             @param pinB6 A pin used by the Nucleo for the encoder
             @param pinB7 A pin used by the Nucleo for the encoder
             @param tim4 The timer used for this specific encoder
        '''
        
        self.tim = pyb.Timer(tim4, prescaler=0, period=0xFFFF)
        self.tim.channel(1, pyb.Timer.ENC_AB, pin=pinB6)
        self.tim.channel(2, pyb.Timer.ENC_AB, pin=pinB7)
        self.position = self.tim.counter()*((2*pi)/4000) # Starting position in [rad]
        self.previousCount = self.tim.counter()
        self.previousTime = ticks_us()
    
    def update(self):
        
        '''! @brief Constantly updates the counter that tracks position.
             @details The position is tracked with a 16-bit counter.  To prevent
                      the counter from overflowing, a change, or delta between
                      previous counts is computed.  If the magnitude of the delta 
                      is larger than half of the maximum count (indicating that  
                      the counter reset), the delta is corrected such that the reset 
                      isn't seen.  Adding up all the deltas gives the current position.  
        '''
        
        self.currentCount = self.tim.counter()
        self.currentTime = ticks_us()
        self.delta = (self.currentCount - self.previousCount) 
        self.deltaTime = ticks_diff(self.currentTime,self.previousTime)
        if self.delta > 32767:
            self.delta -= 65536
        elif self.delta < -32767:
            self.delta += 65536
        else:
            pass
        # convert diff in ticks to delta in [rad]
        self.delta = -self.delta*((2*pi)/4000)
        # Update position in [rad]
        self.position += self.delta 
        # Velocity in [rad/s]
        self.vel = self.delta/(self.deltaTime*1E-6)
        # Iterate count and time counts for next update call
        self.previousCount = self.currentCount
        self.previousTime = self.currentTime
        
        
    def get_position(self):
        
        '''! @brief Creates the method for finding the position.
             @details Collects the position computed in the update method.
             @return The value of position is given
        '''
        # Encoder position in [rad]
        return self.position
    
    def zero(self):
        
        '''! @brief Zeros the position of the encoder.
             @details Sets the position variable equal to zero.  Also sets the
                      previous count equal to the current value of the timer to
                      account for the time to zero.  
        '''
        self.position = 0
        self.previousCount = self.tim.counter()
    
    def get_delta(self):
        
        '''! @brief Creates the method for obtaining Delta
             @details Retrieves the delta computed in the update method.  
             @return The value of Delta is given
            
        '''
        
        return self.delta

    def get_vel(self):
        
        '''! @brief Method for obtaining velocity
             @details Retrieves the velocity computed in the update method.  
             @return The value of Velocity is given
            
        '''
        
        return self.vel
    
    def get_deltaTime(self):
        
        '''! @brief Method for obtaining velocity
             @details Retrieves the velocity computed in the update method.  
             @return The value of Velocity is given
            
        '''
        
        return self.deltaTime