import os.path                      # libraries for pathnames
import cv2                          # libraries for camera and processing
from PyQt4 import QtGui, QtCore     # libraries for GUI implementation
import sys                          # system specific functions
from PIL import Image               # for opening images

# libraries for image processing
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

class Capture():
    def __init__(self):

        self.capturing = False
        self.c = cv2.VideoCapture(0)

        self.pixel_threshold = 80           # default value for pixel threshold 80
        self.pixel_max_size = 255           # default value for max pixel size 255
        self.kernel_size = (7,7)            # default value for Kernel Size
        self.std_Deviation = 1              # default value for Std Deviation
        self.h_threshold1 = 90              # default value for Hysteresis Threshold 1
        self.h_threshold2 = 110             # default value for Hysteresis Threshold 2

        self.show_canny_image = True        # automatically show processed canny image by default

        home_dir = os.path.expanduser("~")                  # get home directory

        # define all directory locations
        x_dir = home_dir + "/Pictures/CamView/captured"     # index file directory
        i_dir = home_dir + "/Pictures/CamView/captured"     # capture image directory
        c_dir = home_dir + "/Pictures/CamView/processed"    # processed image directory

        # define all file names
        self.index_dir = x_dir + "/.index"                          # index file
        self.image_dir = i_dir + "/img_{}.png"                      # captured images from Cam
        self.canny_dir = c_dir + "/canny_{}_{}:{}-{}:{}-{}:{}.png"  # images processed by canny edge detection

        # make sure a folder exists to save captured images
        if not os.path.exists(i_dir):                       # check if folder exists
            os.makedirs(i_dir)                              # create folder if it doesn't
        else:                                               # else:
            pass                                            # do nothing

        # make sure a folder exists to save processed images
        if not os.path.exists(c_dir):                       # check if folder exists
            os.makedirs(c_dir)                              # create folder if it doesn't
        else:                                               # else:
            pass                                            # do nothing

        # make sure index file exists
        if not os.path.isfile(self.index_dir):              # check if index file exists
            self.index_file = open(self.index_dir, 'w')     # create file if it doesn't
            self.index_file.write(str(0))                   # make index 0 by default
            self.index_file.close()                         # close file (save changes)
        else:                                               # else:
            pass                                            # do nothing

        self.index_file = open(self.index_dir)              # open index file in read mode
        self.img_index = int(self.index_file.read())        # determine 'img_index' from file
        self.index_file.close()                             # close file

        # Starts image capturing
        # This function is called by the 'Start' button
    def startCapture(self):
        print ("pressed Start")
        self.capturing = True
        cap = self.c
        while(self.capturing):
            ret, frame = cap.read()
            cv2.imshow("Capture", frame)                    # show capture window
            cv2.moveWindow("Capture", 1275, 0)              # move window to desired location
            cv2.waitKey(5)
        cv2.destroyAllWindows()

        # Stops image capturing
        # This function is called by the 'Stop' button
    def endCapture(self):
        print ("pressed Stop")
        self.capturing = False

    def quitCapture(self):
        print ("pressed Quit")
        cap = self.c
        cv2.destroyAllWindows()
        cap.release()
        QtCore.QCoreApplication.quit()

        # Saves a captured image on specified folder
        # This function is called by the 'Save Picture' button
    def savePicture(self):
        cap = self.c
        ret, frame = cap.read()
        self.img_index += 1                                 # updates index variable (+1)
        img_name = self.image_dir.format(self.img_index)    # sets name + index and directory of captured image
        cv2.imwrite(img_name, frame)                        # saves image to directory
        print("Saved Picture as {}".format(img_name))       # send message to terminal

        # updates index file
        self.index_file = open(self.index_dir, 'r+')        # open index file in read/write mode
        self.index_file.seek(0)                             # move cursor to begining of file
        self.index_file.write(str(self.img_index))          # updates index number in file (+1)
        self.index_file.close()                             # close file (saves to file)

        # Resets Image Index
        # This function is called by the 'Reset Index' button
    def resetIndex(self):
        self.index_file.close()                             # close index file (assumes it's already open)
        self.index_file = open(self.index_dir, 'w')         # open index file in write mode
        self.index_file.seek(0)                             # move cursor to begining of file
        self.index_file.write(str(0))                       # write '0' on file
        self.index_file.close()                             # close file (save changes)
        self.index_file = open(self.index_dir, 'r+')        # re-opens file in read/write mode
        self.img_index = 0                                  # resets index variable to 0
        print("WARNING: Image index reset!")                # warns about index being reset

    def cannyCheckBox(self):                                # Toogle value of show_canny_image
        self.show_canny_image = not self.show_canny_image   # Called by the 'Open Image' checkbox

    def pixelThreshold(self, val):                          # update value from pixel threshold spinbox
        self.pixel_threshold = val                          # pass value to pixel threshold variable

    def pixelMaxSize(self, val):                            # update value from kernel size spinbox
        self.pixel_max_size = val                           # pass value to pixel max size variable

    def kernelSize(self, val):                              # update value from kernel size spinbox
        self.kernel_size = (val,val)                        # pass value to Kernel size variable

    def stdDeviation(self, val):                            # update value from Standard Deviation spinbox
        self.std_Deviation = val                            # pass value to Std Deviation variable

    def hysteresisThreshold_1(self, val):                   # update value from hysteresisThreshold_1 spinbox
        self.h_threshold1 = val                             # pass value to Threshold 1 variable

    def hysteresisThreshold_2(self, val):                   # update value from hysteresisThreshold_2 spinbox
        self.h_threshold2 = val                             # pass value to Threshold 2 variable

        # Perform Canny Edge detection on latest image captured
        # This function is called by the 'Canny Edges' button
    def cannyEdges(self):

        img_name = self.image_dir.format(self.img_index)    # name of latest image captured

        if os.path.exists(img_name):                        # check if an image exists

            k_size = self.kernel_size
            std_dev = self.std_Deviation

            canny = cv2.imread(img_name)                    # read latest image captured
            blur = cv2.GaussianBlur(canny, k_size, std_dev) # perform gaussian blur

            p_thr = self.pixel_threshold
            p_max = self.pixel_max_size

            # Preprocess Image
            blur_grey  = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)           # grayscale blurred image
            _, canny_thr = cv2.threshold(blur_grey, p_thr, p_max, cv2.THRESH_BINARY)  # find binary image with thresholding
            plt.imshow(cv2.cvtColor(canny_thr, cv2.COLOR_GRAY2RGB))

            thr_1 = self.h_threshold1
            thr_2 = self.h_threshold2

            # Determine the name of canny image to be processed
            k_size_str = str(k_size).replace(" ", "")       # remove blank spaces in k_size
            canny_name = self.canny_dir.format(self.img_index, p_thr, p_max, k_size_str, std_dev, thr_1, thr_2)

            # Canny Edge detection
            edges = cv2.Canny(blur_grey, thr_1, thr_2)
            plt.imshow(cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))
            cv2.imwrite(canny_name, edges)                                  # writes image on the folder
            print("Canny Edge detection image saved as " + canny_name)      # send message to terminal

            if self.show_canny_image:                       # if Checkbox is checked
                img = Image.open(canny_name)                # open processed image
                img.show()                                  # and display it
            else:
                pass

        else:                                               # if the image does not exists
            print("WARNING: No image available.")           # show message in terminal

