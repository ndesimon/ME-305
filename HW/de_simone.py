'''
@file       de_simone.py
@brief      Plots data read from given file
@details    Takes data from a csv file named eric.csv and plots any float/int
            data using matplotlib
@author     Nick De Simone
@date       1/14/2021
'''

from matplotlib import pyplot

# Lists to contain x and y float values
x = []
y = []

def readFile(filename='eric.csv', rdFlag=True, dbFlag=True, runs=1):
    ''' @brief    Reads file and splits its values into x- and y-lists
         @details Takes user-defined file then reads and cleans its contents 
                  into x- and y-lists of float values to be plotted by 
                  plotFile function
         @param   filename Specify file to read
         @param   rdFlag   Start/stop file reading
         @param   dbFlag   Start/stop debug comments
    '''
    if dbFlag:
        print('Reading Start')
    
    ## Open file for reading, evaluate for int/float data, add into x&y 
    with open(filename, 'r', encoding="utf-8") as file:
        
        # Continue file read until false
        while rdFlag == True:
            
            # Read each row of given file as an individual string
            row = file.readline()
           
            # Strip empty chars from front/back of row, split columns into 
            # list of individual strings 
            dataList = row.strip().split(',')
            
            # Proceed if 2 or more column values in dataList
            if len(dataList) > 1:
                try:                    
                    # Evaluate 1&2 data points in each row for validity
                    x_vals = dataList[0].strip().split(',')
                    y_vals = dataList[1].strip().split(',')                
                    
                    x_p = float(x_vals[0])
                    y_p = float(y_vals[0])
                    
                    # Add data to x&y if both values are valid
                    if isinstance(x_p, float) and isinstance(y_p, float):
                        x.append(x_p)                       
                        y.append(y_p)
                
                # ValueError will trigger after reading letters
                except ValueError:   
                    pass
                            
            # Flag Condn: Empty row in file indicates end of file
            if row == '':
                # Stop file read
                rdFlag = False
            
            # Debug comments
            if dbFlag:           
                print('row'+str(runs)+' = ' + row)
                print('data'+str(runs)+' = ' + str(dataList))
                print('x'+str(runs)+' = ' + str(x))
                print('y'+str(runs)+' = ' + str(y))
                runs+=1
                if row == '':
                    if dbFlag:
                        print('Reading Done')
            else:
                pass
            
        return x and y
                

def plotFile(x, y, dbFlag=True):
    ''' @brief   Plots x- and y-data
        @details Plots x- and y- data points from lists generated by readFile 
                 function
        @param   x      List containing x-data points
        @param   y      List containing y-data points
        @param   dbFlag Start/stop debug comments
    '''
    if dbFlag:
        print('Plotting Start')
    pyplot.plot(x, y)
    pyplot.xlabel("Arthur's Speed [m/s]")
    pyplot.ylabel("Coconut Frequency [knocks/sec]")
    pyplot.show()
    if dbFlag:
        print('Plotting Done')

if __name__ == '__main__': 
    # Optional user input for files other than eric.csv
    # Note: must pass 'filename' into readFile function call
    # Uncomment line below for optional input
    # filename = input('Enter filename: ')
    print('Reading and plotting file...')
    readFile()
    plotFile(x,y)
    print('Done')
