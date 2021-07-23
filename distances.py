import numpy as np
import os
import cv2 as cv

def cal_histogram(img):
    # his=cv.calcHist([img],[0],None,[256],[0,256]) 
    #Mask None Maybe changd if w switch to n*m cells i guss !!
    # his=np.histogram(img,256,(0,255)) 
    his=np.histogram(img,16,(0,15)) 
    return his[0] 
def x2_distance(hist1,hist2):
    dist = 0.0
    for i in range(len(hist1)):
        t=((hist1[i]-hist2[i])*(hist1[i]-hist2[i]))
        b=(hist1[i]+hist2[i])
        if b==0:
            dist=dist + (t/(b+1))
        else:
            dist=dist + (t/b)     
    return dist
def distances_to_hists(nw_img_hist, the_rest_hist):
    distances=[]
    for i,his in enumerate(the_rest_hist):
        dis = x2_distance(nw_img_hist,his[0])
        distances.append([dis,his[1]])   
    return distances

histos= np.load('histos_nw_360.npy',allow_pickle=True) 
d=[]
path=os.path.join( 'tst','')
alltstpics = os.listdir(path)
for i in alltstpics:
    img=cv.imread(path+i)
    img=cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    his = cal_histogram(img)
    d.append(distances_to_hists(his,histos))
    
    
ddd= np.array(d)
np.save('distances_nw_40to360',d)        

print('don')       
