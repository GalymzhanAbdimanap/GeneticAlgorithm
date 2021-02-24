import cv2 
from utils import *
from SimpleSegmentationGA import SimpleSegmentationGA


if __name__ == '__main__':

    # HYPER PARAMETERS FOR GENETIC ALGHORITM.
    POP_NUM=80
    DELTAX=50 # VALUE OF H.
    EPOCH=100
    IMAGE_PATH = '7.jpg'

    image = cv2.imread(IMAGE_PATH)
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    peaks = find_peaks_(gray) #[:2]
    length_ = int(width/DELTAX)
    ssga = SimpleSegmentationGA(POP_NUM, length_, DELTAX, EPOCH, gray)
    start_time = time.time()
    lines = run(ssga, peaks, EPOCH)
    print('Time run=', time.time()-start_time)
    drawLines(image, lines[-1], DELTAX)