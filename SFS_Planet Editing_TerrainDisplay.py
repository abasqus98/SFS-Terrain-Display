import matplotlib.pyplot as plt
import matplotlib.image as img
from matplotlib.gridspec import GridSpec as gridspec
from math import pi,floor,ceil
import numpy as np
import json

#############################################
#############################################

#EDIT HERE TO ADJUST PATH
#path_pack=r'D:\zzz\SFS\Addon 2.03- the SFS Mod Pack\Truly Terrained Solar System (FRM)\\'
#path_pack=r'D:\zzz\SFS\IRIS x TTSS [Python]\\'
#path_pack=r'D:\zzz\SFS\IRIS x TTSS\\'
#path_pack=r'D:\zzz\SFS\Heightmap Test - pngjpgcol\\'

path_pack=r'C:\Users\Hendry\Documents\zzz\zzz SFS\IRIS x TTSS [Python]\\'

#EDIT HERE TO PICK PLANET
planet='Phoebe'

#EDIT HERE TO ADJUST STEP
div=100000 #100000 is both smooth and fast 

#EDIT HERE TO SKIP DIFFICULTY
skip_normal=0
skip_hard=0
skip_realistic=0

#EDIT HERE TO SKIP TIMEWARP HEIGHT
skip_twh=1

##############################################
##############################################

print(f'Visualizing {planet} from {path_pack.split('\\')[-3]}')

path_hmap=path_pack+'Heightmap Data'
path_pldat=path_pack+'Planet Data'
planet=planet+'.txt'
terrain={}
Rdata={}

#Extracting terrain parameters, including each difficulties
with open (path_pldat+'\\'+planet,'r+') as f:
    d=json.load(f)
    ter=d['TERRAIN_DATA']['terrainFormulaDifficulties']
    ter={key.lower(): value for key, value in ter.items()}
    
    if skip_normal and 'normal' in ter: del ter['normal']
    if skip_hard and 'hard' in ter: del ter['hard']
    if skip_realistic and 'realistic' in ter: del ter['realistic']

    
    if ('radiusDifficultyScale' in d['BASE_DATA']) and d['BASE_DATA']['radiusDifficultyScale']!={}:
        d['BASE_DATA']['radiusDifficultyScale']={key.lower(): val for key, val in d['BASE_DATA']['radiusDifficultyScale'].items()}
        Rdata['normal']=d['BASE_DATA']['radius']*d['BASE_DATA']['radiusDifficultyScale']['normal']
        Rdata['hard']=d['BASE_DATA']['radius']*d['BASE_DATA']['radiusDifficultyScale']['hard']
        Rdata['realistic']=d['BASE_DATA']['radius']*d['BASE_DATA']['radiusDifficultyScale']['realistic']
    else:
        Rdata={'normal':1*d['BASE_DATA']['radius'],\
               'hard':2*d['BASE_DATA']['radius'],\
               'realistic':20*d['BASE_DATA']['radius']}
    if not skip_twh:
        Twarp=d['BASE_DATA']['timewarpHeight']


