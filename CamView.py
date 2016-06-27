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

        self.kernel_size = (7,7)            # default value for Kernel Size
        self.std_Deviation = 1              # default value for Std Deviation
        self.h_threshold1 = 90              # default value for Hysteresis Threshold 1
        self.h_threshold2 = 110             # default value for Hysteresis Threshold 2
        self.sigma = .33                    # default value for Sigma

        self.show_canny_image = True        # automatically show processed canny image by default

        home_dir = os.path.expanduser("~")                  # get home directory

        # define all directory locations
        x_dir = home_dir + "/Pictures/CamView/1-captured"   # index file directory
        i_dir = home_dir + "/Pictures/CamView/1-captured"   # capture image directory
        b_dir = home_dir + "/Pictures/CamView/2-blurred"    # blurred images directory
        g_dir = home_dir + "/Pictures/CamView/3-grayscale"  # grayscale images directory
        c_dir = home_dir + "/Pictures/CamView/4-processed"  # canny edge image directory

        # define all file names
        self.index_dir = x_dir + "/.index"                              # index file
        self.image_dir = i_dir + "/img_{}.png"                          # captured images from Cam
        self.blur_dir = b_dir + "/blur_{}_{}:{}.png"                    # blurred images
        self.gray_dir = g_dir + "/gray_{}_{}:{}.png"                    # grayscale images
        self.canny_dir = c_dir + "/canny_{}_{}:{}-{}:{}.png"            # images processed by canny edge detection
        self.auto_canny_dir = c_dir + "/canny_{}_{}:{}-{}:{}-{}.png"    # images processed by canny edge detection

        # make sure a folder exists to save captured images
        if not os.path.exists(i_dir):                       # check if folder exists
            os.makedirs(i_dir)                              # create folder if it doesn't
        else:                                               # else:
            pass                                            # do nothing

        # make sure a folder exists to save blurred images
        if not os.path.exists(b_dir):                       # check if folder exists
            os.makedirs(b_dir)                              # create folder if it doesn't
        else:                                               # else:
            pass                                            # do nothing

        # make sure a folder exists to save grayscale images
        if not os.path.exists(g_dir):                       # check if folder exists
            os.makedirs(g_dir)                              # create folder if it doesn't
        else:                                               # else:
            pass                                            # do nothing

        # make sure a folder exists to save canny edge images
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

    def kernelSize(self, val):                              # update value from kernel size spinbox
        self.kernel_size = (val,val)                        # pass value to Kernel size variable

    def stdDeviation(self, val):                            # update value from Standard Deviation spinbox
        self.std_Deviation = val                            # pass value to Std Deviation variable

    def hysteresisThreshold_1(self, val):                   # update value from hysteresisThreshold_1 spinbox
        self.h_threshold1 = val                             # pass value to Threshold 1 variable

    def hysteresisThreshold_2(self, val):                   # update value from hysteresisThreshold_2 spinbox
        self.h_threshold2 = val                             # pass value to Threshold 2 variable

    def sigmaValue(self, val):                              # update value from sigma spinbox
        self.sigma = val                                    # pass value to sigma variable

        # Perform Canny Edge detection on latest image captured
        # This function is called by the 'Canny Edges' button
    def cannyEdges(self):

        img_name = self.image_dir.format(self.img_index)    # name of latest image captured

        if os.path.exists(img_name):                        # check if an image exists

            canny = cv2.imread(img_name)                    # read latest image captured

            # Blur Image
            k_size = self.kernel_size
            std_dev = self.std_Deviation

            k_size_str = str(k_size).replace(" ", "")                                   # remove blank spaces in k_size

            blur_img_name = self.blur_dir.format(self.img_index, k_size_str, std_dev)   # name of blurred image
            blur = cv2.GaussianBlur(canny, k_size, std_dev)                             # perform gaussian blur
            cv2.imwrite(blur_img_name, blur)                                            # writes blurred image to directory

            # Grayscale Image
            gray_img_name = self.gray_dir.format(self.img_index, k_size_str, std_dev)   # name of grayscale image
            gray  = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)                              # grayscale blurred image
            cv2.imwrite(gray_img_name, gray)                                            # writes grayscale image to directory

            thr_1 = self.h_threshold1
            thr_2 = self.h_threshold2

            # Determine the name of canny image to be processed
            canny_name = self.canny_dir.format(self.img_index, k_size_str, std_dev, thr_1, thr_2)

            # Canny Edge detection
            edges = cv2.Canny(gray, thr_1, thr_2)
            plt.imshow(cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))
            cv2.imwrite(canny_name, edges)                                  # writes image on the directory
            print("Canny Edge detection image saved as " + canny_name)      # send message to terminal

            if self.show_canny_image:                       # if Checkbox is checked
                img = Image.open(canny_name)                # open processed image
                img.show()                                  # and display it
            else:
                pass

        else:                                               # if the image does not exists
            print("WARNING: No image available.")           # show message in terminal

    def autoCannyEdges(self):

        img_name = self.image_dir.format(self.img_index)    # name of latest image captured

        if os.path.exists(img_name):                        # check if an image exists

            canny = cv2.imread(img_name)                    # read latest image captured

            # Blur Image
            k_size = self.kernel_size
            std_dev = self.std_Deviation

            k_size_str = str(k_size).replace(" ", "")                                   # remove blank spaces in k_size

            blur_img_name = self.blur_dir.format(self.img_index, k_size_str, std_dev)   # name of blurred image
            blur = cv2.GaussianBlur(canny, k_size, std_dev)                             # perform gaussian blur
            cv2.imwrite(blur_img_name, blur)                                            # writes blurred image to directory

            # Grayscale Image
            gray_img_name = self.gray_dir.format(self.img_index, k_size_str, std_dev)   # name of grayscale image
            gray  = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)                              # grayscale blurred image
            cv2.imwrite(gray_img_name, gray)                                            # writes grayscale image to directory

            sigma = self.sigma
            v = np.median(gray)                                                         # compute the median of the single channel pixel intensities

            thr_1 = int(max(0, (1.0 - sigma) * v))
            thr_2 = int(min(255, (1.0 + sigma) * v))

            # Determine the name of canny image to be processed
            canny_name = self.auto_canny_dir.format(self.img_index, k_size_str, std_dev, thr_1, thr_2, sigma)

            # Canny Edge detection
            edges = cv2.Canny(gray, thr_1, thr_2)
            plt.imshow(cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))
            cv2.imwrite(canny_name, edges)                                  # writes image on the directory
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

		extractAction1 = QtGui.QAction("&Quit", self)
		extractAction1.setShortcut("Ctrl+Q")
		extractAction1.setStatusTip('Leave the App')
		extractAction1.triggered.connect(self.close_application)

		extractAction2 = QtGui.QAction("&Gaussian Filter", self)
		extractAction2.setStatusTip('Swipe all values in the Gaussian Filter')
		extractAction2.triggered.connect(self.close_application)

		extractAction3 = QtGui.QAction("&Hysteresis Threshold", self)
		extractAction3.setStatusTip('Swipe all values in the Hysteresis Threshold')
		extractAction3.triggered.connect(self.close_application)

		extractAction4 = QtGui.QAction("&Aperture Size", self)
		extractAction4.setStatusTip('Swipe all values for Sobel operator')
		extractAction4.triggered.connect(self.close_application)

		self.statusBar()

		mainMenu = self.menuBar()

		fileMenu1 = mainMenu.addMenu('&File')
		fileMenu1.addAction(extractAction1)

		fileMenu2 = mainMenu.addMenu('&Swipe')
		fileMenu2.addAction(extractAction2)
		fileMenu2.addAction(extractAction3)
		fileMenu2.addAction(extractAction4)

		# This is a stub. Need to complete the GroupBox for the 'Capture' section
		TracParamFrame = QtGui.QGroupBox(self)
		TracParamFrame.setTitle("Capture")
		TracParamFrame.move(50, 35)

		# This is a stub. Need to complete the GroupBox for the 'Edge Detection' section
		TracParamFrame = QtGui.QGroupBox(self)
		TracParamFrame.setTitle("Edge Detection")
		TracParamFrame.resize(200,50)
		TracParamFrame.move(245, 35)

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
		btn.resize(115,50)
		btn.move(410,75)

		# Automatic Canny Edge button
		btn = QtGui.QPushButton("Auto Detect", self)
		btn.clicked.connect(self.capture.autoCannyEdges)
		btn.resize(115,50)
		btn.move(410,140)

		# Checkbox to automatically open canny image after processing
		cbx = QtGui.QCheckBox("Open Image", self)
		cbx.resize(115,40)
		cbx.move(410, 190)
		cbx.toggle()
		cbx.stateChanged.connect(self.capture.cannyCheckBox)

		klab = QtGui.QLabel("Kernel Size:", self)
		klab.move(210, 75)

		klab = QtGui.QLabel("Std Deviation:", self)
		klab.move(195, 110)

		tlab = QtGui.QLabel("Threshold 1:", self)
		tlab.move(205, 145)

		tlab = QtGui.QLabel("Threshold 2:", self)
		tlab.move(205, 180)

		tlab = QtGui.QLabel("Sigma:", self)
		tlab.move(248, 215)

		# Spinbox for Kernel Size for Gaussian filter
		spn1 = QtGui.QSpinBox(self)
		spn1.move(315, 75)
		spn1.setFixedWidth(70)
		spn1.setRange(1,9)
		spn1.setValue(7)
		spn1.setSingleStep(2)
		spn1.valueChanged.connect(self.capture.kernelSize)

		# Spinbox for Standard Deviation for Gaussian filter
		spn2 = QtGui.QSpinBox(self)
		spn2.move(315, 110)
		spn2.setFixedWidth(70)
		spn2.setRange(1,10)
		spn2.setValue(1)
		spn2.valueChanged.connect(self.capture.stdDeviation)

		# Spinbox for Hysteresis Threshold 1 values
		spn3 = QtGui.QSpinBox(self)
		spn3.move(315, 145)
		spn3.setFixedWidth(70)
		spn3.setRange(0,500)
		spn3.setValue(90)
		spn3.valueChanged.connect(self.capture.hysteresisThreshold_1)

		# Spinbox for Hysteresis Threshold 2 values
		spn4 = QtGui.QSpinBox(self)
		spn4.move(315, 180)
		spn4.setFixedWidth(70)
		spn4.setRange(0,500)
		spn4.setValue(110)
		spn4.valueChanged.connect(self.capture.hysteresisThreshold_2)

		# Spinbox for sigma values
		spn5 = QtGui.QDoubleSpinBox(self)
		spn5.move(315, 215)
		spn5.setFixedWidth(70)
		spn5.setRange(.00,.99)
		spn5.setValue(.33)
		spn5.setSingleStep(0.01)
		spn5.valueChanged.connect(self.capture.sigmaValue)

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
