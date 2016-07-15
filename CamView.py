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

        self.show_canny_image = True        # open canny image by default
        self.manual_canny = False           # calculate threshold values automatically by default

        home_dir = os.path.expanduser("~")                      # get home directory

        # define all directory locations
        a_dir = home_dir + "/Pictures/CamView/1-captured"       # index file and capture image directory
        b_dir = home_dir + "/Pictures/CamView/2-blurred"        # blurred images directory
        c_dir = home_dir + "/Pictures/CamView/3-processed"      # canny edge image directory

        # define all file names
        self.index_dir = a_dir + "/.index"                      # index file
        self.img_dir = a_dir + "/img_{}.png"                    # captured images from Cam
        self.blur_dir = b_dir + "/blur_{}_{}:{}.png"            # blurred images
        self.ref_dir = a_dir + "/REF.png"                       # background reference image
        self.canny_dir = c_dir + "/canny_{}_{}:{}-{}-{}:{}.png" # images processed by canny edge detection

        # make sure a folder exists to save captured images
        if not os.path.exists(a_dir):                       # check if folder exists
            os.makedirs(a_dir)                              # create folder if it doesn't
        else:                                               # else:
            pass                                            # do nothing

        # make sure a folder exists to save blurred images
        if not os.path.exists(b_dir):                       # check if folder exists
            os.makedirs(b_dir)                              # create folder if it doesn't
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

        # Starts image capturing. Called by the 'Start' button.
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

        # Stops image capturing. Called by the 'Stop' button.
    def endCapture(self):
        print ("pressed Stop")
        self.capturing = False

    def quitCapture(self):
        print ("pressed Quit")
        cap = self.c
        cv2.destroyAllWindows()
        cap.release()
        QtCore.QCoreApplication.quit()

        # Saves a captured image on specified folder. Called by 'takePicture'.
    def savePicture(self):
        cap = self.c
        ret, frame = cap.read()
        self.img_index += 1                                 # updates index variable (+1)
        img_name = self.img_dir.format(self.img_index)      # sets name + index and directory of captured image
        cv2.imwrite(img_name, frame)                        # saves image to directory
        print("Saved Picture as {}".format(img_name))       # send message to terminal

        # updates index file
        self.index_file = open(self.index_dir, 'r+')        # open index file in read/write mode
        self.index_file.seek(0)                             # move cursor to begining of file
        self.index_file.write(str(self.img_index))          # updates index number in file (+1)
        self.index_file.close()                             # close file (saves to file)

    def saveBackground(self):
        cap = self.c
        ret, frame = cap.read()
        bck_name = self.ref_dir
        cv2.imwrite(bck_name, frame)                        # saves image to directory
        print("Saved Picture as {}".format(bck_name))       # send message to terminal

        # Resets Image Index. Called by the 'Reset Index' button.
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

    def autoCannyCheckBox(self):                            # Toogle value of manual_canny
        self.manual_canny = not self.manual_canny           # Called by the 'Manual Threshold' checkbox

    def kernelSize(self, val):                              # update value from kernel size spinbox
        self.kernel_size = (val,val)                        # pass value to Kernel size variable

    def stdDeviation(self, val):                            # update value from Standard Deviation spinbox
        self.std_Deviation = val                            # pass value to Std Deviation variable

    def sigmaValue(self, val):                              # update value from sigma spinbox
        self.sigma = val                                    # pass value to sigma variable

    def hysteresisThreshold_1(self, val):                   # update value from hysteresisThreshold_1 spinbox
        self.h_threshold1 = val                             # pass value to Threshold 1 variable

    def hysteresisThreshold_2(self, val):                   # update value from hysteresisThreshold_2 spinbox
        self.h_threshold2 = val                             # pass value to Threshold 2 variable

        # Canny Edge detection. Called by either 'backgroundReference' or 'detectEdges'
    def cannyEdges(self, blur_name):
        blur = cv2.imread(blur_name)                        # get blurred image
        thr = self.getThresholds(blur_name)                 # get threshold values
        gauss = self.getGaussParameters()                   # get Gauss filter parameters
        # name of canny edge image
        canny_name = self.canny_dir.format(self.img_index, gauss[0], gauss[1], thr[0], thr[1], thr[2])
        edges = cv2.Canny(blur, thr[1], thr[2])             # Canny Edge detection
        cv2.imwrite(canny_name, edges)                      # writes image on the directory
        print("Canny Edge image saved as " + canny_name)    # send message to terminal
        return(canny_name)

    def blurImage(self, img_name):
        img = cv2.imread(img_name)                          # read image
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)        # grayscale image
        gauss = self.getGaussParameters()                   # get Gauss filter parameters
        # name of blurred image
        blur_name = self.blur_dir.format(self.img_index, gauss[0], gauss[1])
        blur = cv2.GaussianBlur(gray, self.kernel_size, gauss[1])   # perform gaussian blur
        cv2.imwrite(blur_name, blur)                        # writes blurred image to directory
        print("Blurred image saved as " + blur_name)        # send message to terminal
        return(blur_name)

        # Determine threshold values. Called by 'cannyEdges'
    def getThresholds(self, blur_name):
        if self.manual_canny:                               # if manual checkbox is checked
            sigma = ""                                      # sigma value N/A
            thr_1 = self.h_threshold1                       # get threshold 1 value
            thr_2 = self.h_threshold2                       # get threshold 2 value
        else:                                               # else: use method by Adrian Rosebrock
            sigma = self.sigma                              # get sigma value
            blur = cv2.imread(blur_name)                    # read blur image
            v = np.median(blur)                             # calculate median
            thr_1 = int(max(0, (1.0 - sigma) * v))          # calculate Threshold 1
            thr_2 = int(min(255, (1.0 + sigma) * v))        # calculate Threshold 2
        return(sigma, thr_1, thr_2)

    def getGaussParameters(self):
        k_size = self.kernel_size                           # get kernel size
        k_size_str = str(k_size).replace(" ", "")           # remove blank spaces in k_size
        return(k_size_str, self.std_Deviation)

        # Display image. Called by 'cannyEdges'
    def displayImage(self, canny_name):
        if self.show_canny_image:                           # if Checkbox is checked
            img = Image.open(canny_name)                    # open processed image
            img.show()                                      # and display it
        else:                                               # else:
            pass                                            # do nothing

    def checkIfImageExists(self, img_name):
        if not os.path.exists(img_name):                    # if the image does not exists
            print("WARNING: No image available.")           # show message in the terminal
        else:                                               # else:
            pass                                            # do nothing

    def matchImage(self):
        img1 = cv2.imread("/home/edgardo/Pictures/CamView/4-processed/canny_1_(7,7):1-90:200.png")
        img2 = cv2.imread("/home/edgardo/Pictures/CamView/4-processed/canny_2_(7,7):1-90:200.png")

        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
        img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:40], img2, flags = 2)
        plt.imshow(img3),plt.show()

    def takePicture(self):                                  # Called by the 'Take Picture' button
        self.savePicture()                                  # take a picture

    def detectEdges(self):                                  # Called by the 'Detect Edges' button
        img_name = self.img_dir.format(self.img_index)      # define image name
        blur_name = self.blurImage(img_name)                # perform Gaussian Blur
        canny_name = self.cannyEdges(blur_name)             # perform Canny Edge detection
        self.displayImage(canny_name)                       # display processed image (or not)

    def backgroundReference(self):                          # Called by the 'Background Reference' button
        bck_name = self.ref_dir                             # define background name
        self.saveBackground()                               # take a picture of the background
        blur_name = self.blurImage(bck_name)                # perform Gaussian Blur
        canny_name = self.cannyEdges(blur_name)             # perform Canny Edge detection
        self.displayImage(canny_name)                       # display processed image (or not)

