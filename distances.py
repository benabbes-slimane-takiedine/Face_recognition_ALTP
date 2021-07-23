
import numpy as np
import os
import cv2 as cv

def compare(center,suroundings,k=0.1):
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
def traitmnt_ltp(img_path_name):
        img=cv.imread(img_path_name)
        img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        blank_1 = np.zeros(img.shape, dtype='uint8')
        blank_2 = np.zeros(img.shape, dtype='uint8')
        height=img.shape[0]
        width=img.shape[1]
        for h in range(1,height-1):
                for w in range(1,width-1):
                    window=img[h-1:h+2,w-1:w+2]
                    suroundings=get_surounding_bits(window)
                    result = compare(window[1,1],suroundings,0.1)
                    blank_1[h,w]=int(result[1],2)
                    blank_2[h,w]=int(result[2],2)           
        his1=cal_histogram(blank_1)
        his2=cal_histogram(blank_2)
        his=[]
        for i in range(len(his1)):
            his.append(his1[i])
        for i in range(len(his2)):
            his.append(his2[i])
        return his
def cal_histogram(img):
    his=np.histogram(img,16,(0,15)) 
    return his[0] 
def x2_distance(hist1,hist2):
    dist = 0.0  
    for i in range(32):
        t=float((hist1[i]-hist2[i])*(hist1[i]-hist2[i]))
        b=float(hist1[i]+hist2[i])
        if b==0:
            dist=dist + (t/(b+1))
        else:
            dist=dist + (t/b)     
    return dist
def distances_to_hists(nw_img_hist, the_rest_hist):
    distances=[]
    for _,his in enumerate(the_rest_hist):
        dis = x2_distance(nw_img_hist,his[0])
        distances.append([dis,his[1]])   
    return distances

def part_2():
        
    histos_faces= np.load('histos_of_360.npy',allow_pickle=True) 
    d=[]
    path=os.path.join( 'tst','')
    for i in range(1,41):
        img=cv.imread(path+str(i)+'.jpg')
        img=cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        hist=[traitmnt_ltp(path+str(i)+'.jpg'),str(i)+'.jpg']
        d.append(distances_to_hists(hist[0],histos_faces))
        
    
    distances= np.array(d)
    np.save('distances_40to360',distances)    
    print('finished 2/3')

