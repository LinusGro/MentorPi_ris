# Project Seminar 'Robotics and Computational Intelligence' 2025 presented by RIS | Technical University of Darmstadt

More information on the course can be found here: https://www.etit.tu-darmstadt.de/ris/lehre_ris/lehrveranstaltungen_ris/pro_robo_ris/


This repository serves as a starting base for the students participating in this year's course. 

The task will be to program a MentorPi that is set in a maze environment. Here, the MentorPi is supposed to handle different tasks. These tasks include the autonomous navigation and localization of the MentorPi in an unknown maze.

Detailed information on the tasks is given internally via Moodle.

| ![Image 2](images/Bild1.jpg) | ![Image 1](images/Bild_PiBot_im_Labyrinth.jpg) |
|------------------------|------------------------|
| MentorPi robot named Chewbacca |  Robot in the maze     |


This repository aims to provide a reasonable starting position for ROS2 development on the Raspberry Pi 5 based MentorPi robot platform from Hiwonder. Specifically, the version equipped with the mecanum-wheel drivetrain and the gimbal monocular camera (https://www.hiwonder.com/collections/raspberrypi-bionic-robot/products/mentorpi-m1?variant=41285892702295).


# Table of Contents
- [General Information](#general-information)
   - [Basic Knowledge](#basic-knowledge)
- [Basic Setup](#basic-setup)  
   - [Linux Setup](#linux-setup)
   - [Installing ROS2](#installing-ros2)
      - [Install Additional Dependencies](#install-additional-dependencies)
   - [Setup your ROS2 Workspace](#setup-your-ros2-workspace)
   - [Set Environment Variables](#set-environment-variables)
   - [Set User Permissions](#set-user-permissions)
- [The Maze](#the-maze)
	- [Matrix representation of the maze](#matrix-representation-of-the-maze)
	- [Example maze](#example-maze)
   	- [ROS2 datatype for the maze](#ros2-datatype-for-the-maze)
	- [Implementation of the maze](#implementation-of-the-maze)
- [ROS2 on an additional computer](#ros2-on-an-additional-computer)
   - [Computer running Ubuntu](#computer-running-ubuntu)
   - [Computer running Windows or macOS](#computer-running-windows-or-macos)
- [Testing](#testing)  
   - [Test the Camera](#test-the-camera)
      - [Test the Camera with a connected Monitor](#test-the-camera-with-a-connected-monitor)
      - [Test the Camera from a Remote Computer (a bit more advanced)](#test-the-camera-from-a-remote-computer-a-bit-more-advanced)
   - [Test AprilTag](#test-apriltag)
      - [Camera Calibration](#camera-calibration)
      - [Rectification Pipeline](#rectification-pipeline)
      - [AprilTag Node](#apriltag-node)
   - [Test the LIDAR](#test-the-lidar)
   - [Test SLAM](#test-slam)
- [Quality of Life Additions and Some Tips](#quality-of-life-additions-and-some-tips)
   - [Terminator](#terminator)
   - [SSH Setup](#ssh-setup)
   - [rviz2](#rviz2)
   - [Multiple Robots on the Same Network](#multiple-robots-on-the-same-network)
   - [About Standardization](#about-standardization)
   - [How To Start Development](#how-to-start-development)
- [Contributions](#contributions)


# General Information
The MentorPi platform from Hiwonder is a Raspberry Pi 5 based robot platform. The operating system we will be installing on the Raspberry Pi 5 is Ubuntu 24.04, which is a version of Linux. Therefore the robot can be thought of as a normal computer, that can be used with a mouse, keyboard and monitor. The robot uses mecanum wheels, and features a monocular camera, which can be moved around, a LIDAR scanner, an inertial measurement unit (IMU), and wheel encoders.
As a development framework, the Robot Operating System (ROS2) is used. The version used is ROS2 Jazzy. ROS2 is an open-source framework for building robotic applications. It acts as the middleware between the different components of the robot and also provides tools, libraries, hardware abstraction, device drivers and more for standardized robot development.
<br>
<br>

## Basic Knowledge
Before starting, some basic knowledge should be available. In case you are not familiar with the following, read online about the basics or watch some tutorials (e.g. Youtube). **Important: These basics will not be covered in the lecture. You are expected to learn the necessary skills on your own.**
- some basics in Linux (you will use Ubuntu 24.04)
    - basic console commands `cd`, `ls`, `mkdir`, `source`, `cp`, `mv`, `rm`, `chmod`, ...
    - the purpose of `sudo`
    - the purpose of `apt-get`
    - read here https://www.digitalocean.com/community/tutorials/an-introduction-to-linux-basics or watch e.g. this tutorial https://www.youtube.com/watch?v=s3ii48qYBxA
- some basics in C/C++
    - C/C++ compiling procedure including the purpose of `cmake`, `make` and `CmakeLists.txt`
- some basics in Python
    - the purpose of `pip`
- the purpose of Git as well as basic commands `commit`, `push`, `pull`, `clone`, `fork`, ...
    - e.g. have a look at https://learngitbranching.js.org/?locale=de_DE for learning the basics of git
- ROS (you will use the ROS2 version Jazzy)
    - *Note: How ROS is installed on the MentorPi will be explained further below*
    - do the tutorials at https://docs.ros.org/en/jazzy/Tutorials.html
    - RVIZ
    - rqt (e.g. `rqt_graph` )
    - For more information, see the ROS2 documentation: https://docs.ros.org/en/jazzy/index.html
 - basic knowledge about mobile robots
    - will be taught in the lecture
    - kinematic model of mecanum wheel drive robot (see https://www.youtube.com/watch?v=gnSW2QpkGXQ or https://www.youtube.com/watch?v=Xrc0l4TDnyw&t=91s
    - basic functionality of an IMU, LIDAR and encoders
- General coding advice: Don't copy paste commands blindfold. Try to understand what's the purpose of the command and also read what happens in the console output (especially, when there are errors). ChatGPT can be a great help in explaining the functionality of commands, interpreting error messages, and assisting with debugging. However, **ChatGPT does not replace a thinking brain sitting in front of the laptop**, and you should always try to understand what you are typing into the console and why.

<div style="display: flex; gap: 10px; align-items: flex-start;">
  <img src="images/meme_chatgpt_small.png" alt="Meme" width="300"/>
  <img src="images/robo_debugging.png" alt="Robo debugging" width="500"/>
</div>




# Basic Setup
* In this chapter, the basic setup of the robot is explained. You will install Linux, ROS2 and all necessary drivers for the motors, servos, camera and LIDAR on the Raspberry Pi 5 of the robot.
`Ubuntu 24.04` together with `ROS2 Jazzy` is used in this project.

* This README walks you through the initial setup for your robot. How and why things work may not be explained in detail. For explanation of the project structure and information about nodes and topics, see the project documentation in the `/docs` folder of this repository.

* This README assumes basic knowledge about the LINUX file system and how to navigate it, see [Basic Knowledge](#basic-knowledge).

<br>

## Linux Setup
First, `Ubuntu 24.04` needs to be installed on the SD card of the Raspberry Pi 5. The SD card is located under the Raspberry PI 5 as shown below:

<p align="center">
  <img src="images/sd_card_location.png" alt="SD card location">
</p>

1. **Flash Linux Image**  
The easiest way to flash the Linux image is via the Raspberry Pi imager.
* For Windows, you can download the program here: https://www.raspberrypi.com/software/
* On Ubuntu, you can simply install the program via the following command:
```bash
sudo apt install rpi-imager
```
Open the Raspberry PI Imager Tool, choose `Raspberry Pi 5` under *Device* and under *Choose OS*: `Other general-purpose OS` -> `Ubuntu` -> `Ubuntu Desktop 24.04.2 LTS (64-bit)`. Then choose the micro SD-card (at least 64GB) you want to install the OS on and click next to continue following the instructions of the tool.

2. **Boot for the first time**
* Put the SD-card in the Raspberry Pi 5, and connect a mouse, keyboard and a monitor. The monitor can be connected via a micro HDMI cable, the micro HDMI port is located on the Raspberry Pi 5 on the forward facing side of the robot. A mouse and a keybaord can be connected via USB using the USB dock on the backward facing side of the robot. Then, boot the robot using the switch on the black PCB above the Raspberry Pi 5. 
* Follow the installer for Ubuntu. You can choose your own username and password.
<br>

## Installing ROS2
* Follow this guide: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html to install ROS2 Jazzy on the Raspberry Pi 5. For development, it makes a lot of sense to also have an additional computer with ROS2 installed. This makes remotely diagnosing and controlling the robot much easier. Choose the **Desktop Install** both for the robot and, if applicable, your computer. 
* Run 
```bash
source /opt/ros/jazzy/setup.bash
```
to source the `ROS2` installation. This command needs to be entered manually every time you want to work with `ROS2` in a new terminal.
In order to avoid this, you can add it to your .bashrc file.

The .bashrc file is a script in your home directory that initializes settings, environment variables, and commands for new terminal sessions. It is executed everytime a new shell is started.

To add the command, open the file with a text editor, for example using:
```bash
nano ~/.bashrc
```
and add the new command, in this case:
```bash
source /opt/ros/jazzy/setup.bash
```
to the end of the file. Save the file and reload by either entering
```bash
source ~/.bashrc
```
or by closing the terminal and opening a new one (doing this runs the .bashrc file).
<br>
<br>

### Install Additional Dependencies
First, update your package manager:
```bash
sudo apt update
```
Then install the following packages (there might be warnings that the packages might not be supported for ROS-Jazzy but you can ignore these for now):
* **usb_cam**
   - A ROS 2 package for interfacing with USB cameras, enabling video capture and streaming in robotic applications.
```bash
sudo apt install ros-jazzy-usb-cam
```
* **camera_calibration**
   - A ROS 2 package for calibrating USB cameras.
   - Needed to create a rectified image, wich is essential for object or Tag detection.
```bash
sudo apt install ros-jazzy-camera-calibration
```
* **image_proc**
   - A ROS 2 package for rectifying an image together with a camera calibration file.
   - Needed to create a rectified image, wich is essential for object or Tag detection.
```bash
sudo apt install ros-jazzy-image-proc
```
* **apriltag-ros**
   - A ROS2 package for detecting **AprilTags**, which are fiducial markers used for **robot localization and object tracking**.
   - Important for object detection and relative position calculation.
```bash
sudo apt install ros-jazzy-apriltag-ros
```
* **apriltag-msgs**
   - A ROS2 package with the proprietary messages used by the `apriltag` package.
```bash
sudo apt install ros-jazzy-apriltag-msgs
``` 
* **slam_toolbox**  
   - A ROS 2 package for Simultaneous Localization and Mapping (SLAM), providing tools for 2D SLAM, map merging, and long-term mapping.  
   - Essential for robots that require real-time environment mapping and localization in unknown areas.  
```bash
sudo apt install ros-jazzy-slam-toolbox
```
* **navigation2**
   - A ROS 2 package for robot navigation, enabling autonomous path planning, obstacle avoidance, and control.
   - Required for setting up navigation tasks in your robotic project.
```bash
sudo apt install ros-jazzy-navigation2
```
* **joint-state-publisher**
   - A tool for publishing the state of all joints in a robot.
   - Essential for visualizing robot movement or simulating joint positions in RViz.
```bash
sudo apt install ros-jazzy-joint-state-publisher
```
* **xacro**
   - Stands for XML Macros and is used to simplify the creation of URDF files for robot models.
   - Required for generating dynamic robot description files.
```bash
sudo apt install ros-jazzy-xacro
```
* **ros-jazzy-imu-complementary-filter**
   - Provides a complementary filter for IMU data processing in the ROS Jazzy distribution.
   - Helps in fusing accelerometer and gyroscope data for smoother motion tracking.
```bash
sudo apt install ros-jazzy-imu-complementary-filter
```
* **python3-transforms3d**
   - A Python library for handling 3D transformations such as rotations and translations.
   - Used in the `JoystickControl` package for manipulating 3D poses and transformations.
```bash
sudo apt install python3-transforms3d
```
* **python3-pydantic**
   - A Python library for data validation and settings management.
   - Required by the `ros usb_cam` package to handle camera configurations and data structures.
```bash
sudo apt install python3-pydantic
```
<br>

## Setup your ROS2 Workspace
In addition to the global ROS2 workspace we just installed in `/opt/ros/jazzy`, an additional workspace in your home directory `/home/user` is needed. (Substitute your home directory).
In general, ROS2 packages installed via the package manager get installed in the global workspace, while your own projects and code are usually organized in a separate ROS2 workspace inside your home folder. We will follow this structure.

1. **Create the following file structure** inside your home directory ~
```bash
|-- workspace
    |-- ros2_ws
        |-- src
```
You can achieve this with the following command:
```bash
mkdir -p ~/workspace/ros2_ws/src
```
Navigate inside the `ros2_ws` folder and initialize the new workspace with
```bash
colcon build
```
You may need to install colcon at this point. It can be installed with: 
```bash
sudo apt install colcon
```
After this, you can source your workspace with
```bash
source install/local_setup.bash
```

This command can also be added to your .bashrc file. This way, your workspace is sourced every time a new terminal is opened. Use the correct path, e.g.:
```bash
source /home/user/workspace/ros2_ws/install/local_setup.bash
```
**Make sure** to change `user` to the username you choose for the robot.

2. **Download the needed Packages from this repository**
    - Download all folders from the `src` folder and place it in **your** `src` folder.

3. **Finished file structure**  
The finished file structure should look like the following:
```bash
|-- workspace
    |-- ros2_ws
        |-- build
        |-- install
        |-- log
        |-- src
            |-- calibration
            |-- imu_calib
            |-- ldrobot-lidar-ros2
            |-- peripherals
            |-- driver
            |-- orchestrator_launch
            |-- simulations
```
4. **Build the workspace again**  
When you are in the `ros2_ws` folder, you can build the workspace again with
```bash
colcon build
```
**Make sure** the build process succeeds.
<br>
<br>

## Set Environment Variables
Because the MentorPi robot comes in different versions, the used version needs to be exported as an environment variable:
```bash
export MACHINE_TYPE=MentorPi_Mecanum
```
This command should also be added to your .bashrc file to ensure the availability of the variable upon startup of a new terminal.
<br>
<br>

## Set User Permissions
Communication with the expansion board occurs via a serial connection. To enable access, you must ensure your user belongs to the appropriate group with permissions to access serial devices. This is achieved with:
```bash
sudo usermod -a -G dialout $USER
```
You need to restart your Raspberry Pi 5 for this rule to take effect. 
<br>
<br>

# The Maze
The maze can be set up modularly in size and configuration and consists of base plates and wall plates, which are placed on the base plates.
The base plates have a size of approx 254mm x 254mm and define a segment/cell of the maze. The wall plates are made of 250mm x 170mm x 3mm MDF. With 3D printed sockets, the wall plates can be mounted on each side of a base  plate.  
Our institute features two configurable mazes, each located in a different room. The shape of the maze can be freely chosen—whether square, rectangular, L-shaped, or any other form.

![Img](images/maze_details.jpg)
*(a) modular base plates (b) wall plate (c) full 3x3 maze*

![Image3](images/maze_full_crop.png)
*full 6x14 maze with robots driving in it*

Some wall plates of the maze are laser-engraved with recursive AprilTags - these can be ignored! They were used in last years project seminar by the robot to localize itself.
More information on the arena, e.g. on size of the base and wall plates can be found in a separate repository:
https://github.com/NikHoh/apriltag-maze

## Matrix representation of the maze

To exchange and represent different mazes, we define a maze $L$ of the size $n \times m$ using a matrix with a 4 Bit encoding:

```math
\mathcal L = [l_{ij}]\in \mathbb{B}^{n\times m} \quad \text{with} \quad \mathbb{B}=\{b\in\mathbb{Z}\,\mid\,0\leq b \leq 2^4-1=15\}.
```
The matrix entries are hereby integers $l_{ij}\in\mathbb{B}=\\{0,1,\ldots,15\\}$ with $\mathbb B$ being the 4 bit range of values.
The column index $i\in\\{1,\ldots,n\\}$ is counting in the $x$-direction and the row index $j \in\\{1,\ldots,m\\}$ is counting in the $y$-direction. The value of $l_{ij}$ determines the amount of walls of a cell using a 4 bit coding, which will be explained below.

Since the maze does no have to be in a rectangular shape (it can be in a L-shape, or some corners are missing), we first determine the size $n \times m$ of the smallest surrounding rectangle of the maze. $n$ and $m$ are hereby positive integers and count the number of the baseplates in $x$ and $y$-direction.
The global coordinate system's origin 𝒪 is set in one corner of the maze.

Starting from the origin 𝒪, the baseplates of the maze will be numbered by a segment number $I\in\\{1, \ldots,  nm\\}$, which allows us to define the cell/segments. Like this, the baseplates of the maze will be numbered, starting from the origin 𝒪 in the $x$-direction and counting every existing, and nonexisting baseplate.

![img_mazenumbered](images/maze_numbered.png)
*3x3 maze with n=3, m=3 and the numbered cells I= 1,2,...,9*

In the case, that some outer cells are missing, we still iterate through all *missing* baseplates. For example in this maze, we added some walls and now cells with Index $I=\\{4,7,9\\}$ are not part of the maze, but we still get the same numbering:

```
+---+---+---+
| 1 | 4 | 7 |
+   +---+---+
| 2   5   8 |
+   +---+---+
| 3   6 | 9 | 
+---+---+---+
```


We can calculate the indices $i,j$ given the segment number $I$ by
```math
I = (j-1)n+i.
```
We also get segment number  $I$ given the indices $i,j$ by using the modulo and floor function:
```math
i=((I-1)\mod n)+1 \qquad \qquad j = \Big\lfloor \frac{I-1}n \Big\rfloor + 1.
```

Now that $n$ and $m$ are determined and the cells are numbered by $I$, we define the value of the cell $l_{ij}=\ldots$ using a binary coding:
```
(0000) - no walls, but the cell is part of the maze
(0001) - wall in postive x-direction
(0010) - wall in negative x-direction
(0100) - wall in positive y-direction
(1000) - wall in negative y-direction
(1111) - cell is not part of the maze
```
For example, cell $I=5$ in the example maze has a wall in positive and negative $x$-direction and hence gets the binary coding `(0011) = 3`. We therefore set $l_{22}=3$ in the matrix representation.
This lookup table helps with the correspondance:

![Maze cell lookup table](images/maze_cell_table.png)




**Important notes**: A maze and its representation is valid, if
- it is closed, i.e. every outer wall exist - there is no way *in* or *out* of the maze.
- a wall exists in one cell $I$, it must also exist in the corresponding neighboring cell. For example, cell $I=1$ has a wall on the right, then cell $I=4$ does need to have a wall above on the left.
- The size $n \times m$ of the maze is minimal, e.g. it is not filled up with *empty*, not usable cells on either side. 
- The maze is atleast $2\times 2$ and the first cell at the origin is not fully enclosed.



For solving a known maze, [Wikipedia](https://en.wikipedia.org/wiki/Maze-solving_algorithm) is a good starting point for maze solving algorithms.
Here it is useful, to represent a maze as a graph $\mathcal G$, where the edges correspond to the cells and vertices represent connected cells:
![ImgMaze2Graph](images/maze2graph.png)

## ROS2 datatype for the maze
The package maze interface contains the definiton of the datatype 'RosMaze.msg':
```cpp
uint8 n 		// x-dimension of the maze
uint8 m			// y-dimension of the maze
int16 start_idx		// Index I of the starting cell
int16 end_idx		// Index I of the goal/end cell
uint8 start_orientation	// robots orientation of the start (4-bit encoding for +-x, +-y dirction)
uint8[] l		// matrix entries l_ij, listed by I={1,...,nm}
```
as well as the service interface 'GetRosMaze.srv':
```cpp
int8 maze_nr
---
maze_interface/RosMaze maze
```
The maze_publisher_node package contains a node that acts as a ROS2 server. Upon receiving a request containing the maze ID, it will respond with a RosMaze.msg with the corresponding maze. If the ID is invalid it will respond with a message where all values are 0. 
This node will be used on exam day to provide the maze data for task 1. You can use the node to test your implementation of a client for the service. The node can be started with: 
```bash
ros2 run maze_publisher_node maze_server
```
An example file is already added to the package (1.maze). The files are organized line-by-line. The first lines are ```n``` , ```m```, ```start_idx```, ```end_idx```, ```start_orientation```. All lines starting from line 5 correspond to the matrix ```L``` mentioned earlier, listed by the cell index ```I```.

## Implementation of the maze
The folder `maze` contains some useful helperfunctions when working with the mazes:
- `generate_random_maze.py` generates a random maze given a specific size and filling factor
- `ascii_to_L.py` generates an maze L given a drawn maze in ascii-style in a `.txt`-file.
	- 3 dashes `---` represent a horizontal wall
	- 3 empty spaces `␣␣␣` represents the absence of a horizontal wall
	- `|` represents a vertical wall
	- `+`represents the corner of a cell
	- Important: You cant use tabs, use blank space characters!
- `validate_maze.py`checks if a maze L is valid
	- all entries in L are in `[0,...,15]`
	- if a wall exists on one cell, it must exist on the neighboring cell
	- all nonreachable cells are marked with `(1111)=15` 
	- all outer walls exist
	- checks, if the maze is minimum size or if it can be trimmed, ie if all cells in an outer row/column are non-reachable
- `isolate_unreachable_cells_and_trim.py`marks unreachable cells in the maze with `(1111)` and trims the maze, if all outer cells in a row/column are non-reachable
- `draw_ascii_maze.py` draws a maze in ascii-style in the console
- `plot_maze.py`generates a plot of the maze
- `test_maze_functions.py` gives an example on how to use the functions
- `L_to_rosfile.py` generates a .maze file that is compatible with the maze publisher node
- `rosfile_to_L.py` reads a .maze file and extracts the matrix L from the file

<br>




## Example maze
As a final example, lets have a look at the maze on the top left. Putting the origin on the upper left corner, we identify the size as $n=13$ and $m=6$ and get the matrix representation $\mathcal L$. Using the functions, we can draw the maze in ascii-style or plot it.

<table>
  <tr>
    <td>
	      <p><strong>Original Maze</strong></p>
      <img src="images/maze_1_crop.png" alt="Original Maze" width="350">
    </td>
    <td>
      <p><strong>Matrix Representation</strong></p>
		      <img src="images/matrix_L.png" alt="matrixL" width="250">
    </td>
  </tr>
  <tr>
    <td>
      <p><strong>ASCII Maze</strong></p>
      <pre style="font-family: monospace; font-size: 12px;">
+---+---+---+---+---+---+
|                       |
+   +   +   +   +   +   +
|                       |
+   +   +---+---+   +   +
|       |               |
+   +   +   +   +   +   +
|       |               |
+   +   +---+---+   +   +
|                       |
+   +   +   +   +   +   +
|                       |
+---+---+   +   +---+---+
|                       |
+   +   +   +   +   +   +
|                       |
+   +   +---+---+   +   +
|               |       |
+   +   +   +   +   +   +
|               |       |
+---+---+   +   +   +   +
|                       |
+   +   +   +   +   +   +
|                       |
+   +   +---+---+   +   +
|                       |
+   +   +   +   +   +   +
|                       |
+---+---+---+---+---+---+
      </pre>
    </td>
    <td>
      <p><strong>Plotted Maze</strong></p>
      <img src="images/maze_plotted.png" alt="Plotted Maze" width="250">
    </td>
  </tr>
</table>






# ROS2 on an additional computer
As mentioned before it is recommended to have an additional computer set up with ROS2 in order to use for example the visualization from rviz2 without the need of having a HDMI cable hooked to the robot at all times. Therefore an additional computer will have to be set up using ROS2. 
<br>
## Computer running Ubuntu
Since the installation mentioned above is used to install ROS2 onto the Raspberry Pi, you can simply repeat the exact same steps to make ROS2 work on your system. Make sure that your PC/Laptop is allowed to communicate with other devices in the same network, otherwise you won't be able to communicate with the robot.
<br>
## Computer running Windows or macOS
The shown installation is only working natively on Ubuntu therefore additional steps are necessary. You can either install ROS2 for Windows/macOS following the guides provided on docs.ros.org(not recommended) or you can use a **Virtual Machine(VM)** to emulate an Ubuntu OS on your system. **We recommend using a VM for this purpose** because the install process from the Raspberry Pi will be exactly the same.<br>
Another possibility would be to run ROS2 from a docker container but this will limit you to GUI-less application (no rviz therefore also not recommended).
### Windows 10/11
In general you can use any VM software you prefer. Possible solution which are available for free (for non-commerical use) are Oracle's Virtual Box(no account required) or VMWare's Workstation Pro (free account required, https://www.youtube.com/watch?v=kTO810vbF_E). Install the VM software and set up a new VM using an ubuntu image which are e.g. available at https://releases.ubuntu.com/noble/.<br>
If this is the first VM you have ever set up, you can find many tutorials on how to do this e.g https://www.youtube.com/watch?v=nvdnQX9UkMY for VirtualBox or https://www.youtube.com/watch?v=BHpRTVP8upg for Workstation Pro (video is 7 years old but the process is still mostly the same).<br>
After setting up the OS onto your VM, you can repeat the same process from the Raspberry Pi to install ROS2. After installing ROS2 and all of the required dependencies you need to make sure that the VM is able to communicate with the Robot. The easiest way to ensure a connection would be to use the following command in a terminal:
```bash
ping <hostname>
```
Where <hostname> must be replaced by the hostname you choose when initializing the Raspberry Pi. Make sure that the robot is powered on and connected to the same network (not eduroam as this might cause problems) as your computer. If the ping is successful, no further steps are required. If this ping is not successful the connection between to VM and the robot could not be established. A first step would be to set the VM's network properties to "Bridged" instead of "NAT" (default). This will expose the VM directly to the network and therefore might be solving the problem.<br>
When using Workstation Pro there is also an option to add a virtual network interface in the settings (Edit->Virtual Network Editor->Change Settings->VMnet0). This virtual network interface can then be set to bridged and selected as the preferred network interface for the VM. If the ping is still not returned you will have to do further troubleshooting by yourself. If you cannot make this work, we recommend visiting the consultation hours.
### MacOS
In general you can use any VM software you prefer. Possible solution which are available for free (for non-commerical use) are Oracle's Virtual Box (no account required) or VMWare's Fusion Pro (free account required, https://www.youtube.com/watch?v=kTO810vbF_E, select Fusion instead of Workstation). Install the VM software and set up a new VM using an ubuntu image which are e.g. available at https://releases.ubuntu.com/noble/ (for Intel silicons) or "noble-desktop-arm64.iso" at https://cdimage.ubuntu.com/daily-live/20240421/ (for Apple/ARM silicons). <br>
If this is the first VM you have ever set up, you can find many tutorials on how to do this e.g https://www.youtube.com/watch?v=nvdnQX9UkMY for VirtualBox or https://www.youtube.com/watch?v=BHpRTVP8upg for Workstation Pro (video is 7 years old but the process is still mostly the same, Fusion is the same).<br>
After setting up the OS onto your VM, you can repeat the same process from the Raspberry Pi to install ROS2. After installing ROS2 and all of the required dependencies you need to make sure that the VM is able to communicate with the Robot. The easiest way to ensure a connection would be to use the following command in a terminal:
```bash
ping <hostname>
```
Where <hostname> must be replaced by the hostname you choose when initializing the Raspberry Pi. Make sure that the robot is powered on and connected to the same network (not eduroam as this might cause problems) as your computer. If the ping is sucessful, no further steps are required. If this ping is not successful the connection between to VM and the robot could not be established. A first step would be to set the VM's network properties to "Bridged" instead of "NAT" (default). This will expose the VM directly to the network and therefore might be solving the problem. If the ping is still not returned you will have to do further troubleshooting by yourself. If you cannot make this work, we recommend visiting the consultation hours.
<br>
<br>



# Testing
If you successfully installed everything, set up ROS2 on your additional computer and understood how the maze works, we can start testing.


## Test Motor Functions
The expansion board from Hiwonder controls all 4 wheels, the 2 PWM servos the camera is attached to and also allows for access to the IMU. 
All this functionality is managed by the `controller` package, which can be found in `~/workspace/ros2_ws/src/driver`.
With
```bash
ros2 launch controller controller.launch.py
```
you can launch this package. You can verify a successful launch by typing
```bash
ros2 topic list
```
in a second terminal. This will list all topics currently published or subscribed to by all running nodes. After the launch of the `controller` package, the list should look like the following:
```bash
matthias@matthiasT15:~$ ros2 topic list
/cmd_vel
/controller/cmd_vel
/controller_manager/joint_states
/diagnostics
/imu
/imu/rpy/filtered
/imu/steady_state
/imu_corrected
/joint_states
/odom
/odom_raw
/odom_rf2o
/parameter_events
/robot_description
/ros_robot_controller/battery
/ros_robot_controller/bus_servo/set_position
/ros_robot_controller/bus_servo/set_state
/ros_robot_controller/button
/ros_robot_controller/enable_reception
/ros_robot_controller/imu_raw
/ros_robot_controller/joy
/ros_robot_controller/pwm_servo/set_state
/ros_robot_controller/sbus
/ros_robot_controller/set_buzzer
/ros_robot_controller/set_led
/ros_robot_controller/set_motor
/ros_robot_controller/set_oled
/ros_robot_controller/set_rgb
/rosout
/set_odom
/set_pose
/tf
/tf_static
```
Now the fun part begins. Open yet another terminal and type
```bash
ros2 launch peripherals joystick_control.launch.py
```
This launches the joystick_control part of the `peripherals` package. This node handles the controller. Make sure the controller is switched on. The controller should now be connected to the USB dongle plugged in to the Raspberry Pi 5. 
The left joystick controls the linear motion of the robot, while the right controls the rotational momentum. With the D-Pad, you can additionally rotate the camera around. Pressing "START" resets the camera position.
<br>
<br>

## Test the Camera

### Test the Camera with a connected Monitor
Run
```bash
ros2 launch peripherals usb_cam.launch.py
```
to launch the `camera` node from the `peripherals` package. Typing
```bash
ros2 topic list
```
you should see 
```bash
matthias@matthiasT15:~$ ros2 topic list
/ascamera/camera_publisher/rgb0/camera_info
/ascamera/camera_publisher/rgb0/compressedDepth
/ascamera/camera_publisher/rgb0/image
/ascamera/camera_publisher/rgb0/image_compressed
/ascamera/camera_publisher/rgb0/image_raw/theora
/image_raw/zstd
```
these topics added to your list. `/ascamera/camera_publisher/rgb0/image` is the topic we care about. Run
```bash
ros2 run rqt_image_view rqt_image_view
```
A window should open. In the top left dropdown menu choose `/ascamera/camera_publisher/rgb0/image` as the topic. Now the live video feed from the camera should be displayed.\
You may need to physically adjust the focus by turning the lens of the camera. Pliers may be needed.
<br>
<br>

### Test the Camera from a Remote Computer (a bit more advanced)
Viewing the video feed from a remote computer is not as straight forward. While all `ROS2` topics published by one machine are visible by all machines running `ROS2` in the same network by default, displaying the raw video stream on a remote machine is not generally possible (bandwidth limitation). Instead, the `/ascamera/camera_publisher/rgb0/image_compressed` topic published by the `camera_node` is utilized. By running a decompresser node on the receiving machine, we can decompress the compressed image on the receiving machine and then display this decompressed image.

**Requirements** for streaming the video feed to a different computer in the same network:
- The receiving computer needs to run `ROS2` (preferably `ROS2 Jazzy`)
- A basic `ROS2` workspace needs to be setup on the receiving computer with the `image_decompressor` package installed (The package can be downloaded from this repository).
- Both, the Raspberry Pi 5 and the receiving computer need to be connected to the same network (Eduroam does not work).  

**Setting up the Connection**  
1. Launch the `camera` node on the Raspberry Pi 5:
```bash
ros2 launch peripherals usb_cam.launch.py
```
2. Run the `decompress_image_node` from the `image_decompressor` package on the receiving computer:
```bash
ros2 run image_decompressor decompress_image_node
```
3. Run `rqt_image_view` on the receiving computer and select the `/decompressed_image` topic to display the decompressed image, the `decompress_image_node` publishes.
```bash
ros2 run rqt_image_view rqt_image_view
```
<br>

## Test AprilTag
The AprilTag detection can only detect tags in a rectified image. Meaning straight objects in real life also appear straight in the image. The `image_proc` package we installed earlier can handle this for us, given we calibrate the camera first. 
<br>
<br>

### Camera Calibration
This can be done without the HDMI cable connected but it is strongly recommended to calibrate the camera with a cable and a monitor connected.
<br>
You can calibrate the image with the ROS2 package `camera-calibration`. First, make sure the camera node is running:
```bash
ros2 launch peripherals usb_cam.launch.py
```
Follow this tutorial on camera calibration:
 https://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration  

*Note: In the lab we have big wooden checkerboards to calibrate your camera with the properties: N = 9, M = 7, X = 0.1.*

The correct command for our workspace is (you might want to understand what --remap means because you will most certainly encounter it again):
```bash
ros2 run camera_calibration cameracalibrator --size MxN --square X --ros-args --remap image:=/ascamera/camera_publisher/rgb0/image --remap camera:=/ascamera --remap camera/set_camera_info:=/usb_cam/set_camera_info
```
Make sure to replace **M** with the vertical dimension of your calibration checkerboard and **N** with the horizontal dimension of your calibration checkerboard. **X** is the length of one square of the checkerboard in meters. Clicking on Upload will save the calibration file at the correct place. If everything works correctly, you can see where the file was saved in the command window in which `usb_cam` is running.

<br>


### Rectification Pipeline
As already discussed, we will use the `image_proc` package to rectify our raw image the `usb_cam` node provides. This is easiest with a launch script from the `peripherals` package, which launches both the `usb_cam` node and the `image_proc` node. So before running, make sure the `usb_cam` is not already running on its own.
```bash
ros2 launch peripherals image_pipeline.launch.py
```
The topic `/apriltag_detections` should now also be published. Just like the raw image, you can display this rectified version with:
```bash
ros2 run rqt_image_view rqt_image_view
```
<br>

### AprilTag Node
You can start the AprilTag detection with the launch file provided in the `peripherals` package:
```bash
ros2 launch peripherals apriltag.launch.py
```
This launch file references the `apriltag_config.yaml` located in the `config` folder of the `peripherals` package. This config file specifies the used detection algorithm and the tag-family. Every tag that can be detected must also be listed here. The 6 Tags of the 6 sides of the provided cube are already added to this file.\
The AprilTag detection should now be working. To verify, place the cube in front of the camera and listen to the `/apriltag_detection` topic:
```bash
ros2 topic echo /apriltag_detections
```
<br>

![ImgCube](images/cubes.jpg)
*Cubes of different color with the AprilTags on the sides. All cubes have the same AprilTags.*

## Test the LIDAR
To test the LIDAR, you need the `controller` node again:
```bash
ros2 launch controller controller.launch.py
```
Now you can launch the `ldlidar_node` present in the `ldrobot-lidar-ros2` folder:
```bash
ros2 launch ldlidar_node ldlidar.launch.py
```
You see the following topics added to your topic list:
```bash
matthias@matthiasT15:~$ ros2 topic list
/bond
/diagnostics
/ldlidar_node/scan
/ldlidar_node/transition_event
/parameter_events
/rosout
```
The `/ldlidar_node/scan` is the important one. 
Open `rivz2` either on the Raspberry Pi 5 or a different computer in the same network running `ROS2` with:
```bash
rviz2 
```
In `rviz2` click on *map* next to *Fixed Frame* in the *Global Options* on the left side. Select *base_footprint* from the dropdown menu. Then click on *add* in the lover left corner and select *LaserScan* from the list. Press *OK*. *LaserScan* should now appear in the left list in red. Click on it to open a dropdown. Click right of *Topic* in the whitespace. An empty dropdown menu should appear. Select `/ldlidar_node/scan` from this menu. The live LIDAR points should now be displayed in the middle. By selecting *Points* next to the *Style* field, you can make the points better visible.
![Alt Text](images/rviz_lidar_points.png "Rviz Lidar Points")
<br>
<br>

## Test SLAM
**SLAM** is short for *Simultaneous Localization and Mapping* and describes the process of mapping one's surroundings while localizing oneself inside this map. It is key for autonomous navigation in an unknown environment. The `ROS2` package `slam_toolbox` can be used to perform this using live LIDAR data and a complete transformation tree. This tree describes the position of the LIDAR in respect to the main coordinate origin of the robot. This transformation tree is implemented in the `controller` package.
1. Launch the `controller` node: (if not already running)
```bash
ros2 launch controller controller.launch.py
```
2. Launch the ldlidar_node: (if not already running)
```bash
ros2 launch ldlidar_node ldlidar.launch.py
```
3. Launch the `slam_toolbox` with a custom launch file located inside the `orchestrator_launch` package:
```bash
ros2 launch orchestrator_launch slam_toolbox.launch.py
```
4. Launch rviz2 either on the Raspberry Pi 5 or on a computer running `ROS2` inside the same network:
```bash
rviz2
```
5. Click on *Add* in the lower left corner and select *Map* from the list. Then press *OK*. Now select `/map` as the *Topic* in the dropdown Menu under the newly created *Map* entry in the left list. The beginnings of a map should now be visible in the middle of the screen.
6. To add the position of the robot inside the map, click *Add* again and select *TF* from the list. Then click *OK*. The position and orientation should now be displayed. Under *Frames*, you can choose which "position" you want to see. Only selecting *base_footprint* may be the most sensible. 
![Alt Text](images/rviz_slam.png "Rviz Lidar Points")
7. You can now launch the joystick_control from the `peripherals` package again:
```bash
ros2 launch peripherals joystick_control.launch.py
```
You should now be able to move around with the robot while the map is continuously updated.
<br>
<br>

# Quality of Life Additions and Some Tips

## Terminator
As you may already noticed, you often have to work with many terminals in paralel. A tiling terminal emulator can help with this. `Terminator` is a nice choice.
```bash
sudo apt install terminator
```
With
   - `strg`+`shift`+`e` you can split the terminal vertically.
   - `strg`+`shift`+`o` you can split the terminal horizontally.
<br>

## SSH Setup
* For easier development, connecting to the Raspberry Pi 5 via SSH is strongly recommended. For this, the Raspberry Pi 5 needs to be connected to the same network as the device from which you want to access the Raspberry Pi 5 (Eduroam does not work).

SSH is not standard installed on Ubuntu 24.04, so we need to install it:
```bash
sudo apt update
sudo apt install openssh-server -y
```
Then, run: 
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```
To verify that ssh is running, run:
```bash
sudo systemctl status ssh
```
It should say **active (running)**.

Look up the IP address from the Raspberry Pi 5 with:
```bash
hostname -I
```
**Make sure**  to use a capital I.

Now you can connect to the Raspberry Pi 5 from your other computer:
```bash
ssh user@IP-address
```
**Replace** `user` with the username of your robot and `IP-address` with the IP-address of your Raspberry Pi 5. 

* Additionally, installing `sshfs` on your machine will allow you to mount  remote file systems. This way you could for example mount the `workspace` folder of your Raspberry Pi 5 in your file system and conveniently edit files with any code editor you like on your machine.

1. Install `sshfs` on your machine:
```bash
sudo apt install sshfs
```
2. Mount a remote folder:
```bash
sshfs user@IP-address:/remote/file/path /local/file/path
```
Of course **replace** `user` `IP-adress` `/remote/file/path` and `local/file/path` with your specific data. 
   - `/remote/file/path` is the path on the remote machine you want to make accessible from your machine
   - `local/file/path` is the file path on your local machine you want to mount the remote folder in. Creating a special folder like `~/remote_code` may be sensible.
<br>

## rviz2
Rviz2 is a visualization tool for ROS2 that allows you to view sensor data, robot models, and transformations in real time.
It can be launched via:
```bash
rviz2
```
Some of the data from the ROS2 topics can be visualized via rviz2, the following are especially relevant.
* TF - all of the transformations between the robot's parts (**NOTE: ** the transformation to the camera uses a depth camera and is incorrect, moving the camera around using the servos is also not accounted for).
* Robot Model - displays the robot with the robot's URDF model (**NOTE: ** to properly display the robot, you need the stl files located in this repository under ros2_ws/src/simulations/mentorpi_description/meshes)
* Odometry (odom) - displays the robot's movement
* Laser Scan - visualizes the LIDAR sensor data
* map - displays the generated SLAM map
<br>

## Multiple Robots on the Same Network
ROS2 topics and nodes are accessible over the entire network. When using multiple robots in the same network, you may want to separate the networks from each other. This is easily achieved via the `ROS_DOMAIN_ID`. All ROS2 clients with the same exported ID can see each other. The default ID is `0`.
You can change the ID of your ROS2 client for example to id `10` with:
```bash
export ROS_DOMAIN_ID=10
```
Please use your group number as ROS_DOMAIN_ID as all groups will be using the same wifi network on site and add this environment variable to the .bashrc file. 

## About Standardization
Most things in ROS2 are standardized. This means there probably is a "standard way" to expose, for example, a topic on which velocity requests can be made. For this specific task, the topic is called `/cmd_vel` and has the type `geometry_msgs/Twist`. This standard naming and typing is mostly adhered to in this workspace. This also allows, for example, easy integration with standard ROS2 packages like `slam_toolbox`. This package expects odometry information to be published on `/odom` and a laser scan published on `/scan`. Both of these, of course, also have an expected type. Because the `controller` package that exposes the `/odom` topic adheres to this standard and `ldrobot-lidar-ros2` almost adheres to this (only the topic name needs to be changed via the launch script), integration is fairly easy. All of this is to say, if you also adhere to the sometimes unwritten rules of standard naming and typing, you can make your life a lot easier. 

## How To Start Development
If you are ready to implement some code, here are some general tips and ideas to get you started.\
* If you want to implement some functionality, it makes probably sense to organize it in a new package, with
```bash
ros2 pkg create <package_name> --build-type ament_cmake
```
you can create a new **cmake** package, and with
```bash
ros2 pkg create <package_name> --build-type ament_python
```
you create a new **python** package. **Make sure** you are inside your build folder (`ros_ws/src`), before entering these commands.

* If you installed a package via the package manager, it is installed in `/opt/ros/jazzy/share`. Some standard launch and parameter files are usually given here. If you want to use such a "standard package" you most likely need to at least adjust the launch script and the parameter files. It is best practice to **not** modify installed packages in `/opt/ros/...`, instead you should organize them inside a package of your own workspace. In our structure, both the `orchestrator_launch` and the `peripherals` package are good places for this. You can copy the given launch scripts and parameter files from `/opt/ros/jazzy/share/package_name/` into one of these packages and launch the installed packages from there.


# Contributions
We thank M. Schmiegel, J. Baur and P. Bodynek for helping with this repository.
