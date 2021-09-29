from abc import abstractmethod, abstractproperty
import numpy as np
import random, time
import cv2 
import pymp 
from matplotlib import pyplot as plt 
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks





class GeneticAlghoritm():

    @abstractmethod
    def createPopulation(self):
        pass

    @abstractmethod
    def selection(self):
        pass

    @abstractmethod
    def mutation(self):
        pass

    @abstractmethod
    def cross(self):
        pass


    @abstractmethod
    def calc(self):
        pass




class SimpleSegmentationGA(GeneticAlghoritm):
    """"""

    def __init__(self, pop_num, length, deltaX, epoch, gray):
        self.pop_num = pop_num
        self.length = length
        self.deltaX =  deltaX # value of h
        self.epoch = epoch
        self.gray = 256 - gray
        


    def createPopulation(self, y1, y2):
        """"""

        self.y1 = y1
        self.y2 = y2
        self.population = []                    #Объявляем массив "В", в котором будем хранить популяцию из 10 индивидов.
        for i in range(self.pop_num):            #Цикл
            c=Individ(self.y1, self.y2, self.length)                #В переменную "с" запихнулся (срандомился) новёхонький уникальненький индивид. (на каждой итерации цикла новый)
            self.population.append(c)           #А тут мы добавляем i-го уникального индивида к массиву (заполняем нашу популяцию)                      #Создаём экземпляр класса. Т.е. создаём нашу популяцию из 10 рандомных индивидов
        
        self.Mother = Individ(self.y1, self.y2, self.length)                     #Инициализируем переменные, с которыми будем работать: маму, папу, 4 сыночков..
        self.Father = Individ(self.y1, self.y2, self.length)                     
        self.Son1 = Individ(self.y1, self.y2, self.length)                       
        self.Son2 = Individ(self.y1, self.y2, self.length)
        self.Son3 = Individ(self.y1, self.y2, self.length)
        self.Son4 = Individ(self.y1, self.y2, self.length)
        self.ParAndSons = []                        #..и массив индивидов "Родители+Дети" в котором будем хранить
        
        for j in range(self.pop_num*3):                    #Тут мы "придаём форму" нашему массиву "Родителей и детей". Инициализируем его рандомными индивидами.
            self.ParAndSons.append(Individ(self.y1, self.y2, self.length))       #Чтобы в дальнейшем иметь возможность напрямую работать с этим массивом с помощью наших атрибутов (А, fit)
                                            #Рандомные значения, которыми мы забили этот массив, нам не помешают. Т.к. мы поэлементно все элементы этого массива забьём актуальными данными вручную по ходу программы.
        

    def cross(self):
        """"""

        for i in range(self.pop_num):                #Заносим в первые 10 элементов массива "Отцы и дети" всю нашу входную популяцию.
            self.ParAndSons[i].A=self.population[i].A.copy()

        random.shuffle(self.population) # 

        tt=0                                       #Счётчик, который нужён для реализации небанального скрещивания.
        for s in range(0,self.pop_num,2):                    #Цикл. От 0 до 10 с шагом 2. Т.е. тут мы берём 5 пар родителей.
            self.Mother.A=self.population[tt+int(self.pop_num/2)].A      #Пусть мамами у нас будут последние 5 индивидов нашей популяции (т.к. они у нас в последствии всегда будут отранжированы (наши популяции), беря последние 5, мы тем самым берём лучших представителей и с ними работаем. Чего с посредственностей-то взять, ну.
            self.Father.A=self.population[tt].A                           #А папами пусть будет first 5 индивидов нашей популяции 
        
            tt=tt+1    # Двигаем наш счётчик ручками.
            ran=random.random()

            for n in range(self.length):
                if random.random()>0.5:
                    self.Son1.A[n] = self.Father.A[n]
                    self.Son2.A[self.length-1-n] = self.Father.A[n]
                    self.Son3.A[n] = self.Mother.A[n]
                    self.Son4.A[self.length-1-n] = self.Mother.A[n]
                else:
                    self.Son1.A[n] = self.Mother.A[n]
                    self.Son2.A[self.length-1-n] = self.Mother.A[n]
                    self.Son3.A[n] = self.Father.A[n]
                    self.Son4.A[self.length-1-n] = self.Father.A[n]

            self.ParAndSons[self.pop_num+2*s].A = self.Son1.A.copy()
            self.ParAndSons[self.pop_num+2*s+1].A = self.Son2.A.copy()
            self.ParAndSons[self.pop_num+2*s+2].A = self.Son3.A.copy()
            self.ParAndSons[self.pop_num+2*s+3].A = self.Son4.A.copy()

    # def mutation(self):
    #     """"""

    #     for r in range(self.pop_num*3, 5):                # Это мутации. Чтобы доказать крутость нашего скрещивания мы минимизируем мутации.
    #         for w in range(0,self.length,2):              # Т.к. при большой вероятности мутации верное решение находится даже при совершенно неработающем механизме скрещивания.
    #             if random.random()<0.25:                  #Поэтому мы мутируем только одного (17-го) индивида. Т.е. мы с вероятностью 0.00001
    #                 self.ParAndSons[r].A[w] = self.ParAndSons[r].A[w] + 2  # Смещаем на 2 пикселя.
    #             elif random.random()>0.25 and random.random()<0.5:
    #                 self.ParAndSons[r].A[w] = self.ParAndSons[r].A[w] - 2
    #         for w in range(1,self.length,2):   
    #             if random.random()>0.5 and random.random()<0.75:   
    #                 self.ParAndSons[r].A[w] = self.ParAndSons[r].A[w] + 2
    #             elif random.random()>0.75 and random.random()<1:
    #                 self.ParAndSons[r].A[w] = self.ParAndSons[r].A[w] - 2    

    def mutation(self):
        """"""

        for r in range(self.pop_num*3, 5):                # Это мутации. Чтобы доказать крутость нашего скрещивания мы минимизируем мутации.
            for w in range(0,self.length):              # Т.к. при большой вероятности мутации верное решение находится даже при совершенно неработающем механизме скрещивания.
                if random.random()<0.2:                  #Поэтому мы мутируем только одного (17-го) индивида. Т.е. мы с вероятностью 0.00001
                    self.ParAndSons[r].A[w] = self.ParAndSons[r].A[w] + np.random.randint(-20, 20)  # Смещаем на 2 пикселя.
 


    def selection(self):
        """"""

        for i in range(self.pop_num*3):                     #Это важно. Далее мы будем ранжировать массив отцов и детей в порядке возрастания живучести (суммы (fit)).
            self.ParAndSons[i].fit = fitness(self.gray, self.deltaX, self.length, self.ParAndSons[i].A)

        #  Сортировка.
        self.ParAndSons = sorted(self.ParAndSons, key=lambda individ: individ.fit)   
        self.population=self.ParAndSons[:self.pop_num].copy()


    def calc(self):
        """"""

        self.cross()
        self.mutation()
        self.selection()
        
        return  self.population[0]
        

    

    


