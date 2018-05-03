import cv2
import argparse
import numpy as np

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

def find_loc(img_rgb):
    templatefile = 'roi.jpg'

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(templatefile,0)
    w, h = template.shape[::-1]


    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.97
    loc = np.where( res >= threshold)


    cnt = 0

    for pt in zip(*loc[::-1]):
        return pt[0]

        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
        cv2.imshow('frame', img_rgb)
        cv2.waitKey(25)
        cnt += 1
        break
    # print cnt



def getFirst(videofile):

    cap = cv2.VideoCapture(videofile)
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps)

    frameUp = None
    upperLim = None


    for i in range(50):
        ret, frame = cap.read()

        if frame is None:
            break
            
        ratio = 960.0 / frame.shape[1]
        frame = cv2.resize(frame, (0,0), fx=ratio, fy=ratio) 

        loc = find_loc(frame)

        # print loc
        if not upperLim or (frameUp and loc != None and upperLim > loc):
            frameUp = i
            upperLim = loc

    return frameUp, upperLim



if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Video crop')
    
    parser.add_argument('video1', metavar='video1', type=str, help='name of original video')
    parser.add_argument('video2', metavar='video2', type=str, help='name of defected video')
    args = parser.parse_args()
    video1 = args.video1
    video2 = args.video2


    # video1 = '1-f.avi'
    # video2 = '2-f.avi'

    try:
        first1 = getFirst(video1)
        first2 = getFirst(video2)
    except:
        print 'roi.jpg file does not exist!'
        first1 = (0, 0)
        first2 = (0, 0)
   
    # print first1
    # print first2

    cap1 = cv2.VideoCapture(video1)
    cap2 = cv2.VideoCapture(video2)
    len1 = int(cap1.get(cv2.CAP_PROP_FRAME_COUNT))
    len2 = int(cap2.get(cv2.CAP_PROP_FRAME_COUNT))    
    # print len1
    # print len2


    for i in range(first1[0]):
        _, frame = cap1.read()
        
    for i in range(first2[0]):
        _, frame = cap2.read()


    lenTot = min((len1 - first1[0]), (len2 - first2[0]))

    error = 0.0

    for i in range(lenTot):
        ret, frame1 = cap1.read()
        ret, frame2 = cap2.read()
        error += rmse(frame1, frame2)



    print error
    error /= lenTot
    print error





