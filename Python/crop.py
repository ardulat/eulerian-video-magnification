import cv2
import argparse
 
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False
 
def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False
 
		# draw a rectangle around the region of interest
		cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
		cv2.imshow("image", image)

 

# load the image, clone it, and setup the mouse callback function

parser = argparse.ArgumentParser(description='Video crop')
parser.add_argument('videofile', metavar='videofile', type=str, help='name of videofile')
args = parser.parse_args()
videofile = args.videofile



# videofile = '1.mp4'
cap = cv2.VideoCapture(videofile)
ret, image = cap.read()
ratio = 960.0 / image.shape[1]
image = cv2.resize(image, (0,0), fx=ratio, fy=ratio) 



clone = image
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)
 
# keep looping until the 'q' key is pressed
while True:
	# display the image and wait for a keypress
	cv2.imshow("image", image)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'r' key is pressed, reset the cropping region
	# if key == ord("r"):
	# 	image = clone.copy()
 
	# if the 'c' key is pressed, break from the loop
	if key == ord("c"):
		break
 
# if there are two reference points, then crop the region of interest
# from teh image and display it

if len(refPt) == 2:
	roi = clone[refPt[0][1]+2:refPt[1][1]-1, refPt[0][0]+2:refPt[1][0]-1]
	cv2.imshow("ROI", roi)
	cv2.imwrite("roi.jpg", roi)
	cv2.waitKey(0)
 
# close all open windows
cv2.destroyAllWindows()		