class Window(QtGui.QMainWindow):

	# Initializations
	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 550, 300)
		self.setWindowTitle("CamView")
		self.setWindowIcon(QtGui.QIcon("./icons/opencv_logo.png"))

		extractAction = QtGui.QAction("&Quit", self)
		extractAction.setShortcut("Ctrl+Q")
		extractAction.setStatusTip('Leave the App')
		extractAction.triggered.connect(self.close_application)

		self.statusBar()

		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(extractAction)

		# This is a stub. Need to complete the GroupBox for the 'Capture' section
		TracParamFrame = QtGui.QGroupBox(self)
		TracParamFrame.setTitle("Capture")
		TracParamFrame.move(50, 35)

		# This is a stub. Need to complete the GroupBox for the 'Canny Edge' section
		TracParamFrame = QtGui.QGroupBox(self)
		TracParamFrame.setTitle("Canny Edge Detection")
		TracParamFrame.resize(200,50)
		TracParamFrame.move(275, 35)

		self.home()

	# Views
	def home(self):

		# Start capture button
		self.capture = Capture()
		btn = QtGui.QPushButton("Start", self)
		btn.clicked.connect(self.capture.startCapture)
		btn.resize(55,50)                                # Use 'btn.resize(btn.sizeHint())' for minimum size
		btn.move(25,75)

		# Stop capture button
		btn = QtGui.QPushButton("Stop", self)
		btn.clicked.connect(self.capture.endCapture)
		btn.resize(55,50)
		btn.move(85,75)

		# Save Picture button
		btn = QtGui.QPushButton("Save Picture", self)
		btn.clicked.connect(self.capture.savePicture)
		btn.resize(115,50)
		btn.move(25,140)

		# Reset Index button
		btn = QtGui.QPushButton("Reset Index", self)
		btn.clicked.connect(self.capture.resetIndex)
		btn.resize(115,50)
		btn.move(25,205)

		# Vertical divider for the Capture and Processing sections
		#div = QtGui.QFrame(self)
		#div.setFrameStyle(self.VLine)
		#div.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Expanding)

		# Canny Edge button
		btn = QtGui.QPushButton("Detect Edges", self)
		btn.clicked.connect(self.capture.cannyEdges)
		btn.move(410,75)
		btn.resize(115,50)

		# Checkbox to automatically open canny image after processing
		cbx = QtGui.QCheckBox("Open Image", self)
		cbx.move(410, 125)
		cbx.resize(115,40)
		cbx.toggle()
		cbx.stateChanged.connect(self.capture.cannyCheckBox)

		klab = QtGui.QLabel("Pixel Threshold:", self)
		klab.move(180, 65)
		klab.setFixedWidth(120)

		klab = QtGui.QLabel("Pixel Max Size:", self)
		klab.move(190, 95)
		klab.setFixedWidth(120)

		klab = QtGui.QLabel("Kernel Size:", self)
		klab.move(210, 135)

		klab = QtGui.QLabel("Std Deviation:", self)
		klab.move(195, 165)

		tlab = QtGui.QLabel("Threshold 1:", self)
		tlab.move(205, 205)

		tlab = QtGui.QLabel("Threshold 2:", self)
		tlab.move(205, 235)

		# Spinbox for Pixel Threshold
		spn1 = QtGui.QSpinBox(self)
		spn1.move(315, 65)
		spn1.setFixedWidth(70)
		spn1.setRange(0,500)
		spn1.setValue(80)
		spn1.valueChanged.connect(self.capture.pixelThreshold)

		# Spinbox for Pixel Maximim Size
		spn1 = QtGui.QSpinBox(self)
		spn1.move(315, 95)
		spn1.setFixedWidth(70)
		spn1.setRange(0,500)
		spn1.setValue(255)
		spn1.valueChanged.connect(self.capture.pixelMaxSize)

		# Spinbox for Kernel Size for Gaussian filter
		spn1 = QtGui.QSpinBox(self)
		spn1.move(315, 135)
		spn1.setFixedWidth(70)
		spn1.setRange(0,500)
		spn1.setValue(7)
		spn1.valueChanged.connect(self.capture.kernelSize)

		# Spinbox for Standard Deviation for Gaussian filter
		spn2 = QtGui.QSpinBox(self)
		spn2.move(315, 165)
		spn2.setFixedWidth(70)
		spn2.setRange(0,500)
		spn2.setValue(1)
		spn2.valueChanged.connect(self.capture.stdDeviation)

		# Spinbox for Hysteresis Threshold 1 values
		spn3 = QtGui.QSpinBox(self)
		spn3.move(315, 205)
		spn3.setFixedWidth(70)
		spn3.setRange(0,500)
		spn3.setValue(90)
		spn3.valueChanged.connect(self.capture.hysteresisThreshold_1)

		# Spinbox for Hysteresis Threshold 2 values
		spn4 = QtGui.QSpinBox(self)
		spn4.move(315, 235)
		spn4.setFixedWidth(70)
		spn4.setRange(0,500)
		spn4.setValue(110)
		spn4.valueChanged.connect(self.capture.hysteresisThreshold_2)

		self.show()

	# Methods
	def close_application(self):
		choice = QtGui.QMessageBox.question(self, 'Extract!', "Exit application?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:
			print("Program terminated by user")
			sys.exit()
		else:
			pass

def run():
	app = QtGui.QApplication(sys.argv)
	GUI = Window()
	sys.exit(app.exec_())

run()
