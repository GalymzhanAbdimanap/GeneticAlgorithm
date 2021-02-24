import numpy as np
import random, time
import cv2
from GeneticAlghoritm import GeneticAlghoritm
from Individ import Individ
from utils import * 




class SimpleSegmentationGA(GeneticAlghoritm):
    """Genetic Algorithm Implementation."""

    def __init__(self, pop_num, lenght, delta_x, gray):
        self.pop_num = pop_num
        self.lenght = lenght    # Length of individ.
        self.delta_x =  delta_x # Value of h.
        self.gray = 256 - gray
        


    def create_population(self, y1, y2):
        """Creates a population, Dad, Mom and 4 sons"""

        self.y1 = y1
        self.y2 = y2
        self.population = []                                               # Declare an array "population" in which we will store a population of 5 individuals.
        for i in range(self.pop_num):           
            c=Individ(self.y1, self.y2, self.lenght)                       # Create a new individual.
            self.population.append(c)                                      # Add the i-th unique individual to the array (fill in our population)
                                  
        
        self.mother = Individ(self.y1, self.y2, self.lenght)               # Initialize the variables with which we will work: mom, dad, 4 sons ..
        self.father = Individ(self.y1, self.y2, self.lenght)                     
        self.son1 = Individ(self.y1, self.y2, self.lenght)                       
        self.son2 = Individ(self.y1, self.y2, self.lenght)
        self.son3 = Individ(self.y1, self.y2, self.lenght)
        self.son4 = Individ(self.y1, self.y2, self.lenght)
        self.par_and_sons = []                                             #.. and an array of individs "Parents and Children" in which we will store
        
        for j in range(self.pop_num*3):                                    # Initialize our array of "Parents and Sons" with random individs.
            self.par_and_sons.append(Individ(self.y1, self.y2, self.lenght))       
        

    def cross(self):
        """Crosses the best individs with each other."""

        for i in range(self.pop_num):                                      # Put in the first pop_num elements of the "Parents and Sons" array our entire input population.
            self.par_and_sons[i].A=self.population[i].A.copy()

        random.shuffle(self.population)                                    # Shuffle population.

        tt=0                                                               # The counter that is needed to implement a non-trivial crossing.
        for s in range(0,self.pop_num,2):                                  # From 0 to pop_num with step 2. That is. here we take pop_num / 2 pairs of parents.
            self.mother.A=self.population[tt+int(self.pop_num/2)].A        # Let the last pop_num / 2 individuals of our population be our mothers.
            self.father.A=self.population[tt].A                            # And let first pop_num / 2 individuals of our population be dads.
        
            tt=tt+1    
            ran=random.random()

            for n in range(self.lenght):                                   # Crossover.
                if random.random()>0.5:
                    self.son1.A[n] = self.father.A[n]
                    self.son2.A[self.lenght-1-n] = self.father.A[n]
                    self.son3.A[n] = self.mother.A[n]
                    self.son4.A[self.lenght-1-n] = self.mother.A[n]
                else:
                    self.son1.A[n] = self.mother.A[n]
                    self.son2.A[self.lenght-1-n] = self.mother.A[n]
                    self.son3.A[n] = self.father.A[n]
                    self.son4.A[self.lenght-1-n] = self.father.A[n]

            self.par_and_sons[self.pop_num+2*s].A = self.son1.A.copy()
            self.par_and_sons[self.pop_num+2*s+1].A = self.son2.A.copy()
            self.par_and_sons[self.pop_num+2*s+2].A = self.son3.A.copy()
            self.par_and_sons[self.pop_num+2*s+3].A = self.son4.A.copy()
   

    def mutation(self):
        """Mutates individuals with a 20% probability."""

        for r in range(self.pop_num*3, 5):                                 # Mutation.
            for w in range(0,self.lenght):              
                if random.random()<0.2:                  
                    self.par_and_sons[r].A[w] = self.par_and_sons[r].A[w] + np.random.randint(-20, 20)  # Offset + -20 pixels.
 


    def selection(self):
        """Sorts by fit and selects the best pop_num individs."""

        for i in range(self.pop_num*3):                                    # It is important. Next, we will rank the array of parents and children in ascending order of survivability (sum (fit)).
            self.par_and_sons[i].fit = fitness(self.gray, self.delta_x, self.lenght, self.par_and_sons[i].A)

        #  Sort.
        self.par_and_sons = sorted(self.par_and_sons, key=lambda individ: individ.fit)   
        self.population=self.par_and_sons[:self.pop_num].copy()


    def call(self):
        """Calls other functions and returns the selected population."""

        self.cross()
        self.mutation()
        self.selection()
        
        return  self.population[0]


SimpleSegmentationGA.fitness_function = fitness
