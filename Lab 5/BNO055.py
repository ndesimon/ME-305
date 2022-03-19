"""!
@file BNO055.py
@brief Interacts with the DRV chip to enable, disable, or trigger faults.
@details Creates a DRV8847 class. Recognizes the built in faults within the DRV
         chip and allows re enabling or disabling when necessary. Instantiates motors. 
         
         See source code:
         https://bitbucket.org/bbartl01/mechatronics-labs/src/master/Lab3/DRV8847.py
   
@author Baxter Bartlett
@author Nick DeSimone
@author Miles Ibarra
@date 03-03-22
"""

from motor5 import Motor
from pyb import Pin, ExtInt, I2C
import time

class BNO055:
    '''!@brief A motor driver class for the DRV8847 from TI.
        @details Objects of this class can be used to configure the DRV8847
                 motor driver and to create one or more objects of the
                 Motor class which can be used to perform motor
                 control.
                 
    '''

    def __init__ (self):
        '''!@brief Initializes and returns a DRV8847 object.
            @details Creates a driver, which can control the enabling and disabling of
            the motor.  
            @param timer The value set for which timer to use
            @param nSLEEP Allows the motor to enable or disable
            @param nFAULT Recognizes if a fault occurs within the chip
        '''
        
        self.i2c = I2C(1, I2C.CONTROLLER)
        # BNO055 Device Address
        self.dev_adr = 0x28
        # Register address for operating mode
        self.opr_mode = 0x3D
        # NDOF Operating Mode corresponds to the number b1100
        self.ndof_mode = 12
        self.cal_byte = 0
        # Initialize in configuration mode
        self.i2c.mem_write(0, self.dev_adr, self.opr_mode)
        self.i2c.mem_write(0x21, self.dev_adr, 0x41)
        self.i2c.mem_write(0x02, self.dev_adr, 0x42)
        self.eulbuf = bytearray(6*[0])
        self.omebuf = bytearray(6*[0])
        

    def change_mode (self, mode):
        '''!@brief Brings the DRV8847 out of sleep mode.
            @details Enables DRV8847.  Temporarily disables fault triggering to fix
                     a bug in which the sensor would fault upon enabling.  
        '''        
        self.i2c.mem_write(mode, self.dev_adr, self.opr_mode)
        
    def get_cal_status (self):
        '''!@brief Brings the DRV8847 out of sleep mode.
            @details Enables DRV8847.  Temporarily disables fault triggering to fix
                     a bug in which the sensor would fault upon enabling.  
        '''        
        self.cal_byte = self.i2c.mem_read(1, self.dev_adr, 0x35)[0]
        mag_stat = self.cal_byte & 0b00000011
        acc_stat = (self.cal_byte & 0b00001100)>>2
        gyr_stat = (self.cal_byte & 0b00110000)>>4
        sys_stat = (self.cal_byte & 0b11000000)>>6
        return ((mag_stat, acc_stat, gyr_stat, sys_stat))
    
    def get_cal_coeff (self, calbuf):
        '''!@brief Brings the DRV8847 out of sleep mode.
            @details Enables DRV8847.  Temporarily disables fault triggering to fix
                     a bug in which the sensor would fault upon enabling.  
        '''        
        self.i2c.mem_read(calbuf, self.dev_adr, 0x55)
        return calbuf
    
    def set_cal_coeff (self, setbuf):
        '''!@brief Brings the DRV8847 out of sleep mode.
            @details Enables DRV8847.  Temporarily disables fault triggering to fix
                     a bug in which the sensor would fault upon enabling.  
        '''        
        self.i2c.mem_write(setbuf, self.dev_adr, 0x55)

        
    def get_euler (self):
        '''!@brief Brings the DRV8847 out of sleep mode.
            @details Enables DRV8847.  Temporarily disables fault triggering to fix
                     a bug in which the sensor would fault upon enabling.  
        '''        
        self.i2c.mem_read(self.eulbuf, self.dev_adr, 0x1A)
        head = (self.eulbuf[1]<<8)|self.eulbuf[0]
        roll = (self.eulbuf[3]<<8)|self.eulbuf[2]
        pitch = (self.eulbuf[5]<<8)|self.eulbuf[4]
        if head > 32767:
            head -= 65536
        if roll > 32767:
            roll -= 65536
        if pitch > 32767:
            pitch -= 65536
        return (-head/16,-roll/16,-pitch/16) #z,y,x
        
    def get_omega (self):
        '''!@brief Brings the DRV8847 out of sleep mode.
            @details Enables DRV8847.  Temporarily disables fault triggering to fix
                     a bug in which the sensor would fault upon enabling.  
        '''        
        self.i2c.mem_read(self.omebuf, self.dev_adr, 0x14)
        gyr_x = (self.omebuf[1]<<8)|self.omebuf[0]
        gyr_y = (self.omebuf[3]<<8)|self.omebuf[2]
        gyr_z = (self.omebuf[5]<<8)|self.omebuf[4]
        if gyr_x > 32767:
            gyr_x -= 65536
        if gyr_y > 32767:
            gyr_y -= 65536
        if gyr_z > 32767:
            gyr_z -= 65536
        return (gyr_x/16,gyr_y/16,gyr_z/16) #x,y,z