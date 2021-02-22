import numpy as np
import random, time
import cv2 
import pymp 
from matplotlib import pyplot as plt 
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks

class Line:
    """
    """
    
    def __init__(self, image, pop_num, deltaX, epoch):
        self.image = image
        self.pop_num = pop_num
        self.deltaX =  deltaX # value of h
        self.epoch = epoch

    def find_peaks(self):
    
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        height, width = self.image.shape[:2]
        img_matrix = [sum(i)/len(i) for i in gray]
   
        x=[i for i in range(height)]
        y = [255-i for i in img_matrix]
        y = gaussian_filter(y, sigma=20)

        maxs, _ = find_peaks(y)
        maxs = maxs.tolist()

        return maxs
    
    def drawLine(self, lines, epoch, color=(0,0,255), thickness = 3, IMG_FOLDER='imgs'):
        image_copy = self.image.copy()
        for j in lines:
            for i in range(len(j)):
                x1 = i*self.deltaX
                x2 = i*self.deltaX+self.deltaX
                y1 = j[i]
                y2 = j[i]
                start_point = (x1, y1)

                if i>0:
                    cv2.line(image_copy, preview_point, start_point, color, thickness)
                end_point = (x2, y2)

                cv2.line(image_copy, start_point, end_point, color, thickness)
                preview_point = end_point

        cv2.imwrite(f"{IMG_FOLDER}/gen_line{epoch}.jpg", image_copy)


    def drawLineEachEpoch(gen_line, p, color=(0,0,255), thickness = 3, IMG_FOLDER='imgs'):

        for i in range(len(gen_line.A)):
            x1 = i*self.deltaX
            x2 = i*self.deltaX+self.deltaX
            y1 = gen_line.A[i]
            y2 = gen_line.A[i]
            start_point = (x1, y1)

            if i>0:
                cv2.line(self.image, preview_point, start_point, color, thickness)

            end_point = (x2, y2)
            cv2.line(self.image, start_point, end_point, color, thickness)
            preview_point = end_point
        cv2.imwrite(f"{IMG_FOLDER}/gen_line_epoch_{p}.jpg", image)

    
    def geneticAlghoritm(self, y1, y2):
        """
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        gray = 256 - gray
        # Static Line params initialization. 
        
        height, width = self.image.shape[:2]
        length = int(width/self.deltaX)
        assert(length>5)

        population = []                    #Объявляем массив "В", в котором будем хранить популяцию из 10 индивидов.
        for i in range(self.pop_num):            #Цикл
            c=Individ(y1, y2, length)                #В переменную "с" запихнулся (срандомился) новёхонький уникальненький индивид. (на каждой итерации цикла новый)
            population.append(c)           #А тут мы добавляем i-го уникального индивида к массиву (заполняем нашу популяцию)                      #Создаём экземпляр класса. Т.е. создаём нашу популяцию из 10 рандомных индивидов
                        
        
        Mother = Individ(y1, y2, length)                     #Инициализируем переменные, с которыми будем работать: маму, папу, 4 сыночков..
        Father = Individ(y1, y2, length)                     
        Son1 = Individ(y1, y2, length)                       
        Son2 = Individ(y1, y2, length)
        Son3 = Individ(y1, y2, length)
        Son4 = Individ(y1, y2, length)
        ParAndSons = []                        #..и массив индивидов "Родители+Дети" в котором будем хранить
        
        for j in range(self.pop_num*3):                    #Тут мы "придаём форму" нашему массиву "Родителей и детей". Инициализируем его рандомными индивидами.
            ParAndSons.append(Individ(y1, y2, length))       #Чтобы в дальнейшем иметь возможность напрямую работать с этим массивом с помощью наших атрибутов (А, fit)
                                            #Рандомные значения, которыми мы забили этот массив, нам не помешают. Т.к. мы поэлементно все элементы этого массива забьём актуальными данными вручную по ходу программы.
        draw_list = []
        for p in range(self.epoch):                    #Это наш основной цикл. Сейчас стоит 60 итераций. Т.е. мы ставим ограничение в 60 поколений.
            est_time = time.time()                              #За них мы должны успеть вырастить целое поколение мутантов-переростков. Мы всегда можем увеличить количество поколений и увеличить вероятность нахождения ответа. Или уменьшить, если наш механизм скрещиваний очень крутой, и мы очень быстро (за 20-30 поколений) находим ответ.
            for i in range(self.pop_num):                #Заносим в первые 10 элементов массива "Отцы и дети" всю нашу входную популяцию.
                ParAndSons[i].A=population[i].A.copy()

            random.shuffle(population) # 
            tt=0                                       #Счётчик, который нужён для реализации небанального скрещивания.
            for s in range(0,self.pop_num,2):                    #Цикл. От 0 до 10 с шагом 2. Т.е. тут мы берём 5 пар родителей.
                Mother.A=population[tt+int(self.pop_num/2)].A      #Пусть мамами у нас будут последние 5 индивидов нашей популяции (т.к. они у нас в последствии всегда будут отранжированы (наши популяции), беря последние 5, мы тем самым берём лучших представителей и с ними работаем. Чего с посредственностей-то взять, ну.
                Father.A=population[tt].A                           #А папами пусть будет first 5 индивидов нашей популяции 
            
                tt=tt+1    # Двигаем наш счётчик ручками.
                ran=random.random()

                for n in range(length):
                    if random.random()>0.5:
                        Son1.A[n] = Father.A[n]
                        Son3.A[n] = Mother.A[n]
                        if n < length-1:
                            Son2.A[n] = Father.A[n+1]
                        if n > 0:
                            Son4.A[n] = Mother.A[n-1]
                    else:
                        Son1.A[n] = Mother.A[n]
                        Son3.A[n] = Father.A[n]
                        if n < length-1:
                            Son2.A[n] = Mother.A[n+1]
                        if n > 0:
                            Son4.A[n] = Father.A[n-1]


                # if (ran>0.8):                          #А это наши механизмы скрещивания.
                #     for n in range(int(length/6)):                 #Берём первые 5 элементов у папы и у мамы (для сына1 и сына2 соответственно).
                #         Son1.A[n]=Father.A[n]
                #         Son2.A[length-1-n]=Father.A[n]
                #         Son3.A[n]=Mother.A[n]
                #         Son4.A[length-1-n]=Mother.A[n]
                        
        
                #     for n in range(int(length/6),length):              #И берём остальные 25 элементов у мамы и у папы для сына1 и сына2 соответственно (крест-накрест)
                #         Son1.A[n]=Mother.A[n]
                #         Son2.A[length-1-n]=Mother.A[n]
                #         Son3.A[n]=Father.A[n]
                #         Son4.A[length-1-n]=Father.A[n]
    
                # if ((ran>0.6) & (ran <=0.8)):          #Тот же самый крест-накрест, только теперь самого тривиального вида.
                #     for n in range(int(length/2)):                #Первые 15 у папы и вторые 15 у мамы для сына1.
                #         Son1.A[n]=Father.A[n]          #И первые 15 у мамы и вторые 15 у папы для сына2.
                #         Son2.A[n]=Father.A[length-1-n]
                #         Son3.A[n]=Mother.A[n]
                #         Son4.A[n]=Mother.A[length-1-n]
                #     for n in range(int(length/2)+1,length):
                #         Son1.A[n]=Mother.A[n]
                #         Son2.A[n]=Mother.A[length-1-n]
                #         Son3.A[n]=Father.A[n]          
                #         Son4.A[n]=Father.A[length-1-n]
        
                # if ((ran <0.6) & (ran >=0.4)):         #Крест накрест. Зеркален первому методу скрещивания. (только не первые 5 элементов берём, а последние)
                #     for n in range(int(length*5/6)):
                #         Son1.A[n]=Father.A[n]
                #         Son2.A[n]=Father.A[length-1-n]
                #         Son3.A[n]=Mother.A[n]
                #         Son4.A[n]=Mother.A[length-1-n]
                #     for n in range(int(length*5/6),length):
                #         Son1.A[n]=Mother.A[n]
                #         Son2.A[n]=Mother.A[length-1-n]
                #         Son3.A[n]=Father.A[n]
                #         Son4.A[n]=Father.A[length-1-n]
        
                # if ((ran <0.4) & (ran>=0.3)):          #Срединный крест-накрест + инверсия.
                #     for n in range(int(length/2)):
                #         Son1.A[n]=Father.A[int(length/2)-1-n]
                #         Son2.A[int(length/2)+n]=Father.A[int(length/2)-1-n]
                #         Son3.A[n]=Mother.A[int(length/2)-1-n]          
                #         Son4.A[int(length/2)+n]=Mother.A[int(length/2)-1-n]
                #     for n in range(int(length/2),length):
                #         Son1.A[n]=Mother.A[length+int(length/2)-1-n]
                #         Son2.A[n-int(length/2)]=Mother.A[length+int(length/2)-1-n]
                #         Son3.A[n]=Father.A[length+int(length/2)-1-n]          
                #         Son4.A[n-int(length/2)]=Father.A[length+int(length/2)-1-n]
        
                # if (ran<0.3):                          #Тут берём для сына1 первые 15 элементов папы + первые 15 элементов мамы.
                #     for n in range(int(length/2)):                #А для сына2 берём вторые 15 элементов мамы + вторые 15 элементов папы.
                #         Son1.A[n]=Father.A[n]
                #         Son1.A[n+int(length/2)]=Mother.A[n]

                #         Son2.A[n]=Father.A[n+int(length/2)]
                #         Son2.A[n+int(length/2)]=Mother.A[n+int(length/2)]

                #         Son3.A[n]=Mother.A[n+int(length/2)]
                #         Son3.A[n+int(length/2)]=Father.A[n+int(length/2)]

                #         Son4.A[n]=Mother.A[n]
                #         Son4.A[n+int(length/2)]=Father.A[n]
                    
                ParAndSons[self.pop_num+2*s].A=Son1.A.copy()
                ParAndSons[self.pop_num+2*s+1].A=Son2.A.copy()
                ParAndSons[self.pop_num+2*s+2].A=Son3.A.copy()
                ParAndSons[self.pop_num+2*s+3].A=Son4.A.copy()
            
            
            for r in range(self.pop_num*3, 5):                # Это мутации. Чтобы доказать крутость нашего скрещивания мы минимизируем мутации.
                for w in range(0,length,2):              # Т.к. при большой вероятности мутации верное решение находится даже при совершенно неработающем механизме скрещивания.
                    if random.random()<0.25:                  #Поэтому мы мутируем только одного (17-го) индивида. Т.е. мы с вероятностью 0.00001
                        ParAndSons[r].A[w] = ParAndSons[r].A[w] + 2  # Смещаем на 2 пикселя.
                    elif random.random()>0.25 and random.random()<0.5:
                        ParAndSons[r].A[w] = ParAndSons[r].A[w] - 2
                for w in range(1,length,2):   
                    if random.random()>0.5 and random.random()<0.75:   
                        ParAndSons[r].A[w] = ParAndSons[r].A[w] + 2
                    elif random.random()>0.75 and random.random()<1:
                        ParAndSons[r].A[w] = ParAndSons[r].A[w] - 2

            # Parallel TRUE.
            # with pymp.Parallel(4) as p:         
            #     for i in p.range(self.pop_num*3):                     #Это важно. Далее мы будем ранжировать массив отцов и детей в порядке возрастания живучести (суммы (fit)).
            #         ParAndSons[i].fitness(gray, self.deltaX)             #Поэтому мы сначала должны посчитать для всех 20 индивидов в этом массиве это самое fit с помощью нашей клёвой функции fitness().

            # Parallel OFF.
            for i in range(self.pop_num*3):                     #Это важно. Далее мы будем ранжировать массив отцов и детей в порядке возрастания живучести (суммы (fit)).
                ParAndSons[i].fitness(gray, self.deltaX)             #Поэтому мы сначала должны посчитать для всех 20 индивидов в этом массиве это самое fit с помощью нашей клёвой функции fitness().

            #  Сортировка.
            ParAndSons = sorted(ParAndSons, key=lambda individ: individ.fit)   

            population=ParAndSons[:self.pop_num].copy()

            # For draw results first 10 epoch for one line.
            if p%10==0:
                draw_list.append(population[0].A)
            #     copy_image = image.copy()
            #     self.drawLineEachEpoch(copy_image, population[0], p)
                  
                  
            
            #pop1.info(p)
            
        return  population[0], draw_list


        
       
 
class Individ():
    """
    """
    
    def __init__(self, y1, y2, length):   
        self.length = length   
        self.A=np.random.randint(y1, y2, length)    #Объявляем атрибут "А" нашего индивида (это будет сама строка 010..101)
        self.fit=0                          #Объявляем атрибут "живучести" индивида (это будет сумма элементов нашей строки 010..101) (пока присвоим ей значение 0)
    
    def fitness(self, image, deltaX):                      #Эта функция нашего индивида как раз отвечает за подсчёт "живучести" (считает сумму)
        summa = 0
        sum_vrt = 0
        for i in range(self.length):                 #Цикл в 30 итераций (i принимает значения от 0 до 29)
            sum_ = np.sum(image[self.A[i], i*deltaX:i*deltaX+deltaX])
            if i>0:
                if self.A[i]>self.A[i-1]:
                    sum_vrt = np.sum(image[self.A[i-1]:self.A[i], i*deltaX])
                else:
                    sum_vrt = np.sum(image[self.A[i]:self.A[i-1], i*deltaX])

            summa=summa + sum_ + sum_vrt       #Сумма вбирает поочерёдно в себя все элементы строки (A[0], A[1], ... A[29])
        
        self.fit=summa
 
#--------------------------------------------------------------------------



#--------------------------------------------------------------------------
# HYPER PARAMETERS FOR GENETIC ALGHORITM.
POP_NUM=80
DELTAX=20 # VALUE OF H.
EPOCH=100
IMAGE_PATH = '7.jpg'



est_time = time.time()
image = cv2.imread(IMAGE_PATH)
lineObj = Line(image, POP_NUM, DELTAX, EPOCH)
doc = lineObj.find_peaks()
gen_line_list = pymp.shared.list()
draw_list_lines = pymp.shared.list()
with pymp.Parallel(4) as p:
    for line in p.range(len(doc)-1):
        # st_time = time.time()
        gen_line, draw_list = lineObj.geneticAlghoritm(y1=doc[line], y2=doc[line+1])
        # print("function time=", time.time()-st_time)
        gen_line_list.append(gen_line.A)
        draw_list_lines.append(draw_list)
        
lineObj.drawLine(gen_line_list, EPOCH+1)

for i in range(int(EPOCH/10)):

    lineObj.drawLine(np.array(draw_list_lines)[:,i], i*10)


print("Time: ", time.time()-est_time)
