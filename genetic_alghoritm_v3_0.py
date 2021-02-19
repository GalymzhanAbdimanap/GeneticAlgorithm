import numpy as np
import random, time
import cv2 
import pymp

class Line:
    """
    """
    y1 = None
    y2 = None
    image = None
    length = None
    pop_num = None
    deltaX = None # value of h
       
 
class Individ(Line):
    """
    """
    
    def __init__(self):      
        self.A=np.random.randint(Line.y1, Line.y2, Line.length)    #Объявляем атрибут "А" нашего индивида (это будет сама строка 010..101)
        self.fit_vrt=0
        self.fit=0                          #Объявляем атрибут "живучести" индивида (это будет сумма элементов нашей строки 010..101) (пока присвоим ей значение 0)
    
    def fitness(self):                      #Эта функция нашего индивида как раз отвечает за подсчёт "живучести" (считает сумму)
        summa = 0
        sum_vrt = 0
        for i in range(Line.length):                 #Цикл в 30 итераций (i принимает значения от 0 до 29)
            sum_ = np.sum(Line.image[self.A[i], i*Line.deltaX:i*Line.deltaX+Line.deltaX])
            if i>0:
                if self.A[i]>self.A[i-1]:
                    sum_vrt = np.sum(Line.image[self.A[i-1]:self.A[i], i*Line.deltaX])
                else:
                    sum_vrt = np.sum(Line.image[self.A[i]:self.A[i-1], i*Line.deltaX])

            summa=summa + sum_ + sum_vrt       #Сумма вбирает поочерёдно в себя все элементы строки (A[0], A[1], ... A[29])
            

        self.fit=summa

 
    def info(self):                         #Функция вывода на экран индивида. В программе мы её не используем.
        print(self.A)                       #Осталась со времени отладки. Важно заметить, что мы тут используем
        self.fitness()                      #функцию fitness(), чтобы она подсчитала нам сумму ряда.
        print(self.fit)                     #прежде чем выводить этот самый fit на экран.
 
class Population(Line):
    """
    """

    def __init__(self):
        self.B = []                    #Объявляем массив "В", в котором будем хранить популяцию из 10 индивидов.
        for i in range(Line.pop_num):            #Цикл
            c=Individ()                #В переменную "с" запихнулся (срандомился) новёхонький уникальненький индивид. (на каждой итерации цикла новый)
            self.B.append(c)           #А тут мы добавляем i-го уникального индивида к массиву (заполняем нашу популяцию)
    def info(self, p=0):                    #Функция вывода популяции на экран.
        for i in range(Line.pop_num):            #Выводим все 10 строк (все 10 индивидов популяции)
            # for j in range(Line.length):        #Выводим поочерёдно каждый элемент строки "А" нашего индивида.
            #     print(self.B[i].A[j], end =",") # i-й элемент массива индивидов "В". И j-й элемент строки "A" этого самого i-го индивида.
            # print("=",end="")          #Важно понять структуру "self.B[i].A[j]". Мы тут залезаем внутрь одного массива в гости к другим массивам. self - вместо него будет имя нашей популяции "pop1". У популяции есть атрибут "B" - массив индивидов. i-й элемент этого массива (B[i]), являясь индивидом, будет иметь все атрибуты класса "индивид", а именно массив из 30 нулей и единиц ("А"). И доступ от атрибута одного класса к атрибуту "внутреннего" класса осуществляется через точку "."
            self.B[i].fitness()        #Вникаем в значение точек. self(имя экземпляра класса (pop1) ТОЧКА B[i] (i-й индивид популяции) ТОЧКА fitness() (функция считающая сумму и кидающая значение этой суммы в переменную self.fit)
            print("epoch=",p, " fit=",self.B[i].fit)       #Принтим значение fit i-го индивида популяции.
            #print()




#--------------------------------------------------------------------------

