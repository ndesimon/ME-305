"""
@file    IMU_driver.py
@brief   Driver for the BNO055 Device, including various reads/writes
@details Allows for interaction with the BNO055 IMU, including calibration methods
         and Euler methods
                  
         See source code here: 
             https://bitbucket.org/ndesimon/me405_labs/src/master/Lab%200x05/IMU_driver.py
             
         See short demonstration video here:

@author         Tyler McCue, Nick De Simone
@date           11/9/21
@copyright      License Info Here
"""
from pyb import I2C

class IMU_Driver:
    ''' @brief        Read and write with BNO055
        @details
    '''

    def __init__(self, id=0x28):
        ''' @brief
            @details
            @param 
        '''
        self.i2c = I2C(1)
        self.i2c = I2C(1, I2C.MASTER)
        self.buff = bytearray()
        self.id = id
        
        ## mode = dictionary of mode values
        # Mode Value: Decimal Value
        # return decimal value after specifying mode value
        self.mode = {"ACCONLY": 1,
        "MAGONLY": 2,
        "GYROONLY": 3,
        "ACCMAG": 4,
        "ACCGYRO": 5,
        "MAGGYRO": 6,
        "AMG": 7,
        "IMU": 8,
        "COMPASS": 9,
        "NDOF_FMC_OFF": 11,
        "NDOF": 12}
        
    def change_mode(self, mode_value):
        ''' @brief      Change operating mode of IMU
            @details    Writes specified operating mode to appropriate device/register address
            @param mode_value Name of desired operating mode as a string
            @return     none
        '''
        self.i2c.mem_write(self.mode.get(mode_value), self.id, 0x3D)
        
    def get_calibration_status(self):
        ''' @brief      Read current calibration status
            @details    Reads from appropriate register address
            @return     Calibration Status
        '''
        self.i2c.mem_read(8,40,35)
    
    def get_calibration_coeffs(self):
        ''' @brief      Read current calibration coefficients
            @details    Reads from appropriate register address into a bytearray
            @return     buff
        '''
        ## buff = bytearray of 22 calibration coefficients
        buff = bytearray(22)
        return self.i2c.mem_read(buff,40,55)
    
    def write_calibration_coeffs(self, b_buffer):
        ''' @brief      Writes specified calibration coefficients to the BNO055
            @details    Writes a bytearray of coeff values to appropriate register address
            @param b_buffer bytearray of desired calibration coefficients
            @return     none
        '''
        self.i2c.mem_write(b_buffer,40,55)

        
    

    


