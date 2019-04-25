import numpy as np
import sys

### Insert the name of the mhd file
file32 = sys.argv[1]

Array = np.fromfile(file32.replace('mhd', 'raw'), dtype=np.float32)
### Replace every non null pixel with value 1
Array[Array!=0]=1

Array.astype(np.uint16).tofile(file32[:len(file32)-4]+'.raw')

file16 = open(file32[:len(file32)-4]+'_int.mhd', 'w+')
with open(file32) as mhdFile:
   for line in mhdFile:
       if line.startswith('ElementType'):
          line = 'ElementType = MET_SHORT' 
          #print(line, file=file32)
          print(line, file=file16)
       elif line.startswith('ElementDataFile'):
          line = 'ElementDataFile = ' + line.split()[2][:len(line.split()[2])-4] +'.raw' 
          print(line, file=file16)
          #print(line, file=file32)
       else:
         print(line, end="", file=file16)
         #print(line, end="", file=file32)

file16.close()
