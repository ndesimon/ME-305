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
@date 02-03-22
"""

import pyb

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
        self.position = self.tim.counter()
        self.previousCount = self.tim.counter()
    
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
        self.delta = self.currentCount - self.previousCount
        if self.delta > 65536/2:
            self.delta -= 65536
        elif self.delta < -65536/2:
            self.delta += 65536
        else:
            pass
        self.position += self.delta
        self.previousCount = self.currentCount
        
        
    def get_position(self):
        
        '''! @brief Creates the method for finding the position.
             @details Collects the position computed in the update method.
             @return The value of position is given
        '''
        
        return self.position
    
    def zero(self):
        
        '''! @brief Zeros the position of the encoder.
             @details Sets the position variable equal to zero.  Also sets the
                      previous count equal to the current value of the timer to
                      account for the time to zero.  
        '''
        self.position = 0
        self.previousCount = self.tim.counter()
        print('Setting position back to zero')
    
    def get_delta(self):
        
        '''! @brief Creates the method for obtaining Delta
             @details Retrieves the delta computed in the update method.  
             @return The value of Delta is given
            
        '''
        
        return self.delta
    
if __name__ == '__main__':
    
    ## @brief creates a variable called ENC1
    #  @details Variable uses the inputs to be inserted into the Encoder class
    #
    ENC1 = Encoder(pyb.Pin.cpu.B6, pyb.Pin.cpu.B7, 4)
    while True:
        try:
            ENC1.zero()
        except KeyboardInterrupt:
            break
        