class Individ:
    """
    """
    
    def __init__(self, y1, y2, length):   
        self.length = length   
        self.A=np.random.randint(y1, y2, self.length)    #Объявляем атрибут "А" нашего индивида (это будет сама строка 010..101)
        self.fit=0                          #Объявляем атрибут "живучести" индивида (это будет сумма элементов нашей строки 010..101) (пока присвоим ей значение 0)
    
    
    



def fitness(image, deltaX, length, individ):                      #Эта функция нашего индивида как раз отвечает за подсчёт "живучести" (считает сумму)
    """"""
    
    summa = 0
    sum_vrt = 0
    for i in range(length):                 #Цикл в 30 итераций (i принимает значения от 0 до 29)
        sum_ = np.sum(image[individ[i], i*deltaX:i*deltaX+deltaX])
        if i>0:
            if individ[i]>individ[i-1]:
                sum_vrt = np.sum(image[individ[i-1]:individ[i], i*deltaX])
            else:
                sum_vrt = np.sum(image[individ[i]:individ[i-1], i*deltaX])
        summa=summa + sum_ + sum_vrt       #Сумма вбирает поочерёдно в себя все элементы строки (A[0], A[1], ... A[29])
    return summa


def find_peaks_(image):
    """"""

    height, width = image.shape[:2]
    img_matrix = [sum(i)/len(i) for i in image]
    x=[i for i in range(height)]
    y = [255-i for i in img_matrix]
    y = gaussian_filter(y, sigma=20)
    maxs, _ = find_peaks(y)
    maxs = maxs.tolist()

    return maxs

def run(gaObj, peaks, epoch):
    """"""

    gen_lines = []
    
    for line in range(len(peaks)-1):
        gaObj.createPopulation(peaks[line], peaks[line+1])
        epoch_line = []
        for p in range(epoch):  
            st_time = time.time()                  #Это наш основной цикл. Сейчас стоит 60 итераций. Т.е. мы ставим ограничение в 60 поколений.
            gen_line = gaObj.calc()
            # For draw results each epoch.
            epoch_line.append(gen_line.A)
            print(f'Line = {line}, Epoch = {p}, fit = {gen_line.fit}, Time = {time.time()-st_time}') 
        
        gen_lines.append(epoch_line)  
    return np.moveaxis(np.array(gen_lines), 0, 1)  # Swap line and epoch axes.


def drawLines(image, lines, deltaX, epoch='last', color=(0,0,255), thickness = 3, IMG_FOLDER='imgs'):
    
    image_copy = image.copy()
    for j in lines:
        for i in range(len(j)):
            x1 = i*deltaX
            x2 = i*deltaX+deltaX
            y1 = j[i]
            y2 = j[i]
            start_point = (x1, y1)

            if i>0:
                cv2.line(image_copy, preview_point, start_point, color, thickness)
            end_point = (x2, y2)

            cv2.line(image_copy, start_point, end_point, color, thickness)
            preview_point = end_point

    cv2.imwrite(f"{IMG_FOLDER}/gen_line{epoch}.jpg", image_copy)



if __name__ == '__main__':

    # HYPER PARAMETERS FOR GENETIC ALGHORITM.
    POP_NUM=200
    DELTAX=50 # VALUE OF H.
    EPOCH=500
    IMAGE_PATH = '7.jpg'

    image = cv2.imread(IMAGE_PATH)
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    peaks = find_peaks_(gray)[:2]
    length_ = int(width/DELTAX)
    ssga = SimpleSegmentationGA(POP_NUM, length_, DELTAX, EPOCH, gray)
    start_time = time.time()
    lines = run(ssga, peaks, EPOCH)
    print('Time run=', time.time()-start_time)
    drawLines(image, lines[-1], DELTAX)




    









