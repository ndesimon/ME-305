'''!
    @file mainpage.py
    Brief doc for mainpage.py

    Detailed doc for mainpage.py 

    @mainpage
    @tableofcontents

    @section sec_intro Introduction
    My name is Nicholas De Simone, and this portfolio contains documentation 
    for various mechatronics lab projects from my time as a mechanical 
    engineering student at Cal Poly, San Luis Obispo. These projects involve
    various hardware mechanisms, such as PMDC/servo motors, quadrature encoders,
    inertial measurement units, and the like, driven by Python source code
    written for microcontrollers (specifically the Nucleo L476). Through 
    these projects, my lab teams and I were able to practice object-oriented 
    and task-based asynchronous programming, serial communication, etc. Please 
    reference any associated links to source code and demonstration videos for 
    further information.

    @section sec_305pro ME 305 Projects

    @subsection sub_labT Term Project: Ball-Balancing Platform
    Our ME 305 Term Project was a culmination of Labs 1-5 described below.
    The goal of the term project was to incorporate closed-loop control, 
    communication with resistive touch panel and IMU devices, and serial user-
    input over the USB VCP port of our Nucleo MCU in order to balance a steel
    ball atop a rotating platform. See @ref labtermpage.py for more details.
    
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
    
    @subsection sub_lab1 Lab 1: LED Light Show
    Our introduction to microPython-based programming in ME 305. This lab
    consisted of writing a finite state machine script to display
    three LED pulse patterns on the Nucleo's native LED.
    See @ref lab1page.py for more details.   
    
    @subsection sub_lab2 Lab 2: Incremental Encoders
    Lab 2 implements task and class Python files to read quadrature encoder 
    pulse signals and interpret them as the angular position of a motor shaft.
    See @ref lab2page.py for more details.
    
    @subsection sub_lab3 Lab 3: DC Motor Control
    Lab 3 uses pulse width modulation to control DC motors, as well as reads
    from the attached quadrature encoders from Lab 2.
    See @ref lab3page.py for more details.
    
    @subsection sub_lab4 Lab 4: Closed-Loop Speed Control
    Lab 4 builds on Labs 2 and 3 with additional task- and driver-files to 
    perform closed-loop speed control on the DC motors of Lab 3.
    See @ref lab4page.py for more details.
    
    @subsection sub_lab5 Lab 5: I2C and Inertial Measurement Unit
    Lab 5 reads angular position and velocity data from an inertial
    measurement unit (specifically, the Bosch BNO055) attached to our platform. 
    This data is 
    implemented as feedback in the closed-loop controller of Lab 4, with the 
    goal of stabilizing the platform relative to the direction of gravity.
    See @ref lab5page.py for more details.

    @section sec_sen Senior Project
    ME 305: Ignore \n 
    Explain senior project. \n 
    
    @subsection sub_vid Demonstration Video
    Check out the link below for a short demo \n 
    <CENTER>
    @htmlonly
    <iframe width="560" height="315" 
    src="https://www.youtube.com/embed/lX-ZXvdmfGU" title="YouTube video player" 
    frameborder="0" allow="accelerometer; autoplay; clipboard-write; 
    encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    @endhtmlonly
    </CENTER>
    \n 
    @subsection sub_link Senior Project Portfolio
    Explain what can be found in the portfolio. \n 
    <a href="https://projectexpo.calpoly.edu/2021/cnc-feed-drive/">
    Click here</a> for our 2021 Senior Project Portfolio.

    @section sec_con Contact Info
    * <b>Email: </b>desimone1n@gmail.com
    * <a href="https://bitbucket.org/ndesimon/me405_labs/src/master/">
    <b>Source Code Repository</b></a>
    * <a href="https://projectexpo.calpoly.edu/2021/cnc-feed-drive/">
    <b>Senior Project Portfolio</b></a>
  
    @author Nicholas De Simone
    @image html prof_pic.png width=200px
    
'''