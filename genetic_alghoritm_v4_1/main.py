import cv2 
from utils import *
from SimpleSegmentationGA import SimpleSegmentationGA


if __name__ == '__main__':

    # Hyper parameters for genetic alghoritms.
    POP_NUM=80
    DELTAX=50 # Value of h.
    EPOCH=100
    IMAGE_PATH = '7.jpg'

    # Image operations. 
    image = cv2.imread(IMAGE_PATH)
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate individ's lenght.
    length_individ = int(width/DELTAX)

    # Calculate the range of random numbers for an individ.
    peaks = find_peaks_(gray) 
    
    # Create object of class.
    ssga = SimpleSegmentationGA(POP_NUM, length_individ, DELTAX, gray)

    start_time = time.time()
    # Run genetic algorithm.
    lines = run(ssga, peaks, EPOCH)
    print('Time =', time.time()-start_time)

    # Draw the result of the genetic alghoritm.  lines[-1] -> result of last epoch.
    drawLines(image, lines[-1], DELTAX)