def drawLine(image, gen_line, p):
        color=(0,0,255)
        thickness = 3
        for i in range(len(gen_line.A)):
            x1 = i*Line.deltaX
            x2 = i*Line.deltaX+Line.deltaX
            y1 = gen_line.A[i]
            y2 = gen_line.A[i]
            start_point = (x1, y1)

            if i>0:
                cv2.line(image, preview_point, start_point, color, thickness)

            end_point = (x2, y2)

            cv2.line(image, start_point, end_point, color, thickness)
            preview_point = end_point
            


        cv2.imwrite(f"imgs/gen_line_epoch_{p}.jpg", image)

#--------------------------------------------------------------------------



def geneticAlghoritm(y1, y2, image, pop_num=10, deltaX=20, epoch=500):
    """
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = 256 - gray
    # Static Line params initialization. 
    Line.y1 = y1
    Line.y2 = y2
    Line.image = gray
    Line.pop_num = pop_num
    Line.deltaX = deltaX
    height, width = image.shape[:2]
    Line.length = int(width/Line.deltaX)
    assert(Line.length>5)

    pop1=Population()                      #Создаём экземпляр класса. Т.е. создаём нашу популяцию из 10 рандомных индивидов
    # pop1.info()                            #Выводим её на экран нашей клёвой функцией вывода.
    pop1.B[0].fitness()
    # print(pop1.B[0].A, pop1.B[0].fit)
    
    
    Mother = Individ()                     #Инициализируем переменные, с которыми будем работать: маму, папу, двух сыночков..
    Father = Individ()                     #..и массив индивидов "Родители+Дети" в котором будем хранить
    Son1 = Individ()                       #10 родителей и 10 их детишек (по два сына у каждой из пяти пар родителей).
    Son2 = Individ()
    Son3 = Individ()
    Son4 = Individ()
    ParAndSons = []
    
    for j in range(Line.pop_num*3):                    #Тут мы "придаём форму" нашему массиву "Родителей и детей". Инициализируем его рандомными индивидами.
        ParAndSons.append(Individ())       #Чтобы в дальнейшем иметь возможность напрямую работать с этим массивом с помощью наших атрибутов (А, fit)
                                        #Рандомные значения, которыми мы забили этот массив, нам не помешают. Т.к. мы поэлементно все элементы этого массива забьём актуальными данными вручную по ходу программы.
    
    print("\n")                            #Отступаем две строчки после вывода нашей стартовой популяции. И да начнётся.. ЕСТЕСТВЕННЫЙ ОТБОР!!!11
    
    for p in range(epoch):                    #Это наш основной цикл. Сейчас стоит 60 итераций. Т.е. мы ставим ограничение в 60 поколений.
        est_time = time.time()                              #За них мы должны успеть вырастить целое поколение мутантов-переростков. Мы всегда можем увеличить количество поколений и увеличить вероятность нахождения ответа. Или уменьшить, если наш механизм скрещиваний очень крутой, и мы очень быстро (за 20-30 поколений) находим ответ.
        for i in range(Line.pop_num):                #Заносим в первые 10 элементов массива "Отцы и дети" всю нашу входную популяцию.
            ParAndSons[i].A=pop1.B[i].A.copy()


        random.shuffle(pop1.B) # 
        
        tt=0                                       #Счётчик, который нужён для реализации небанального скрещивания.
        for s in range(0,Line.pop_num,2):                    #Цикл. От 0 до 10 с шагом 2. Т.е. тут мы берём 5 пар родителей.
            Mother.A=pop1.B[tt+int(Line.pop_num/2)].A      #Пусть мамами у нас будут последние 5 индивидов нашей популяции (т.к. они у нас в последствии всегда будут отранжированы (наши популяции), беря последние 5, мы тем самым берём лучших представителей и с ними работаем. Чего с посредственностей-то взять, ну.
            Father.A=pop1.B[tt].A                           #А папами пусть будет first 5 индивидов нашей популяции 
         

            tt=tt+1    # Двигаем наш счётчик ручками.
    
            ran=random.random()

            # if (ran>0.3):
            for n in range(Line.length):
                if random.random()>0.5:
                    Son1.A[n] = Father.A[n]
                    Son2.A[Line.length-1-n] = Father.A[n]
                    Son3.A[n] = Mother.A[n]
                    Son4.A[Line.length-1-n] = Mother.A[n]
                else:
                    Son1.A[n] = Mother.A[n]
                    Son2.A[Line.length-1-n] = Mother.A[n]
                    Son3.A[n] = Father.A[n]
                    Son4.A[Line.length-1-n] = Father.A[n]
            
            # if (ran>0.8):                          #А это наши механизмы скрещивания.
            #     for n in range(int(Line.length/6)):                 #Берём первые 5 элементов у папы и у мамы (для сына1 и сына2 соответственно).
            #         Son1.A[n]=Father.A[n]
            #         Son2.A[Line.length-1-n]=Father.A[n]
            #         Son3.A[n]=Mother.A[n]
            #         Son4.A[Line.length-1-n]=Mother.A[n]
                    
    
            #     for n in range(int(Line.length/6),Line.length):              #И берём остальные 25 элементов у мамы и у папы для сына1 и сына2 соответственно (крест-накрест)
            #         Son1.A[n]=Mother.A[n]
            #         Son2.A[Line.length-1-n]=Mother.A[n]
            #         Son3.A[n]=Father.A[n]
            #         Son4.A[Line.length-1-n]=Father.A[n]
    
            # if ((ran>0.6) & (ran <=0.8)):          #Тот же самый крест-накрест, только теперь самого тривиального вида.
            #     for n in range(int(Line.length/2)):                #Первые 15 у папы и вторые 15 у мамы для сына1.
            #         Son1.A[n]=Father.A[n]          #И первые 15 у мамы и вторые 15 у папы для сына2.
            #         Son2.A[n]=Father.A[Line.length-1-n]
            #         Son3.A[n]=Mother.A[n]
            #         Son4.A[n]=Mother.A[Line.length-1-n]
            #     for n in range(int(Line.length/2)+1,Line.length):
            #         Son1.A[n]=Mother.A[n]
            #         Son2.A[n]=Mother.A[Line.length-1-n]
            #         Son3.A[n]=Father.A[n]          
            #         Son4.A[n]=Father.A[Line.length-1-n]
    
            # if ((ran <0.6) & (ran >=0.4)):         #Крест накрест. Зеркален первому методу скрещивания. (только не первые 5 элементов берём, а последние)
            #     for n in range(int(Line.length*5/6)):
            #         Son1.A[n]=Father.A[n]
            #         Son2.A[n]=Father.A[Line.length-1-n]
            #         Son3.A[n]=Mother.A[n]
            #         Son4.A[n]=Mother.A[Line.length-1-n]
            #     for n in range(int(Line.length*5/6),Line.length):
            #         Son1.A[n]=Mother.A[n]
            #         Son2.A[n]=Mother.A[Line.length-1-n]
            #         Son3.A[n]=Father.A[n]
            #         Son4.A[n]=Father.A[Line.length-1-n]
    
            # if ((ran <0.4) & (ran>=0.3)):          #Срединный крест-накрест + инверсия.
            #     for n in range(int(Line.length/2)):
            #         Son1.A[n]=Father.A[int(Line.length/2)-1-n]
            #         Son2.A[int(Line.length/2)+n]=Father.A[int(Line.length/2)-1-n]
            #         Son3.A[n]=Mother.A[int(Line.length/2)-1-n]          
            #         Son4.A[int(Line.length/2)+n]=Mother.A[int(Line.length/2)-1-n]
            #     for n in range(int(Line.length/2),Line.length):
            #         Son1.A[n]=Mother.A[Line.length+int(Line.length/2)-1-n]
            #         Son2.A[n-int(Line.length/2)]=Mother.A[Line.length+int(Line.length/2)-1-n]
            #         Son3.A[n]=Father.A[Line.length+int(Line.length/2)-1-n]          
            #         Son4.A[n-int(Line.length/2)]=Father.A[Line.length+int(Line.length/2)-1-n]
    
            # if (ran<0.3):                          #Тут берём для сына1 первые 15 элементов папы + первые 15 элементов мамы.
            #     for n in range(int(Line.length/2)):                #А для сына2 берём вторые 15 элементов мамы + вторые 15 элементов папы.
            #         Son1.A[n]=Father.A[n]
            #         Son1.A[n+int(Line.length/2)]=Mother.A[n]

            #         Son2.A[n]=Father.A[n+int(Line.length/2)]
            #         Son2.A[n+int(Line.length/2)]=Mother.A[n+int(Line.length/2)]

            #         Son3.A[n]=Mother.A[n+int(Line.length/2)]
            #         Son3.A[n+int(Line.length/2)]=Father.A[n+int(Line.length/2)]

            #         Son4.A[n]=Mother.A[n]
            #         Son4.A[n+int(Line.length/2)]=Father.A[n]
                
            ParAndSons[Line.pop_num+2*s].A=Son1.A.copy()
            ParAndSons[Line.pop_num+2*s+1].A=Son2.A.copy()
            ParAndSons[Line.pop_num+2*s+2].A=Son3.A.copy()
            ParAndSons[Line.pop_num+2*s+3].A=Son4.A.copy()
        # for r in range(17,18):                #Это мутации. Чтобы доказать крутость нашего скрещивания мы минимизируем мутации.
        #     for w in range(30):               #Т.к. при большой вероятности мутации верное решение находится даже при совершенно неработающем механизме скрещивания.
        #         if random.random()<0.1:   #Поэтому мы мутируем только одного (17-го) индивида. Т.е. мы с вероятностью 0.00001
        #             if ParAndSons[r].A[w]==1: #инвертируем каждую из его 30 нулей и единиц.
        #                 ParAndSons[r].A[w]=0  #((При решении задачи с уравнением будем мутировать 3-5 индивидов с вероятностью 0.01-0.05 примерно.))
        #             if ParAndSons[r].A[w]==0:
        #                 ParAndSons[r].A[w]=1
        for r in range(Line.pop_num*3, 5):                # Это мутации. Чтобы доказать крутость нашего скрещивания мы минимизируем мутации.
            for w in range(0,Line.length,2):              # Т.к. при большой вероятности мутации верное решение находится даже при совершенно неработающем механизме скрещивания.
                if random.random()<0.25:                  #Поэтому мы мутируем только одного (17-го) индивида. Т.е. мы с вероятностью 0.00001
                    ParAndSons[r].A[w] = ParAndSons[r].A[w] + 2  # Смещаем на 2 пикселя.
                elif random.random()>0.25 and random.random()<0.5:
                    ParAndSons[r].A[w] = ParAndSons[r].A[w] - 2
            for w in range(1,Line.length,2):   
                if random.random()>0.5 and random.random()<0.75:   
                    ParAndSons[r].A[w] = ParAndSons[r].A[w] + 2
                elif random.random()>0.75 and random.random()<1:
                    ParAndSons[r].A[w] = ParAndSons[r].A[w] - 2

        with pymp.Parallel(4) as p:         
            for i in p.range(Line.pop_num*3):                     #Это важно. Далее мы будем ранжировать массив отцов и детей в порядке возрастания живучести (суммы (fit)).
                ParAndSons[i].fitness()             #Поэтому мы сначала должны посчитать для всех 20 индивидов в этом массиве это самое fit с помощью нашей клёвой функции fitness().


        # print("before sort epoch=", p)
        # for i in range(Line.pop_num*3):           
        #     for j in range(Line.length):       
        #         print(ParAndSons[i].A[j], end =",")             # i-й элемент массива индивидов "В". И j-й элемент строки "A" этого самого i-го индивида.
        #     print("=", ParAndSons[i].fit, end ="\n\n")          #Важно понять структуру "self.B[i].A[j]". Мы тут залезаем внутрь одного массива в гости к другим массивам. self - вместо него будет имя нашей популяции "pop1". У популяции есть атрибут "B" - массив индивидов. i-й элемент этого массива (B[i]), являясь индивидом, будет иметь все атрибуты класса "индивид", а именно массив из 30 нулей и единиц ("А"). И доступ от атрибута одного класса к атрибуту "внутреннего" класса осуществляется через точку "."
            
        # print('\n\n')


        # st_time = time.time()
        # for m in range(len(ParAndSons)-1,0,-1):             #Ранжирование (методом пузырька). Лёгкие всплывают наверх, а тяжёлые оказываются внизу. (вместо "len(ParAndSons)-1" можно просто написать 19, т.к. мы знаем длину нашего массива.) Напомню, что Range(19,0,-1)  означает, что мы в цикле идём от 19 до 0 с шагом "-1".
        #     for b in range(m):                              #Тут мы идём в цикле от 0 до "m" (а это счётчик предыдущего цикла). Т.е. каждая итерация внешнего цикла будет уменьшать и длину внутреннего цикла.
        #         if ParAndSons[b].fit > ParAndSons[b+1].fit: #Разобраться с методом пузырька проще всего нарисовав на бумаге ряд 31597 и проделать на нём письменно весь алгоритм, который выдаст гугл по запросу "ранжирование пузырьком".
        #             mem = ParAndSons[b]                     #Мы используем переменную "mem" (от слова memory) чтобы хранить в ней одно значение в момент, когда мы взаимно меняем местами два элемента массива.
        #             ParAndSons[b] = ParAndSons[b+1]
        #             ParAndSons[b+1] = mem
        # print('Time sort=',time.time()-st_time)

        ParAndSons = sorted(ParAndSons, key=lambda individ: individ.fit)   

        pop1.B=ParAndSons[:Line.pop_num].copy()

        # if p<11:
        #     test_image = image.copy()
        #     drawLine(test_image, pop1.B[0], p)


        #pop1.info(p)
        #print("Epoch time=", time.time()-est_time)


        
                                            #Выводим нашу новую популяцию на экран.
                                                         #Отступаем строчку. И повторяем наш цикл ещё 59 раз. Итого мы выведем 60 популяций, причём каждая последующая будет лучше предыдущей.
    
    return  pop1.B[0]



doc = [213,  569,  856, 1004, 1155, 1301, 1454, 1603, 1756, 1905, 2054, 2205, 2354, 2505, 2655, 2806, 2955, 3106, 3256]

doc = [2655, 2806]
# HYPER PARAMETERS FOR GENETIC ALGHORITM.
POP_NUM=100
DELTAX=50 # VALUE OF H.

EPOCH=100

image = cv2.imread('7.jpg')
st_time = time.time()
for line in range(len(doc)-1):
    st_time = time.time()
    gen_line = geneticAlghoritm(y1=doc[line], y2=doc[line+1], image=image, pop_num=POP_NUM, deltaX=DELTAX, epoch=EPOCH)
    print("function time=", time.time()-st_time)
    color=(0,0,255)
    thickness = 3
    for i in range(len(gen_line.A)):
        x1 = i*DELTAX
        x2 = i*DELTAX+DELTAX
        y1 = gen_line.A[i]
        y2 = gen_line.A[i]
        start_point = (x1, y1)

        if i>0:
            cv2.line(image, preview_point, start_point, color, thickness)
        end_point = (x2, y2)

        cv2.line(image, start_point, end_point, color, thickness)
        preview_point = end_point
        

    # For draw first weights.
    # thickness = 3
    # color=(255,0,0)
    # for i in range(len(pop1.B[0].A)):
    #     x1 = i*deltaX
    #     x2 = i*deltaX+deltaX
    #     y1 = pop1.B[0].A[i]
    #     y2 = pop1.B[0].A[i]
    #     start_point = (x1, y1)
    #     end_point = (x2, y2)
    #     cv2.line(image, start_point, end_point, color, thickness)

print("Time: ", time.time()-st_time)
cv2.imwrite("gen_line.jpg", image)



