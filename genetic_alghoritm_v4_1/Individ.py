import numpy as np
import random

class Individ:
    """Generate a new individ."""
    
    def __init__(self, y1, y2, length):   
        self.length = length   
        self.A=np.random.randint(y1, y2, self.length)    # Declare the attribute "A" of our individ (this will be the line 010..101).
        self.fit=0                          # Declare the attribute "fit" of the individ (this will be the sum of the elements of our line 010..101) (for now, we will assign it the value 0)
    
