# CamView

This software provides a simple gui to capture images on a webcam using PyQt4 and OpenCV3.

It also enables the user to use 'Canny Edge' detection on the images captured.

All captured and processed images are automatically saved to separate directories on ~/Pictures/CamView. The directories will be created if they do not exist. It is assumed the software will be run on a Linux system.

# Capture Section

The capture section is design to work similar to a point-and-shoot camera:

By pressing the 'Save' button, it saves the captured image to the designated folder. An image index is appended to the end of each of the new images saved.

# Edge Detection Section

Detect Edges button - performs Canny Edge detection according to the parameters indicated by Kernel Size, Std Deviation, Threshold 1 & 2.

Auto Detect button - automatically calculates thresholds 1 and 2 using the Sigma parameter.

For future use:

In order to set up the development environment on a new system, it is 
recommended to follow these steps:

1) Install Anaconda 3.5 from the site:
	https://www.continuum.io/downloads

2) Install OpenCV3 through Anaconda by typing in a terminal:
	conda install -c https://conda.anaconda.org/menpo opencv3 

3) Install Tensorflow through Anaconda by typing in a terminal:
	conda install -c https://conda.anaconda.org/jjhelmus tensorflow

4) Install git-cola or other git client. To install git-cola from the terminal:
	sudo apt-get install git-cola

Send any questions to eporcell@protonmail.ch
