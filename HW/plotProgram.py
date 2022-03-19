"""!
@file       plotProgram.py
@details    Takes data from a csv file named eric.csv and plots the data using 
            matplotlib.
@author:    Nick De Simone
"""

from matplotlib import pyplot

# x and y int/float values
x = []
y = []

class plotProgram:
    ''' @brief      Plots data from csv file
        @details    Opens, reads, and plots valid data from a csv file and 
                    discards invalid data
    '''   

    def __init__(self, filename='eric.csv'):
        ''' @brief
            @details
            @param encoder_num Encoder defined by main as either the 1 or 2 
                                physical encoder
            @param req_period Period at which encoder task will run
        '''
    ## Start/Stop file reading
    self.rdngFlag = True
    
    ## On/Off debug comments
    self.sdbgFlag = True
    self.runs = 1
    self.filename = filename
    
    def readFile(self, filename='eric.csv'):
        ## Open file for reading, evaluate for int/float data, & add into x&y 
        with open(self.filename, 'r') as file:
            
            # Continue file read until false
            while self.rdngFlag == True:
                
                # Read each row of given file as an individual string
                row = file.readline()
               
                # Strip empty chars from front/back of row, split columns into 
                # list of individual strings 
                dataList = row.strip().split(',')
                
                # Proceed if 2 or more column values in dataList
                if len(dataList) > 1:
                    # Add data to x&y if both values are digits
                    x_point = dataList[0].strip().split(',')
                    y_point = dataList[1].strip().split(',')                
                    
                    if x_point[0].isdigit() and y_point[0].isdigit():
                        x.append(float(x_point[0]))                       
                        y.append(float(y_point[0]))
                        
                        
                if self.dbgFlag:           
                    print('run = '+ str(runs))
                    print('row = ' + row)
                    print('data = ' + str(dataList))
                    print('x = ' + str(x))
                    print('y = ' + str(y))
                    self.runs+=1
                                
                # Flag Condn: Empty row in file indicates end of file
                if row == '':
                    # Stop file read
                    rdngFlag = False
                    
                else:
                    pass

# Run program
if __name__ == '__main__':
    
    ## Open file for reading, evaluate for int/float data, & add into x&y 
    with open('eric1.csv', 'r') as file:
        
        # Continue file read until false
        while rdngFlag == True:
            
            # Read each row of given file as an individual string
            row = file.readline()
           
            # Strip empty chars from front/back of row, split columns into 
            # list of individual strings 
            dataList = row.strip().split(',')
            
            # Proceed if 2 or more column values in dataList
            if len(dataList) > 1:
                # Add data to x&y if both values are digits
                x_point = dataList[0].strip().split(',')
                y_point = dataList[1].strip().split(',')                
                
                if x_point[0].isdigit() and y_point[0].isdigit():
                    x.append(x_point[0])                       
                    y.append(y_point[0])
                    
                    
            if dbgFlag:           
                print('run = '+ str(runs))
                print('row = ' + row)
                print('data = ' + str(dataList))
                print('x = ' + str(x))
                print('y = ' + str(y))
                runs+=1
                            
            # Flag Condn: Empty row in file indicates end of file
            if row == '':
                # Stop file read
                rdngFlag = False
                
            else:
                pass

            
            
            
            
            
            
#             data.append(row.strip().split(','))
#     # Add values from data list into x and y lists
#     for line in data:       
#         print(line)
#         # Check every line for >= 2 value entries
#         if(len(line) > 1):
#             # Check that values in lines are acceptable (numbers)
#             for i in line:
#                 if i.isdigit():
#                     # Add accepted values into x&y lists
#                     x.append(line[0])
#                     y.append(line[1])
#                 # Remove incorrect values
# #                else:
#  #                   list.remove()