#Breaking down the heightmap formulation
for key in ter:
    #For each difficulty..
    terrain[key]={}
    for i in range(len(ter[key])):
        #Splitting hmap formula
        ter[key][i]=ter[key][i].replace('=',' ').replace('(',' ').\
                     replace(')',' ').replace(',',' ').replace('AddHeightMap',' ')
        ter[key][i]=ter[key][i].split()
        terrain[key]['h_'+str(i+1)]={}
        terrain[key]['h_'+str(i+1)]['output']={}
        terrain[key]['h_'+str(i+1)]['output']=ter[key][i][0]
        if not(ter[key][i][1].endswith('.png')) and not(ter[key][i][1].endswith('.txt')):
            ter[key][i][1]=ter[key][i][1]+'.txt'
        terrain[key]['h_'+str(i+1)]['name']={}
        terrain[key]['h_'+str(i+1)]['name']=ter[key][i][1]
        terrain[key]['h_'+str(i+1)]['width']={}
        terrain[key]['h_'+str(i+1)]['width']=ter[key][i][2]
        terrain[key]['h_'+str(i+1)]['height']={}
        terrain[key]['h_'+str(i+1)]['height']=ter[key][i][3]

        #Multipliers naming
        if len(ter[key][i])==5 or len(ter[key][i])==6:
            if not(ter[key][i][4].endswith('.txt')) and \
               not(ter[key][i][4].casefold()=='null') \
               and not(ter[key][i][4].endswith('.png')):
                ter[key][i][4]=ter[key][i][4]+'.txt'
            terrain[key]['h_'+str(i+1)]['mult1']={}
            terrain[key]['h_'+str(i+1)]['mult1']=ter[key][i][4]
        if len(ter[key][i])==6:
            terrain[key]['h_'+str(i+1)]['mult2']={}
            terrain[key]['h_'+str(i+1)]['mult2']=ter[key][i][5]
        #print(f'h_{i} {ter[key][i][0]}')
        
        #Taking main values
        terrain[key]['h_'+str(i+1)]['values']={}
        if ter[key][i][1].endswith('.txt'):
            with open (path_hmap+'\\'+ter[key][i][1],'r+') as f:
                d=json.load(f)
                terrain[key]['h_'+str(i+1)]['values']=d['points']
                #print(len(d['points']))
        elif ter[key][i][1].endswith('.png'):
            imgdat=img.imread(path_hmap+'\\'+ter[key][i][1])
            imgdim=imgdat.shape
            #print(imgdim)
            terrain[key]['h_'+str(i+1)]['values']=[0 for _ in range(2*imgdim[1])]
            for j in range(imgdim[1]):

                #forward version
                #terrain[key]['h_'+str(i+1)]['values'][2*j]=float(sum(imgdat[:,j,3])/imgdim[0])
                #terrain[key]['h_'+str(i+1)]['values'][2*j+1]=float(sum(imgdat[:,j,3])/imgdim[0])
                
                # reversed version: correct one
                terrain[key]['h_'+str(i+1)]['values'][2*j]=float(sum(imgdat[:,imgdim[1]-1-j,3])/imgdim[0])
                terrain[key]['h_'+str(i+1)]['values'][2*j+1]=float(sum(imgdat[:,imgdim[1]-1-j,3])/imgdim[0])
                
                
                

        #Taking mult1 values
        if len(ter[key][i])==5 or len(ter[key][i])==6:
            if not(ter[key][i][4].casefold()=='null'):
                terrain[key]['h_'+str(i+1)]['mult1values']={}
                if ter[key][i][4].endswith('.txt'):
                    with open (path_hmap+'\\'+ter[key][i][4],'r+') as f:
                        d=json.load(f)
                        terrain[key]['h_'+str(i+1)]['mult1values']=d['points']
                        #print(len(d['points']))
                elif ter[key][i][4].endswith('.png'):
                    imgdat=img.imread(path_hmap+'\\'+ter[key][i][4])
                    imgdim=imgdat.shape
                    #print(imgdim)
                    terrain[key]['h_'+str(i+1)]['mult1values']=[0 for _ in range(2*imgdim[1])]
                    for j in range(imgdim[1]):
                        # NEED TO CHECK, PROBABLY REVERSED
                        terrain[key]['h_'+str(i+1)]['mult1values'][2*j]=float(sum(imgdat[:,j,3])/imgdim[0])
                        terrain[key]['h_'+str(i+1)]['mult1values'][2*j+1]=float(sum(imgdat[:,j,3])/imgdim[0])

        
'''   
print(json.dumps(terrain,indent=4))
np.set_printoptions(threshold=6)
print(terrain)
print(circ)
'''

#Print the content. json.dump can't simplify list
for key0 in terrain:
    print(f'{key0}')
    for key1 in terrain[key0]:
        print(f'\t{key1}')
        for key2 in terrain[key0][key1]:
            if isinstance(terrain[key0][key1][key2],list):
                sz=len(terrain[key0][key1][key2])
                sz=f'1x{sz} list'
            else:
                sz=terrain[key0][key1][key2]
            print(f'\t\t{key2} : {sz}')
                

th=list(np.arange(0,2*pi*(1+1/div),2*pi/div)) #0 to 2pi
th[len(th)-1]=2*pi
#pos=[i*Radius for i in th] #0 to circ
sealvl=[0 for _ in range(len(th))]
height=sealvl

