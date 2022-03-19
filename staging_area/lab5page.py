'''! @page lab5page.py Lab 5: I2C and Inertial Measurement Unit
    @tableofcontents
    Balance a platform using IMU data and closed-loop motor control.
    
    @section sec_intro5 Introduction
    Lab 5 incorporates new task and driver files that use the I2C 
    communication protocol to read angular position and 
    velocity data from an inertial measurement unit, the Bosch BNO055, that is
    attached to our platform. This data is implemented as feedback in the 
    closed-loop controller of Lab 4, with the goal of stabilizing the platform.
    
    Platform stability is achieved when the BNO055 senses zero degrees for the 
    "pitch" and "roll" Euler angles, which correspond to our platform's x- and 
    y-axes, respectively. 
    Note that, in order to read acceptable values from the IMU,
    a calibration procedure is necessary. This procedure is prompted in the
    User Interface when a ".txt" file is not available on the host Nucleo MCU.
    Upon completion of the calibration procedure, the calibration coefficients, 
    which are read from their corresponding register address on the BNO, are
    written to a ".txt" file and saved on the MCU for subsequent runs.   
    Please see @ref sec_files5 for descriptions of our project files.
    
    @section sec_files5 Project Files
    
    @subsection sub_main5 Main File
    The main file instantiates our task- and class-files as objects to be run
    asynchronously. Note the task diagram below for information regarding file 
    communication and run frequency. See @ref main.py for more information. 
    @image html taskDiagram4.png width=600px
    
    @subsection sub_utask5 User Task
    The user interface is written as a generator function that prints to a 
    terminal emulator. It is able to read a user's keyboard presses as 
    controller and IMU commands, such as printing the IMU's current Euler
    angles and angular velocities or accepting user-input 
    controller gain values, over the USB virtual comm port. 
    See @ref UTask5.py for more information, and the figure below for the User
    Task's state transition diagram.
    @image html term_ui_task_std.png width=600px
    
    
    @subsection sub_imutask5 IMU Task
    The IMU task calls methods of the BNO055 driver class, @ref BNO055.py,
    to read IMU data and prompt user calibration when necessary.
    See @ref IMUTask.py for more information and the figure below 
    for the IMU Task's state transition diagram.
    @image html imutask_std.png width=500px  
    
    @subsection sub_ctask5 Controller Task
    The controller task communicates controller gain values Kp, Kd, and Ki, 
    angular setpoints, and Euler angle/angular velocity data (read
    from the IMU device) to our closed-loop driver, @ref closedloop5.py. This
    task is also responsible for sending duty cycles to the motor task, 
    which enables motor actuation according to the actuation signal computed 
    in the closed-loop driver.  
    See @ref CTask5.py for more information and the 
    figure below for the Controller Task's state transition diagram.
    @image html term_ctask_std.png width=500px

    @subsection sub_mtask5 Motor Task
    The motor task sends duty cycles, which are determined as the actuation
    signal of the closed-loop controller, to their respective motors,
    either Motor 1 or Motor 2. 
    See @ref MTask5.py for more information and the figure below 
    for the Motor Task's state transition diagram.
    @image html MTaskSTD3.png width=500px    

    @subsection sub_imu5 BNO055 Driver
    This driver class handles I2C communication with the BNO055 IMU device. 
    Associated methods include reading Euler angle and angular velocity data
    from the BNO, as well as reading/writing calibration coefficients
    according to the device's current calibration status.
    See @ref BNO055.py for more information.

    @subsection sub_clc5 Closed-Loop Control Driver
    The closed-loop driver is a class file that computes actuation signals 
    according to user-defined controller gains Kp, Ki, and Kd, desired 
    setpoint, and, for use with the IMU device, the IMU's 
    Euler angle and angular velocity data. For the self-balancing platform, the
    angular setpoint defaults to a 0 degree reference angle, such that the 
    controller attempts to reach a level position. The controller is able to
    perform proportional, integral, and/or derivative control.
    See @ref closedloop5.py for more information.

    @subsection sub_mot5 Motor Driver
    The motor driver is a class file that instantiates pin, timer, and timer 
    channel objects for the designated motor's PWM channels, which are 
    configured as inverted PWM channels. The driver also has a method to set
    motor duty cycles as a pulse width percent, whose value is passed in as the 
    closed-loop controller's actuation signal.
    See @ref motor5.py for more information.
    
    @subsection sub_sha5 Shares Class
    The shares class file allows variables to be created, read from, and 
    written to multiple files.
    See @ref shares.py for more information.
    
'''