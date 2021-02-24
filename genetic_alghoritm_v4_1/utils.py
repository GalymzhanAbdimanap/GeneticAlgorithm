import numpy as np
import random, time
import cv2 
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks


def fitness(image, delta_x, length, individ):                      
    """Responsible for calculating the "fit" (counts the amount)."""
    
    summa = 0
    sum_vrt = 0
    for i in range(length):                 
        sum_ = np.sum(image[individ[i], i*delta_x:i*delta_x+delta_x])
        if i>0:
            if individ[i]>individ[i-1]:
                sum_vrt = np.sum(image[individ[i-1]:individ[i], i*delta_x])
            else:
                sum_vrt = np.sum(image[individ[i]:individ[i-1], i*delta_x])
        summa=summa + sum_ + sum_vrt       
    return summa


def find_peaks_(image):
    """Calculates ranges of random numbers for our individuals."""

    height, width = image.shape[:2]
    img_matrix = [sum(i)/len(i) for i in image]
    x=[i for i in range(height)]
    y = [255-i for i in img_matrix]
    y = gaussian_filter(y, sigma=20)
    maxs, _ = find_peaks(y)
    maxs = maxs.tolist()

    return maxs

def run(gaObj, peaks, epoch):
    """Runs a genetic algorithm."""

    gen_lines = []
    
    for line in range(len(peaks)-1):
        gaObj.create_population(peaks[line], peaks[line+1])
        epoch_line = []
        for p in range(epoch):  
            st_time = time.time()                  
            gen_line = gaObj.call()
            epoch_line.append(gen_line.A)            # For draw results each epoch, add results of each epoch.
            print(f'Line = {line}, Epoch = {p}, fit = {gen_line.fit}, Time = {time.time()-st_time}') 
        
        gen_lines.append(epoch_line)  
    return np.moveaxis(np.array(gen_lines), 0, 1)    # Swap line and epoch axes.


def drawLines(image, lines, delta_x, epoch='last', color=(0,0,255), thickness = 3, IMG_FOLDER='imgs'):
    """Draws the result of a genetic algorithm."""
    
    image_copy = image.copy()
    for j in lines:
        for i in range(len(j)):
            x1 = i*delta_x
            x2 = i*delta_x+delta_x
            y1 = j[i]
            y2 = j[i]
            start_point = (x1, y1)

            if i>0:
                cv2.line(image_copy, preview_point, start_point, color, thickness)
            end_point = (x2, y2)

            cv2.line(image_copy, start_point, end_point, color, thickness)
            preview_point = end_point

    cv2.imwrite(f"{IMG_FOLDER}/gen_line{epoch}.jpg", image_copy)