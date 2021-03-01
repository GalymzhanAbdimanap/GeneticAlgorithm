import numpy as np
import random, time
import cv2 
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
from numba import njit
import pymp

@njit
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
    """Calculates ranges of random numbers for our individs."""

    height, width = image.shape[:2]
    img_matrix = [sum(i)/len(i) for i in image]
    x=[i for i in range(height)]
    y = [255-i for i in img_matrix]
    y = gaussian_filter(y, sigma=20)
    maxs, _ = find_peaks(y)
    maxs = maxs.tolist()

    return maxs

def run(gaObj, peaks, epoch, parallel=True, number_cpu=4):
    """Can choose how to run."""
   
    gen_lines = pymp.shared.list()
    if parallel:
        with pymp.Parallel(number_cpu) as p:
            range_peaks = p.range(len(peaks)-1)
            gen_lines = run_genetic_algorithm(gaObj, peaks, epoch, range_peaks, gen_lines)
    else:
        range_peaks = range(len(peaks)-1)
        gen_lines = run_genetic_algorithm(gaObj, peaks, epoch, range_peaks, gen_lines)
              
    return np.moveaxis(np.array(gen_lines), 0, 1)    # Swap line and epoch axes.


def draw_lines(image, lines, delta_x, imagename, epoch='last', color=(0,0,255), thickness = 3, IMG_FOLDER='output'):
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
    cv2.imwrite(f"{IMG_FOLDER}/{imagename[:-4]}_gen_line_{epoch}.jpg", image_copy)


def run_genetic_algorithm(gaObj, peaks, epoch, range_peaks, gen_lines):
    """Runs a genetic alghoritm."""

    for line in range_peaks:
        gaObj.create_population(peaks[line], peaks[line+1])
        epoch_line = pymp.shared.list()
        for p in range(epoch):  
            st_time = time.time()                  
            gen_line = gaObj.call()
            epoch_line.append(gen_line.A)            # For draw results each epoch, add results of each epoch.
            print(f'Line = {line}, Epoch = {p}, fit = {gen_line.fit}, Time = {time.time()-st_time}') 
        gen_lines.append(epoch_line)
    
    return gen_lines

def crop_lines(image, lines, delta_x, imagename, IMG_FOLDER='crops'):
    """Crop the lines."""

    for i in range(-1,len(lines)):
        height, width = image.shape[:2]

        if i == (-1):
            first_line = [[i*delta_x, 0] for i, el in enumerate(lines[i])]
        else:
            first_line = [[i*delta_x, el] for i, el in enumerate(lines[i])]

        first_line = first_line[::-1] # Reverse first line.
        
        if i < len(lines)-1:
            second_line = [[i*delta_x, el] for i, el in enumerate(lines[i+1])]
        else:
            second_line = [[i*delta_x, height] for i, el in enumerate(lines[i])]

        points = np.array([first_line + second_line])
        mask = np.zeros((height, width), dtype=np.uint8)
        cv2.fillPoly(mask, points, (255))

        res = cv2.bitwise_and(image,image,mask = mask)

        rect = cv2.boundingRect(points) # Returns (x,y,w,h) of the rect
        im2 = np.full((res.shape[0], res.shape[1], 3), (0, 255, 0), dtype=np.uint8 ) # You can also use other colors or simply load another image of the same size
        maskInv = cv2.bitwise_not(mask)
        colorCrop = cv2.bitwise_or(im2,im2,mask = maskInv)
        finalIm = res + colorCrop
        cropped = finalIm[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]

        cv2.imwrite(f"{IMG_FOLDER}/croped_{imagename[:-4]}_{i}.png", cropped)

