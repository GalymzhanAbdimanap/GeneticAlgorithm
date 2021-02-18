# importing required libraries of opencv 
import cv2 
  
# importing library for plotting 
from matplotlib import pyplot as plt 

from scipy.ndimage import gaussian_filter

from scipy.signal import find_peaks
  
# reads an input image 
image = cv2.imread("7.jpg")

# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_matrix = []
x = []
for i in image:
    for j in i:
        color = sum(j)/len(j)
        x.append(color)
    img_matrix.append(sum(x)/len(x))
    x=[]



#----------------------------------------------------------------------

x=[]
# x axis values 
for i in range(3508):
    x.append(i)
 
# corresponding y axis values 
y = [255-i for i in img_matrix]


y = gaussian_filter(y, sigma=20)

# plotting the points  
# plt.plot(x, y) 
  
# # naming the x axis 
# plt.xlabel('height') 
# # naming the y axis 
# plt.ylabel('color') 
  
# # giving a title to my graph 
# plt.title('') 
  
# # function to show the plot 
# plt.show()

#-------------------------------------------------------------------------------------------
mins, _ = find_peaks(y*-1)
maxs, _ = find_peaks(y)
print(maxs)
arr = mins
# arr = [i for i, el in enumerate(y) if el < 1.5]
print(len(arr))

count = 0
color = (0, 255, 0) 
thickness = 3
height, width, channels = image.shape
# For draw minimums.
for i in arr:
    start_point = (0, i)
    end_point = (width,i)
    cv2.line(image, start_point, end_point, color, thickness)
    
color=(255,0,0)

# For draw peaks.
for i in maxs:
    start_point = (0, i)
    end_point = (width,i)
    # print(i)
    cv2.line(image, start_point, end_point, color, thickness)

cv2.imwrite("1.jpg", image)


#--------------------------------------------------------------------------------\