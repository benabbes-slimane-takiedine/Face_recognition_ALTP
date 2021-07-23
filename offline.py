import numpy as np
import os
import cv2 as cv

# return the 8 adjacent pixels in the right order (clockwise)
def get_surounding_bits(img):
    items=[]
    items.append(img[0][0])
    items.append(img[0][1])
    items.append(img[0][2])
    items.append(img[1][2])
    items.append(img[2][2])
    items.append(img[2][1])
    items.append(img[2][0])
    items.append(img[1][0])
    return items
# return a histogram of img using np.histogram()    
def cal_histogram(img):
    # his=cv.calcHist([img],[0],None,[256],[0,256]) 
    #Mask None Maybe changd if w switch to n*m cells i guss !!
    # his=np.histogram(img,256,(0,255)) 
    his=np.histogram(img,16,(0,15)) 
    return his[0] 
# return an array with the origenal LTP result and the two rsults with the upper pass (+1) and lower pass(-1) 
def cs_altp(center,suroundings,k=0.1):
    t=center*k
    result=[]
    up_down=[]
    for i in range(4):
        beg=int(suroundings[i])
        oposit=int(suroundings[i+4])
        dif=beg-oposit
        rang=[-t,t]
        if (dif <rang[0]):
            result.append(-1)
        elif(dif >= rang[0] and dif <= rang[1]):
            result.append(0)
        elif(dif >rang[1]):
            result.append(1)
            
    ori=''
    for i in result:
        ori= ori + str(i)
    up=''
    for i in result:
        if(i ==-1):
            up=up+str(0)
        else:    
            up= up + str(i)           
    down=''
    for i in result:
        if(i ==-1): 
               
            down= down + str(1)  
        else:
            down= down + str(0)   
                         
    up_down.append(ori)
    up_down.append(up)      
    up_down.append(down)              
    return up_down 
             
def part_1():
        
    path=os.path.join('Faces','')
    allpics = os.listdir(path)
    histograms=[]

    # # creating the two images with th uppr and lowr pass
    # # from the ltp procedure to calculate the 2 histograms needed as a discriptor
    for o in allpics:
            cur_path=os.path.join(path,o)
            img=cv.imread(cur_path)
            img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
            blank_1 = np.zeros(img.shape, dtype='uint8')
            blank_2 = np.zeros(img.shape, dtype='uint8')
            height=img.shape[0]
            width=img.shape[1]
            for h in range(1,height-1):
                for w in range(1,width-1):
                    window=img[h-1:h+2,w-1:w+2]
                    suroundings=get_surounding_bits(window)
                    result = cs_altp(window[1,1],suroundings,0.1)
                    blank_1[h,w]=int(result[1],2)
                    blank_2[h,w]=int(result[2],2)
                    # blank_1[h,w]=int(result[1],2)*256/16
                    # blank_2[h,w]=int(result[2],2) *256/16
            
            his1=cal_histogram(blank_1)
            his2=cal_histogram(blank_2)
            his=[]
            for i in range(len(his1)):
                his.append(his1[i])
            for i in range(len(his2)):
                his.append(his2[i])
            histograms.append([his,o])

    path1=os.path.join('tst','')
    tstpics = os.listdir(path1)
    histogramstst=[]

    for o in tstpics:
            cur_path=os.path.join(path1,o)
            img=cv.imread(cur_path)
            img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
            blank_1 = np.zeros(img.shape, dtype='uint8')
            blank_2 = np.zeros(img.shape, dtype='uint8')
            height=img.shape[0]
            width=img.shape[1]
            for h in range(1,height-1):
                for w in range(1,width-1):
                    window=img[h-1:h+2,w-1:w+2]
                    suroundings=get_surounding_bits(window)
                    result = cs_altp(window[1,1],suroundings,0.1)
                    blank_1[h,w]=int(result[1],2)
                    blank_2[h,w]=int(result[2],2)
                    # blank_1[h,w]=int(result[1],2)*256/16
                    # blank_2[h,w]=int(result[2],2) *256/16
            
            his1=cal_histogram(blank_1)
            his2=cal_histogram(blank_2)
            his=[]
            for i in range(len(his1)):
                his.append(his1[i])
            for i in range(len(his2)):
                his.append(his2[i])
            histogramstst.append([his,o])

    # saving the result histograms in an array   
        
    img_360= np.array(histograms)
    path_data=os.path.join( '','')
    np.save(path_data+'histos_of_360',img_360)      

    img_40= np.array(histogramstst)
    path_data=os.path.join( '','')
    np.save(path_data+'histos_of_40',img_40)  
    print('finished 1/3')    
