import numpy as np
import cv2
from matplotlib import pyplot as plt
img1 = cv2.imread('bluebetter.png',0)          # queryImage
#img2 = cv2.imread('box_in_scene.png',0) # trainImage
# Initiate SIFT detector
sift = cv2.SIFT()
surf = cv2.SURF()

#sift = cv2.
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)

cap = cv2.VideoCapture('bluebox.mp4')
ret,frame = cap.read()
while True:
    if ret is None:
        cap = cv2.VideoCapture('bluebox.mp4')
        #ret, frame = cap.read()
    ret,frame = cap.read()
    kp2, des2 = sift.detectAndCompute(frame,None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    matches = flann.knnMatch(des1,des2,k=2)
    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in xrange(len(matches))]
    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)
    img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
    plt.imshow(img3,),plt.show()
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()