class Window(QtGui.QMainWindow):

    # Initializations
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 600, 300)
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

        self.spinboxStatus = True                       # Initilize variable for active or grayed-out spinboxes

        # Start capture button
        self.capture = Capture()
        btn = QtGui.QPushButton("Start", self)
        btn.clicked.connect(self.capture.startCapture)
        btn.resize(55,50)                               # Use 'btn.resize(btn.sizeHint())' for minimum size
        btn.move(25,75)

        # Stop capture button
        btn = QtGui.QPushButton("Stop", self)
        btn.clicked.connect(self.capture.endCapture)
        btn.resize(55,50)
        btn.move(85,75)

        # Take Picture button
        btn = QtGui.QPushButton("Take Picture", self)
        btn.clicked.connect(self.capture.takePicture)
        btn.resize(115,50)
        btn.move(25,140)

        # Reset Index button
        btn = QtGui.QPushButton("Reset Index", self)
        btn.clicked.connect(self.capture.resetIndex)
        btn.resize(115,50)
        btn.move(25,205)

        # Canny Edge button
        btn = QtGui.QPushButton("Detect Edges", self)
        btn.clicked.connect(self.capture.detectEdges)
        btn.resize(115,50)
        btn.move(410,75)

        # Reference Button
        btn = QtGui.QPushButton("Background Ref", self)
        btn.clicked.connect(self.capture.backgroundReference)
        btn.resize(115,25)
        btn.move(410,195)

        # Match Button
        btn = QtGui.QPushButton("Match", self)
        btn.clicked.connect(self.capture.matchImage)
        btn.resize(115,25)
        btn.move(410,230)

        # Checkbox to automatically open canny image after processing
        cbx = QtGui.QCheckBox("Open Image", self)
        cbx.resize(135,30)
        cbx.move(410, 130)
        cbx.toggle()
        cbx.stateChanged.connect(self.capture.cannyCheckBox)

        # Checkbox to calculate threshold values manually or automatically
        cbx = QtGui.QCheckBox("Manual Threshold", self)
        cbx.resize(155,30)
        cbx.move(410, 160)
        cbx.stateChanged.connect(self.capture.autoCannyCheckBox)
        cbx.stateChanged.connect(self.spinboxToggle)

        klab = QtGui.QLabel("Kernel Size:", self)
        klab.move(210, 75)

        klab = QtGui.QLabel("Std Deviation:", self)
        klab.move(195, 110)

        tlab = QtGui.QLabel("Sigma:", self)
        tlab.move(248, 145)

        tlab = QtGui.QLabel("Threshold 1:", self)
        tlab.move(205, 180)

        tlab = QtGui.QLabel("Threshold 2:", self)
        tlab.move(205, 215)

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

        # Spinbox for sigma values
        self.spn5 = QtGui.QDoubleSpinBox(self)
        self.spn5.move(315, 145)
        self.spn5.setFixedWidth(70)
        self.spn5.setRange(.00,.99)
        self.spn5.setValue(.33)
        self.spn5.setSingleStep(0.01)
        self.spn5.valueChanged.connect(self.capture.sigmaValue)
        self.spn5.setEnabled(self.spinboxStatus)

        # Spinbox for Hysteresis Threshold 1 values
        self.spn3 = QtGui.QSpinBox(self)
        self.spn3.move(315, 180)
        self.spn3.setFixedWidth(70)
        self.spn3.setRange(0,500)
        self.spn3.setValue(90)
        self.spn3.valueChanged.connect(self.capture.hysteresisThreshold_1)
        self.spn3.setEnabled(not self.spinboxStatus)

        # Spinbox for Hysteresis Threshold 2 values
        self.spn4 = QtGui.QSpinBox(self)
        self.spn4.move(315, 215)
        self.spn4.setFixedWidth(70)
        self.spn4.setRange(0,500)
        self.spn4.setValue(110)
        self.spn4.valueChanged.connect(self.capture.hysteresisThreshold_2)
        self.spn4.setEnabled(not self.spinboxStatus)

        self.show()

    # Methods
    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Extract!', "Exit application?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Program terminated by user")
            sys.exit()
        else:
            pass

    def spinboxToggle(self):
        self.spinboxStatus = not self.spinboxStatus     # Toggle value of spinboxStatus
        self.spn3.setEnabled(not self.spinboxStatus)    # Refresh status for spn3
        self.spn4.setEnabled(not self.spinboxStatus)    # Refresh status for spn4
        self.spn5.setEnabled(self.spinboxStatus)        # Refresh status for spn5

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