#Generating heightmap
for diff in terrain:
    #For each difficulty...
    print(diff)
    for i in range(len(terrain[diff])):
        print(f'   {i+1} th hgtmp ',end="")
        #terrain[diff]['h_'+str(i+1)]['result']={}
        terrain[diff]['h_'+str(i+1)]['result']=sealvl

        for j in range(len(th)):
            ptid=((Rdata[diff]*th[j])%float(terrain[diff]['h_'+str(i+1)]['width']))/\
                  float(terrain[diff]['h_'+str(i+1)]['width'])
            ptid=ptid*(len(terrain[diff]['h_'+str(i+1)]['values'])-1)

            idl=floor(ptid)%len(terrain[diff]['h_'+str(i+1)]['values']) #+1
            idu=ceil(ptid)%len(terrain[diff]['h_'+str(i+1)]['values']) #+1
            init=terrain[diff]['h_'+str(i+1)]['values'][idl]
            final=terrain[diff]['h_'+str(i+1)]['values'][idu]
            #ptid=ptid+1
            
            if idu==idl: terrain[diff]['h_'+str(i+1)]['result'][j]=final
            else: terrain[diff]['h_'+str(i+1)]['result'][j]=\
                  (ptid-idl)/(idu-idl)*(final-init)+init
            
        if terrain[diff]['h_'+str(i+1)]['output']=='OUTPUT':
            print(f'| output ',end="")
            
            if 'mult1' in terrain[diff]['h_'+str(i+1)] and \
               not(terrain[diff]['h_'+str(i+1)]['mult1']=='null'):
                print(f'| mult1 ',end="")
                #result=4thparam(result, mult1values)
                for k in range(len(terrain[diff]['h_'+str(i+1)]['result'])):
                    idxm=terrain[diff]['h_'+str(i+1)]['result'][k]*(len(\
                        terrain[diff]['h_'+str(i+1)]['mult1values'])-1)
                    idxu=ceil(idxm)
                    idxl=floor(idxu)

                    if idxu>len(terrain[diff]['h_'+str(i+1)]['mult1values']):
                        idxu=len(terrain[diff]['h_'+str(i+1)]['mult1values'])
                    if idxl>len(terrain[diff]['h_'+str(i+1)]['mult1values']):
                        idxl=len(terrain[diff]['h_'+str(i+1)]['mult1values'])
                    if idxl<1: idxl=1
                    if idxu==idxl: idxu+=1

                    if idxu>len(terrain[diff]['h_'+str(i+1)]['mult1values']):
                        fin=terrain[diff]['h_'+str(i+1)]['mult1values'][\
                            len(terrain[diff]['h_'+str(i+1)]['mult1values'])-1]
                    else:
                        fin=terrain[diff]['h_'+str(i+1)]['mult1values'][idxu]
                    if idxl>len(terrain[diff]['h_'+str(i+1)]['mult1values']):
                        init=terrain[diff]['h_'+str(i+1)]['mult1values'][\
                            len(terrain[diff]['h_'+str(i+1)]['mult1values'])-1]
                    else:
                        init=terrain[diff]['h_'+str(i+1)]['mult1values'][idxl]

                    terrain[diff]['h_'+str(i+1)]['result'][k]=\
                        (idxm-idxl)/(idxu-idxl)*(fin-init)+init
                    
                    
            if 'mult2' in terrain[diff]['h_'+str(i+1)]:
                print(f'| mult2 ',end="")
                for j in range(len(terrain[diff])):
                    if terrain[diff]['h_'+str(i+1)]['mult2']==\
                       terrain[diff]['h_'+str(j+1)]['output']:
                        break
                terrain[diff]['h_'+str(i+1)]['result']=list(map(lambda x,y: x*y,\
                            terrain[diff]['h_'+str(i+1)]['result'],\
                            terrain[diff]['h_'+str(j+1)]['result']))
        print(f'| heightmult ',end="")

        
        terrain[diff]['h_'+str(i+1)]['result']=\
                    list(map(lambda x: x*float(terrain[diff]['h_'+str(i+1)]['height']),\
                    terrain[diff]['h_'+str(i+1)]['result']))
        print(f'| done ',end="")
                    
          

        #element2element multiplication must use numpy. convert back using .tolist()

        print('')

    terrain[diff]['heightresult']=sealvl
    #adding every heightmap
    for i in range(len(terrain[diff])-1):
        if terrain[diff]['h_'+str(i+1)]['output']=='OUTPUT':
            terrain[diff]['heightresult']=\
                    list(map(lambda x,y:x+y, \
                    terrain[diff]['heightresult'], \
                    terrain[diff]['h_'+str(i+1)]['result']))

'''''
tryy='normal'

height=terrain[tryy]['heightresult']

thdeg=list(map(lambda x: x/pi*180,th))


Rp=list(map(lambda x: x+Rdata[tryy],height))

samp=4
samp=samp/2
thdegseam=thdeg[(len(thdeg)-ceil(samp/360*div)):]
thdegseam=list(map(lambda x: x-360,thdegseam))
thdegseam=thdegseam+thdeg[:(floor(samp/360*div))]
heightseam=height[(len(height)-ceil(samp/360*div)):]+height[:(floor(samp/360*div))]
#fig,(axp,axc)=plt.subplots(1,2)#subplot_kw={'projection':'polar'})

fig=plt.figure()
axp=fig.add_subplot(3,1,1, projection='polar')
axp.plot(th,Rp)

axc=fig.add_subplot(3,1,2)
axc.plot(thdeg,height)

axs=fig.add_subplot(3,1,3)
axs.plot(thdegseam,heightseam)
#plt.plot(thdeg,height)
fig.suptitle(f'{planet[:-4]} - normal')
plt.show()
'''''

