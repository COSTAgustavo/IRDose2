import sys

arg1 = sys.argv[1]

with open('test.mhd') as file:           #Idem...
   for  line in file:
     if line.startswith('DimSize'):
        dim_x = line.split()[2]
        dim_y = line.split()[3]
        dim_z = line.split()[4]

     if line.startswith('ElementSpacing'):
        pixelSize_x = line.split()[2]
        pixelSize_y = line.split()[2]
        pixelSize_z = line.split()[2]

print('Dimensions', dim_x, dim_y, dim_z)
print('Element Spacing', pixelSize_x, pixelSize_y, pixelSize_z)

shift_x = (float(dim_x)*float(pixelSize_x))/2
shift_y = (float(dim_y)*float(pixelSize_y))/2
shift_z = (float(dim_z)*float(pixelSize_z))/2

print('Shifts:', shift_x, shift_y, shift_z)
print(arg1)
