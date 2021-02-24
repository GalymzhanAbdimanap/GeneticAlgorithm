import numpy as np
import random

class Individ:
    """
    """
    
    def __init__(self, y1, y2, length):   
        self.length = length   
        self.A=np.random.randint(y1, y2, self.length)    #Объявляем атрибут "А" нашего индивида (это будет сама строка 010..101)
        self.fit=0                          #Объявляем атрибут "живучести" индивида (это будет сумма элементов нашей строки 010..101) (пока присвоим ей значение 0)
    