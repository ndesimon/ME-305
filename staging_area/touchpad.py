"""!
@file touchpad.py
@brief Interacts with touchpad to determine ball position and velocity.
@details Creates a Touchpad class. Configures the four pins of the panel
         such that ADC measurements can be read.  
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab2/encoder.py
 
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 03-18-22
"""






#INCLUDE THE SCAN TIME IN HERE!!!!!!!!!!








from pyb import Pin, ADC
from math import pi
from time import ticks_us, ticks_diff
import micropython
from array import array

class Touchpad:
    '''!@brief      Contains methods to obtain values from the touchpad.
        @details    Configures pins to obtain position and velocities of the ball
                    using ADC measurements.
    '''
    
    @micropython.native
    def __init__ (self, xpPin, xmPin, ypPin, ymPin, xwidth, ylength):
        
        '''! @brief Creates the initial setup for the touchpad
             @details Sets up all the pins associated with the touchpad
             @param xpPin A pin used the positive x terminal of the touchpad.
             @param xmPin A pin used the negative x terminal of the touchpad.
             @param ypPin A pin used the positive y terminal of the touchpad.
             @param ymPin A pin used the negative y terminal of the touchpad.
             @param xwidth A value used for the physical width of the pad.
             @param ylength A value used for the physical length of the pad.
        '''
        
        self.xpPin = xpPin
        self.xmPin = xmPin
        self.ypPin = ypPin
        self.ymPin = ymPin
        self.OUT = Pin.OUT_PP
        self.IN = Pin.IN
        self._res = micropython.const(4096)
        self.xscale = xwidth/self._res
        self.yscale = ylength/self._res
        self._half = micropython.const(2)
        self.xc = xwidth/self._half
        self.yc = ylength/self._half
        #initial values of calibration coefficients
        self.Kxx = 1
        self.Kxy = 0
        self.xo = 0
        self.Kyx = 0
        self.Kyy = 1
        self.yo = 0
        self._buf = array('h',25*[0])
        self._freq = micropython.const(200000)
        self._avgdiv = micropython.const(25)

    @micropython.native
    def xScan(self):
        
        '''! @brief Uses ADC measurements for x position.
             @details Configures pins to obtain the ADC measurement of the x position
                      which will be converted to mm.
             @return The value of x position in mm.
        '''
        
        xp = Pin(self.xpPin, self.OUT)
        xp.high()
        
        xm = Pin(self.xmPin, self.OUT)
        xm.low()
        
        yp = Pin(self.ypPin, self.IN)
        
        ym = ADC(Pin(self.ymPin))
        
        ym_rt = ym.read_timed(self._buf, self._freq)
        
        ym_filt = sum(self._buf)/self._avgdiv
    
        self.xADC = ym_filt*self.xscale - self.xc
        return self.xADC
#        self.xADC = ym.read()
        
    @micropython.native
    def yScan(self):
        
        '''! @brief Uses ADC measurements for y position.
             @details Configures pins to obtain the ADC measurement of the y position
                      which will be converted to mm.
             @return The value of y position in mm. 
        '''
        
        yp = Pin(self.ypPin, self.OUT)
        yp.high()
        
        ym = Pin(self.ymPin, self.OUT)
        ym.low()
        
        xp = Pin(self.xpPin, self.IN)
        
        xm = ADC(Pin(self.xmPin))
        
        xm_rt = xm.read_timed(self._buf, self._freq)
        
        xm_filt = sum(self._buf)/self._avgdiv
        
        self.yADC = xm_filt*self.yscale - self.yc
        return self.yADC
#        self.yADC = xm.read()
        
    @micropython.native
    def zScan(self):
        
        '''! @brief Determines if ball is in contact with pad.
             @details Configures the pins to determine if the ball is in current contact
                      or is not on the touchpad.
             @return The value of z
        '''
        
        yp = Pin(self.ypPin, self.OUT)
        yp.high()
        
        xm = Pin(self.xmPin, self.OUT)
        xm.low()
        
        xp = Pin(self.xpPin, self.IN)
        
        ym = ADC(Pin(self.ymPin))
        
        if ym.read() < 4050:
            self.z = 1
        else:
            self.z = 0
        
        return self.z
    
    @micropython.native    
    def XYZ_Scan(self):
        
        '''! @brief Uses all x,y,z scans and combines into one tuple.
             @details Configures the values from x,y,z scan to be inserted into
                      a tuple that can be passed into other modules.
             @return tuple containing x,y,z scan
        '''
        xsc = self.xScan()
        self.zScan()
        ysc = self.yScan()
        self.x = self.Kxx*xsc + self.Kxy*ysc + self.xo
        self.y = self.Kyx*xsc + self.Kyy*ysc + self.yo
        return(self.x, self.y, self.z)
        
    @micropython.native
    def set_cal_coeff(self, Kxx, Kxy, xo, Kyx, Kyy, yo):
        
        '''! @brief Sets values for calibration coefficients.
             @details Calculated values for the calibration coefficients computed
                      in TTask using the matricies.
        '''
        self.Kxx = Kxx
        self.Kxy = Kxy
        self.xo = xo
        self.Kyx = Kyx
        self.Kyy = Kyy
        self.yo = yo

        
if __name__ == '__main__':
    x = Touchpad(Pin.cpu.A7, Pin.cpu.A1, Pin.cpu.A6, Pin.cpu.A0, 176, 100)
    import utime
    n = 0
    t1 = utime.ticks_us()
    while n < 100:
        x.XYZ_Scan()
        n += 1
    t2 = utime.ticks_us()
#    print(t1)
#    print(t2)
    t = utime.ticks_diff(t2, t1)/100
    print(f'Run time for all 3 Scans: {t} microseconds')