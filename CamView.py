import os.path                      # libraries for pathnames
import cv2                          # libraries for camera and processing
from PyQt4 import QtGui, QtCore     # libraries for GUI implementation
import sys                          # system specific functions

# libraries for image processing
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

class Capture():
    def __init__(self):

        self.capturing = False
        self.c = cv2.VideoCapture(0)

        home_dir = os.path.expanduser("~")                  # get home directory

        # define all directory locations
        x_dir = home_dir + "/Pictures/CamView/captured"     # index file directory
        i_dir = home_dir + "/Pictures/CamView/captured"     # capture image directory
        c_dir = home_dir + "/Pictures/CamView/processed"    # processed image directory

        # define all file names
        self.image_dir = i_dir + "/img_{}.png"              # captured images from Cam
        self.canny_dir = c_dir + "/canny_{}.png"            # images processed by canny edge detection
        self.index_dir = x_dir + "/.index"                  # index file

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
        print ("pressed start")
        self.capturing = True
        cap = self.c
        while(self.capturing):
            ret, frame = cap.read()
            cv2.imshow("Capture", frame)            # show capture window
            cv2.moveWindow("Capture", 1275, 0)      # move capture window to desired location
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

        # Perform Canny Edge detection on latest image captured
        # This function is called by the 'Canny Edges' button
    def cannyEdges(self):

        img_name = self.image_dir.format(self.img_index)    # name of latest image captured

        # make sure the captured image exists
        if os.path.exists(img_name):            # check if an image exists

            canny = cv2.imread(img_name)        # read latest image captured

            # Preprocess Image
            canny_pre  = cv2.cvtColor(cv2.GaussianBlur(canny, (7,7), 0), cv2.COLOR_BGR2GRAY)    # preprocess by blurring and grayscale
            _, canny_thresh = cv2.threshold(canny_pre, 80, 255, cv2.THRESH_BINARY)              # find binary image with thresholding
            plt.imshow(cv2.cvtColor(canny_thresh, cv2.COLOR_GRAY2RGB))

            # Canny Edge detection
            canny_edges = cv2.Canny(canny_pre, threshold1=90, threshold2=110)
            plt.imshow(cv2.cvtColor(canny_edges, cv2.COLOR_GRAY2RGB))
            cv2.imwrite(self.canny_dir.format(self.img_index), canny_edges)     # writes image on the folder
            print("Canny Edge detection image saved as {}".format(img_name))    # send message to terminal

        else:                                       # if the image does not exists
            print("WARNING: Image not present.")    # show message in terminal
            print("Please capture an image")

class Window(QtGui.QMainWindow):

	# Initializations
	def __init__(self):
		super(Window, self).__init__()
		self.setGeometry(50, 50, 500, 300)
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

		self.home()

	# Views
	def home(self):

		# Start capture button
		self.capture = Capture()
		btn = QtGui.QPushButton("Start", self)
		btn.clicked.connect(self.capture.startCapture)
		btn.resize(55,50)                                # set button size. Use 'btn.resize(btn.sizeHint())' for minimum size
		btn.move(25,50)

		# Stop capture button
		btn = QtGui.QPushButton("Stop", self)
		btn.clicked.connect(self.capture.endCapture)
		btn.resize(55,50)
		btn.move(85,50)

		# Save Picture button
		btn = QtGui.QPushButton("Save Picture", self)
		btn.clicked.connect(self.capture.savePicture)
		btn.resize(115,50)
		btn.move(25,125)

        # Reset Index button
		btn = QtGui.QPushButton("Reset Index", self)
		btn.clicked.connect(self.capture.resetIndex)
		btn.resize(115,50)
		btn.move(25,200)

        # Canny Edge button
		btn = QtGui.QPushButton("Canny Edges", self)
		btn.clicked.connect(self.capture.cannyEdges)
		btn.resize(115,50)
		btn.move(200,50)

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
