'''! @page labtermpage.py Term Project: Ball-Balancing Platform
    @tableofcontents
    Balance ball on top of rotating resistive touch panel.
    
    @section sec_introT Introduction
    For our ME 305 Term Project, our team attempted to balance a steel ball
    on top of a rotating platform. This project involved reading from a 
    resistive touch panel (upon which the ball was placed) and an IMU device
    in order to perform cascaded closed-loop control on two DC motors. Please
    note that this term project builds on @ref lab3page.py, @ref lab4page.py,
    and @ref lab5page.py, so it may be advantageous for the reader to consider
    the documentation for each of those labs as well.
    
    The resistive touch panel was the only new hardware component to this
    lab, and it was used to detect the ball's x- and y-locations and 
    velocities atop the platform. This data was delivered as an outer-loop 
    feedback signal to the firmware's cascaded controller, which also involves
    inner-loop control according to data from the IMU device. See the block
    diagram depicted below for observation of our closed-loop controller.
    And please see @ref sec_filesT for descriptions of our project files.
    @image html term_block_diagram.png width=600px
       
    @section sec_resT Results
    Ultimately, our team was unsuccessful in balancing the ball for any 
    extended period of time. However, we have reached successful implementation
    of all components of the platform control, save for correct Kp, Ki, and Kd
    gain values. Features include, but are certainly not limited to, reading 
    from the touch panel and IMU devices, closed-loop motor control to 
    manipulate the platform's angle, thorough user interface and data 
    collection features, and, with further tuning of the outer- 
    and inner-loop controller gains, we are confident that our system would
    be able to successfully balance the ball.
    Please see the following video for a demonstration of our term project: \n 
    <CENTER>
    @htmlonly
    <iframe width="560" height="315" 
    src="https://www.youtube.com/embed/GsEgwm0p4Bg" 
    title="YouTube video player" frameborder="0" allow="accelerometer; 
    autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen></iframe>
    @endhtmlonly
    </CENTER>
    \n  
    
    @section sec_datT Data Collection 
    A user of our Term Project firmware is able to collect up to 15 seconds
    worth of data from nine categories of the associated hardware, where this
    data is written to a CSV file and may then be plotted in various 
    configurations. The data set includes time in [sec], the ball's position 
    and velocity, in both the x- and y-directions, and the rotating platform's
    angular position and velocity, in both the x- and y-directions. Please
    see <b>Figures 1-9</b> for observation of this data.
    
    <CENTER>
    @image html YvX.png width=500px
    <b>Figure 1:</b> Ball Position on Platform over Time. The ball's position
    along the x- and y-axes (defined here as the horizontal and vertical
    positions, respectively) of the platform are plotted against one another
    to provide a visual of the ball's path of travel over time.
    
    @image html XvT.png width=500px
    <b>Figure 2:</b> Horizontal Ball Position over Time. The ball's position, 
    in [mm], along the x-axis of the platform plotted over time in [sec].
    
    @image html YvT.png width=500px
    <b>Figure 3:</b> Vertical Ball Position over Time. The ball's position, 
    in [mm], along the y-axis of the platform plotted over time in [sec].
    
    @image html VXvT.png width=500px
    <b>Figure 4:</b> Horizontal Ball Velocity over Time. The ball's velocity, 
    in [mm/s], along the x-axis of the platform plotted over time in [sec].
    
    @image html VYvT.png width=500px
    <b>Figure 5:</b> Vertical Ball Velocity over Time. The ball's velocity, 
    in [mm/s], along the y-axis of the platform plotted over time in [sec].

    @image html THXvT.png width=500px
    <b>Figure 6:</b> Platform Pitch over Time. The platform's angular position, 
    in [deg], about the x-axis of the platform plotted over time in [sec].
    
    @image html THYvT.png width=500px
    <b>Figure 7:</b> Platform Roll over Time. The platform's angular position, 
    in [deg], about the y-axis of the platform plotted over time in [sec].
    
    @image html OMXvT.png width=500px
    <b>Figure 8:</b> Platform Pitch Velocity over Time. The platform's angular 
    velocity, in [deg/s], about the x-axis of the platform plotted 
    over time in [sec].
    
    @image html OMYvT.png width=500px
    <b>Figure 9:</b> Platform Roll Velocity over Time. The platform's angular 
    velocity, in [deg/s], about the y-axis of the platform plotted 
    over time in [sec].    
    </CENTER>
    
    @section sec_filesT Project Files
    
    @subsection sub_mainT Main File
    The main file instantiates our task- and class-files as objects to be run
    asynchronously. Note the task diagram below for information regarding file 
    communication and run frequency. See @ref main.py for more information. 
    @image html term_task_diagram.png width=500px
    
    @subsection sub_utaskT User Task
    The user interface is written as a generator function that prints to a 
    terminal emulator. It is able to read a user's keyboard presses as 
    controller and IMU commands, such as printing the IMU's current Euler
    angles and angular velocities or accepting user-input 
    controller gain values, over the USB virtual comm port. 
    See @ref UTask5.py for more information, and the figure below for the User
    Task's state transition diagram.
    @image html term_ui_task_std.png width=600px
    
    @subsection sub_ttaskT Touch Panel Task
    The touch panel task calls methods of the panel's driver class, 
    @ref touchpad.py, to read the ball's position and velocity data atop the 
    platform, as well as to prompt user calibration when necessary. Note that
    the task performs alpha-beta filtering of the ADC readings pulled from the
    panel driver and is also able to execute shift, scale, and offset 
    corrections on said panel data.
    See @ref TTask.py for more information and the figure below 
    for the Touch Panel Task's state transition diagram.
    @image html ttask_std.png width=500px  

    @subsection sub_imutaskT IMU Task
    The IMU task calls methods of the BNO055 driver class, @ref BNO055.py,
    to read IMU data and prompt user calibration when necessary.
    See @ref MTask5.py for more information and the figure below 
    for the IMU Task's state transition diagram.
    @image html imutask_std.png width=500px  
    
    @subsection sub_ctaskT Controller Task
    The controller task communicates controller gain values Kp, Kd, and Ki, 
    angular setpoints, and Euler angle/angular velocity data (read
    from the IMU device) to our closed-loop driver, @ref closedloop5.py. This
    task is also responsible for sending duty cycles to the motor task, 
    which enables motor actuation according to the actuation signal computed 
    in the closed-loop driver. Note that the controller task is able to control
    the outer- and inner-loop for our cascaded controller.
    See @ref CTask5.py for more information and the 
    figure below for the Controller Task's state transition diagram.
    @image html term_ctask_std.png width=500px

    @subsection sub_mtaskT Motor Task
    The motor task sends duty cycles, which are determined as the actuation
    signal of the closed-loop controller, to their respective motors,
    either Motor 1 or Motor 2. 
    See @ref MTask5.py for more information and the figure below 
    for the Motor Task's state transition diagram.
    @image html MTaskSTD3.png width=500px    

    @subsection sub_touT Touch Panel Driver
    This driver class handles ADC readings of the resistive touch
    panel device, which are associated with the ball's position and velocity. 
    Associated methods include (1) configuring the panel's four pins as outputs,
    floats, or ADCs to scan the x-y-z axes of the panel and (2) setting values
    for the scale, shift, and offset calibration coefficients to convert our
    ADC readings into acceptable distance ([mm]) readings.
    See @ref touchpad.py for more information.

    @subsection sub_imuT BNO055 Driver
    This driver class handles I2C communication with the BNO055 IMU device. 
    Associated methods include reading Euler angle and angular velocity data
    from the BNO, as well as reading/writing calibration coefficients
    according to the device's current calibration status.
    See @ref BNO055.py for more information.

    @subsection sub_clcT Closed-Loop Control Driver
    The closed-loop driver is a class file that computes actuation signals 
    according to user-defined controller gains Kp, Ki, and Kd, desired 
    setpoint, and, for use with the IMU or touch panel devices, the IMU's 
    Euler angle and angular velocity data or the ball's position and velocity,
    respectively. For our cascaded controller, the actuation signal computed
    by the outer-loop, which pulls its reference and feedback signals from
    the touch panel data, is sent as the reference signal for the inner-loop,
    which pulls its reference and feedback signals from the IMU data. 
    The controller is able to perform proportional, integral, 
    and/or derivative control.
    See @ref closedloop5.py for more information.

    @subsection sub_motT Motor Driver
    The motor driver is a class file that instantiates pin, timer, and timer 
    channel objects for the designated motor's PWM channels, which are 
    configured as inverted PWM channels. The driver also has a method to set
    motor duty cycles as a pulse width percent, whose value is passed in as the 
    closed-loop controller's actuation signal.
    See @ref motor5.py for more information.
    
    @subsection sub_shaT Shares Class
    The shares class file allows variables to be created, read from, and 
    written to multiple files.
    See @ref shares.py for more information.
    
'''