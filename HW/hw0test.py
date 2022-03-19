"""!
@file       plotProgram.py
@details    Takes data from a csv file named eric.csv and plots the data using 
            matplotlib.
@author:    Nick De Simone
"""

from matplotlib import pyplot

# x and y int/float values
global x
x = []
global y
y = []

def readFile(filename='eric1.csv', rdngFlag = True, dbgFlag = True, runs = 1):
    """! @brief   Encoder Driver to manipulate physical encoders
        @details Constructs encoder objects by linking specified
                 encoder numbers to corresponding Nucleo pins
        @param   filename Specify file to read
        @param   rdngFlag Continue file read until false
        @param   dbgFlag
        @param   runs
    """
    print('Reading Start')
    ## Open file for reading, evaluate for int/float data, & add into x&y 
    with open(filename, 'r') as file:
        
        # Continue file read until false
        while rdngFlag == True:
            
            # Read each row of given file as an individual string
            row = file.readline()
           
            # Strip empty chars from front/back of row, split columns into 
            # list of individual strings 
            dataList = row.strip().split(',')
            
            # Proceed if 2 or more column values in dataList
            if len(dataList) > 1:
                try:                    
                    x_vals = dataList[0].strip().split(',')
                    y_vals = dataList[1].strip().split(',')                
                    
                    x_p = float(x_vals[0])
                    y_p = float(y_vals[0])
                    
                    # Add data to x&y if both values are valid
                    if isinstance(x_p, float) and isinstance(y_p, float):
                        x.append(x_p)                       
                        y.append(y_p)
                except ValueError:   
                    pass
            
            if dbgFlag:           
                print('run = '+ str(runs))
                print('row'+str(runs)+' = ' + row)
                print('data'+str(runs)+' = ' + str(dataList))
                print('x'+str(runs)+' = ' + str(x))
                print('y'+str(runs)+' = ' + str(y))
                runs+=1
                            
            # Flag Condn: Empty row in file indicates end of file
            if row == '':
                # Stop file read
                rdngFlag = False
                print('Reading Done')
                
            else:
                pass

def plotFile():
    """! @brief   Encoder Driver to manipulate physical encoders
         @details Constructs encoder objects by linking specified
                  encoder numbers to corresponding Nucleo pins
         @param   encoder_num Specify Encoder 1 or 2
    """
    pyplot.plot(x, y)
    pyplot.xlabel('X-Data')
    pyplot.ylabel('Y-Data')
    pyplot.show()

# Run program
if __name__ == '__main__': 
    readFile()
    plotFile()
    # ## Open file for reading, evaluate for int/float data, & add into x&y 
    # with open('eric1.csv', 'r') as file:
        
    #     # Continue file read until false
    #     while rdngFlag == True:
            
    #         # Read each row of given file as an individual string
    #         row = file.readline()
           
    #         # Strip empty chars from front/back of row, split columns into 
    #         # list of individual strings 
    #         dataList = row.strip().split(',')
            
    #         # Proceed if 2 or more column values in dataList
    #         if len(dataList) > 1:
    #             # Add data to x&y if both values are digits
    #             x_point = dataList[0].strip().split(',')
    #             y_point = dataList[1].strip().split(',')                
                
    #             if x_point[0].isdigit() and y_point[0].isdigit():
    #                 x.append(x_point[0])                       
    #                 y.append(y_point[0])
                    
                    
    #         if dbgFlag:           
    #             print('run = '+ str(runs))
    #             print('row = ' + row)
    #             print('data = ' + str(dataList))
    #             print('x = ' + str(x))
    #             print('y = ' + str(y))
    #             runs+=1
                            
    #         # Flag Condn: Empty row in file indicates end of file
    #         if row == '':
    #             # Stop file read
    #             rdngFlag = False
                
    #         else:
    #             pass

            
            
            
            
            
            
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