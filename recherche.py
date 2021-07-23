from operator import concat
import numpy as np
import os
import cv2 as cv
from numpy.core.numeric import True_
# import scipy
from numpy.lib.function_base import average
from numpy.lib.histograms import histogram


# return the X² distanc between the histograms  
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
# same as the offline phase  
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
# same as the offline phase excpt its run over just one image and not the whole database 
# return a histogram discriptor
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
                    result = compare(window[1,1],suroundings,0.18)
                    blank_1[h,w]=int(result[1],2)
                    blank_2[h,w]=int(result[2],2)
                    # blank_1[h,w]=int(result[1],2)*256/16
                    # blank_2[h,w]=int(result[2],2) *256/16             
        his1=cal_histogram(blank_1)
        his2=cal_histogram(blank_2)
        his=[]
        ############
        for i in range(len(his1)):
            his.append(his1[i])
        for i in range(len(his2)):
            his.append(his2[i])
        # histograms.append([his1,his2])
        return his
# same as the offline phase  
def cal_histogram(img):
    # his=cv.calcHist([img],[0],None,[256],[0,256]) 
    #Mask None Maybe changd if w switch to n*m cells i guss !!
    # his=np.histogram(img,256,(0,255)) 
    his=np.histogram(img,16,(0,15)) 
    return his[0] 
# same as the offline phase  
def compare(center,suroundings,k=0.18):
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
             
# return the distances to every histogram in th database
def distances_to_hists(nw_img_hist, the_rest_hist):
    distances=[]
    for i,his in enumerate(the_rest_hist):
        dis = x2_distance(nw_img_hist,his[0])
        distances.append([dis,his[1]])   
    return distances

def look_it_up(data_path,pic_path,pic_name):
    hist_all_pic= np.load(data_path,allow_pickle=True)
    nw_pic=os.path.join( pic_path,'')
    nw_pic=nw_pic+pic_name
    hi = traitmnt_ltp(img_path_name=nw_pic)
    distancs = distances_to_hists(hi,hist_all_pic)
    distancs_sortd = distancs.copy()
    distancs_sortd.sort()
    return distancs_sortd
 
histos= np.load('histos_nw.npy',allow_pickle=True) 
d=[]
path=os.path.join( 'tst','')
allpics = os.listdir(path)
for i in allpics:
    img=cv.imread(path+i)
    img=cv.cvtColor(img,cv.COLOR_RGB2GRAY)
    his = cal_histogram(img)
    distance=[]
    for j in histos:
        distance.append(distances_to_hists(his,histos))
    d.append(distance)    
ddd= np.array(d)
np.save('distances_nw',ddd)        

print('don')       

# aa= np.array(distances_to_hists)
# path_data=os.path.join( '','')
# np.save(path_data+'histos_nw',aa)        

# tstpath=os.path.join( 'tst','')
# alltstpics = os.listdir(tstpath)
# path=os.path.join( 'Faces','')
# allpics = os.listdir(path)
# data_path='histos_nw.npy'
# tott=0
# totf=0
# j=0
# i=0
# f=0
# t=0
# pathsortd = r'C:\Users\DELL\Desktop\bhloul\sortd'
# for o in range(1,41):
#     i=i+1
#     d=look_it_up(data_path=data_path,pic_path=tstpath,pic_name=str(o)+'.jpg')
#     pathss = os.path.join(pathsortd,str(o),'')
#     # print(pathss)#+str(i)+'.jpg')
#     for pic in os.listdir(pathss):
#         j=j+1
#         if(pic == d[0][1]):
#             t=t+1
#         else:    
#             f=f+1
#             # print('true ',i,'/40')
#     # print('corrct ',t,' and fals ',f)   
#     tott=tott+t      
#     totf=totf+t      
#     t=f=0
# print('ror rue ',tott,' tot false ' , totf , 'i is ',i, 'j is ',j)       
        
