import numpy as np, py4DSTEM as py4d
import ncempy.io as nio
from py4DSTEM.datacube import DataCube
import os, pprint
#from emdfile import save as _save
#import emdfile as emd
# import warnings

# -------------------------------------------------------------------------------------------------------    
print('reading ser file')

pth = os.getcwd()
allfiles = {}
i = 1
for root, dirs, files in os.walk(pth):
    for name in files:
        fullname = os.path.join(name)
        allfiles[i] = name
        #print(fullname)
        i+=1
del root, dirs, files #fullname

print('files in current directory:')
pprint.pprint(allfiles)
inname = input(f'enter SER file index(1-{i-1}): ')

serData = nio.read( allfiles[int(inname)] )
serData['pixelSize'] = [ 0.00025 , 0.00025] # random values!!!
serData['pixelUnit'] = ['A^-1', 'A^-1']
serDataShape=serData['data'].shape
scanX = int(input('enter pixels per line (X direction): '))
scanY = int(input('enter pixels per col  (Y direction): '))
nbedX = serDataShape[1]
nbedY = serDataShape[2]
serdat = serData['data']

# shape is {NBED_counts_x, NBED_counts_y, NBED_size_x, NBED_size_x}
maxval = np.max( np.max( np.max( serdat[:,:,:] ) ) ) 
if ( maxval < 65500 ):
    ar = np.zeros(( scanX , scanY , nbedX , nbedY ), dtype=np.float16)
else:
    ar = np.zeros(( scanX , scanY , nbedX , nbedY ), dtype=np.float32)
#ar = np.zeros(( scanX , scanY , nbedX , nbedY ), dtype=np.float32)


print('making numpy array woth NBED patterns\n')
k=0;
for i in range(scanX):
    for j in range(scanY):
        ar[i,j,:,:] = serdat[k,:,:]
        k+=1


print('creating HDF5 file\n')
# easy way to create DataCube
# make sure that ar type of ar variable is <class 'numpy.ndarray'> 
datcub = DataCube(ar, name='gaas_nbed')
datcub.calibration.set_Q_pixel_units(serData['pixelUnit'][0])
datcub.calibration.set_Q_pixel_size(serData['pixelSize'][0])
datcub.calibration.set_R_pixel_size(1)
datcub.calibration.set_R_pixel_units('nm')

# If u want to reduce size of resulting h5 file, use the following command
# optimal size of binned NBED - 128x128
print('Do u want to reduce size of resulting h5 file (y/n)?')
print('Note1: if scanXY grid is more than 100x100 you can bin NBEDs in order to reduce final size of h5 file')
print('Note2: optimal size of binned NBED is 128x128')
ques = input('Do you want to bin NBED patterns (y/n)? ')
if (ques == 'y'):
    binFactor = int(nbedX/128)
    datcub.bin_Q(binFactor)


outname = input('enter h5 output file name (_something_.h5): ')
py4d.save(outname, datcub)

