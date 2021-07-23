import numpy as np
import os
import cv2 as cv



def part_3(k):
    print('**********************************************************************************************************************')
    print('')
    print('****  the big picture on the right in the request and the number on it is the number of the correct votes it got  ****')
    print('')
    print('**********************************************************************************************************************')
    if(k % 2 !=0):
        k=k+1
    distances = np.load("distances_40to360.npy", allow_pickle=True)
    for tst_img in range(1, 41, 1):
        sourcepic = os.path.join("tst", "")
        ori = cv.imread(sourcepic + str(tst_img) + ".jpg")
        ori = cv.cvtColor(ori, cv.COLOR_BGR2GRAY)

        distance = distances[tst_img - 1]
        d = []
        for i in range(len(distance) - 1):
            d.append([float(distance[i][0]), distance[i][1]])
        d.sort()
        n = np.asarray(d)

        tstpicspath = os.path.join("Faces", "")
        allimgs = np.ndarray((112 * 10, 92 * 2), "uint8")
        votes_names = n[:, 1]
        votes_names = votes_names[0:k]
        sortedpath = os.path.join("sortd", str(tst_img), "")
        picssortd = os.listdir(sortedpath)
        
        corcts = 0
        for i,v in enumerate(votes_names):
            if v in picssortd:
                corcts = corcts + 1
        a = []
        a1 = []
        for nam in votes_names[0:k//2]:
            # pic = cv.imread(tstpicspath+str(i)+'.jpg')
            pic = cv.imread(tstpicspath + nam)
            pic = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
            pic = cv.putText(
                pic,
                nam[0:-4],
                (20, 25),
                fontFace=cv.FONT_HERSHEY_DUPLEX,
                fontScale=0.9,
                color=(20, 20, 20),
            )
            a.append(pic)
        for nam in votes_names[k//2:k]:
            # pic1 = cv.imread(tstpicspath+str(i*2)+'.jpg')
            pic1 = cv.imread(tstpicspath + nam)
            pic1 = cv.cvtColor(pic1, cv.COLOR_BGR2GRAY)
            pic1 = cv.putText(
                pic1,
                nam[0:-4],
                (20, 25),
                fontFace=cv.FONT_HERSHEY_DUPLEX,
                fontScale=0.9,
                color=(20, 20, 20),
            )
            a1.append(pic1)
        allimg1 = np.hstack(a)
        allimg2 = np.hstack(a1)
        allimgs = np.vstack([allimg1, allimg2])
        ori = cv.putText(
            ori,
            str(corcts),
            (25, 25),
            fontFace=cv.FONT_HERSHEY_DUPLEX,
            fontScale=0.5,
            color=(20, 250, 20),
        )
        allimgs = np.hstack([allimgs, cv.resize(ori, (92 * 2, 112 * 2))])
        cv.imshow("all", allimgs)
        cv.waitKey(0)    
    print('finished 3/3)')  

