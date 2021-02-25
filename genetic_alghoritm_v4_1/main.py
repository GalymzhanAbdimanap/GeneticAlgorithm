import cv2 
import glob, os
from utils import *
from SimpleSegmentationGA import SimpleSegmentationGA



if __name__ == '__main__':

    # Hyper parameters for genetic alghoritms.
    POP_NUM=80
    DELTAX=50 # Value of h.
    EPOCH=100
    IMAGES_PATH = 'input'
    # IMAGE_PATH = '7.jpg'
    

    images = glob.glob(f'{IMAGES_PATH}/*.jpg')
    for imagename in images:
        fstart_time = time.time()
        # Image operations. 
        image = cv2.imread(imagename)
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
        lines = run(ssga, peaks, EPOCH, parallel=False)
        print('Time run =', time.time()-start_time)

        start_time = time.time()
        # Draw the result of the genetic alghoritm. lines[-1] -> result of last epoch.
        draw_lines(image, lines[-1], DELTAX, os.path.basename(imagename))
        print('Time draw_lines =', time.time()-start_time)

        start_time = time.time()
        # Crop the result of genetic alghoritm.
        crop_lines(image, lines[-1], DELTAX, os.path.basename(imagename))
        print('Time crop_lines =', time.time()-start_time)
        print('Time for one image =', time.time()-fstart_time)
        
