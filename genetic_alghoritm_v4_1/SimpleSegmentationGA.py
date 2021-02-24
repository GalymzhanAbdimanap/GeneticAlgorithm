import numpy as np
import random, time
import cv2
from GeneticAlghoritm import GeneticAlghoritm
from Individ import Individ
from utils import * 




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