if len(terrain) != 0:

    fig=plt.figure()
    gs=gridspec(3,len(terrain), figure=fig, hspace=.5, wspace=.3)
    difflist=list(terrain.keys())
    thdeg=list(map(lambda x: x/pi*180,th))
    title=''

    for i in range(len(difflist)):
        
        axp=fig.add_subplot(gs[0,i],projection='polar')
        Rp=list(map(lambda x: x+Rdata[difflist[i]],terrain[difflist[i]]['heightresult']))
        axp.plot(th,Rp)

        axc1=fig.add_subplot(gs[1,i])
        axc1.plot(thdeg,terrain[difflist[i]]['heightresult'])
        if not skip_twh:
            twh=[Twarp+Rdata[difflist[i]] for _ in range(len(thdeg))]
            axc1.plot(thdeg,twh)
                      
   
        axc2=fig.add_subplot(gs[2,i])
        samp=1
        samp=samp/2
        thdegseam=thdeg[(len(thdeg)-ceil(samp/360*div)):]
        thdegseam=list(map(lambda x: x-360,thdegseam))
        thdegseam=thdegseam+thdeg[:(floor(samp/360*div))]
        heightseam=terrain[difflist[i]]['heightresult']\
                    [(len(terrain[difflist[i]]['heightresult'])-ceil(samp/360*div)):]+\
                terrain[difflist[i]]['heightresult'][:(floor(samp/360*div))]
        axc2.plot(thdegseam,heightseam)
        title=title+str(difflist[i])+', '

    title=title[:-2].title()
    plt.suptitle(f'{planet[:-4]}: '+title)
    plt.show()


##HAUMEA ONLY
'''''
ll=len(terrain['normal']['heightresult'])

plt.subplot(7,1,1)
plt.plot(thdeg,terrain['normal']['h_1']['result'])
plt.subplot(7,1,2)
plt.plot(thdeg,terrain['normal']['h_2']['result'])
plt.subplot(7,1,3)
plt.plot(thdeg,terrain['normal']['h_3']['result'])
plt.subplot(7,1,4)
plt.plot(thdeg,terrain['normal']['h_4']['result'])
plt.subplot(7,1,5)
plt.plot(thdeg,terrain['normal']['h_5']['result'])
plt.subplot(7,1,6)
plt.plot(thdeg,terrain['normal']['h_6']['result'])
plt.subplot(7,1,7)
plt.plot(thdegseam[136:141],heightseam[136:141])
plt.show()



a1=terrain['normal']['h_1']['result'][:2]
a2=terrain['normal']['h_2']['result'][:2]
a3=terrain['normal']['h_3']['result'][:2]
a4=terrain['normal']['h_4']['result'][:2]
a5=terrain['normal']['h_5']['result'][:2]
a6=terrain['normal']['h_6']['result'][:2]


a1=a1+terrain['normal']['h_1']['result'][-3:]
a2=a2+terrain['normal']['h_2']['result'][-3:]
a3=a3+terrain['normal']['h_3']['result'][-3:]
a4=a4+terrain['normal']['h_4']['result'][-3:]
a5=a5+terrain['normal']['h_5']['result'][-3:]
a6=a6+terrain['normal']['h_6']['result'][-3:]

plt.subplot(7,1,1)
plt.plot(thdegseam[136:141],a1)
plt.subplot(7,1,2)
plt.plot(thdegseam[136:141],a2)
plt.subplot(7,1,3)
plt.plot(thdegseam[136:141],a3)
plt.subplot(7,1,4)
plt.plot(thdegseam[136:141],a4)
plt.subplot(7,1,5)
plt.plot(thdegseam[136:141],a5)
plt.subplot(7,1,6)
plt.plot(thdegseam[136:141],a6)
plt.subplot(7,1,7)
plt.plot(thdegseam[136:141],heightseam[136:141])
plt.show()

###HAUMEA ONLY
'''''
'''''
05 01 2026
seam overlap
Planet Selection
Plotting positioning and lengend
Application


'''''
