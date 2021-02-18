import numpy as np
import random
import cv2 

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
        self.fit=0                          #Объявляем атрибут "живучести" индивида (это будет сумма элементов нашей строки 010..101) (пока присвоим ей значение 0)
 
    def fitness(self):                      #Эта функция нашего индивида как раз отвечает за подсчёт "живучести" (считает сумму)
        summa=0
        for i in range(Line.length):                 #Цикл в 30 итераций (i принимает значения от 0 до 29)
            sum_ = np.sum(Line.image[self.A[i], i*Line.deltaX:i*Line.deltaX+Line.deltaX])
            # cv2.line(image, ())
            
            summa=summa+sum_           #Сумма вбирает поочерёдно в себя все элементы строки (A[0], A[1], ... A[29])
            
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
    def info(self):                    #Функция вывода популяции на экран.
        for i in range(Line.pop_num):            #Выводим все 10 строк (все 10 индивидов популяции)
            # for j in range(Line.length):        #Выводим поочерёдно каждый элемент строки "А" нашего индивида.
            #     print(self.B[i].A[j], end ="") # i-й элемент массива индивидов "В". И j-й элемент строки "A" этого самого i-го индивида.
            # print("=",end="")          #Важно понять структуру "self.B[i].A[j]". Мы тут залезаем внутрь одного массива в гости к другим массивам. self - вместо него будет имя нашей популяции "pop1". У популяции есть атрибут "B" - массив индивидов. i-й элемент этого массива (B[i]), являясь индивидом, будет иметь все атрибуты класса "индивид", а именно массив из 30 нулей и единиц ("А"). И доступ от атрибута одного класса к атрибуту "внутреннего" класса осуществляется через точку "."
            self.B[i].fitness()        #Вникаем в значение точек. self(имя экземпляра класса (pop1) ТОЧКА B[i] (i-й индивид популяции) ТОЧКА fitness() (функция считающая сумму и кидающая значение этой суммы в переменную self.fit)
            print(self.B[i].fit)       #Принтим значение fit i-го индивида популяции.



    


def geneticAlghoritm(y1, y2, image, pop_num=10, deltaX=20, epoch=500):
    """
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = 255 - gray
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
    ParAndSons = []
    
    for j in range(Line.pop_num*2):                    #Тут мы "придаём форму" нашему массиву "Родителей и детей". Инициализируем его рандомными индивидами.
        ParAndSons.append(Individ())       #Чтобы в дальнейшем иметь возможность напрямую работать с этим массивом с помощью наших атрибутов (А, fit)
                                        #Рандомные значения, которыми мы забили этот массив, нам не помешают. Т.к. мы поэлементно все элементы этого массива забьём актуальными данными вручную по ходу программы.
    
    print("\n")                            #Отступаем две строчки после вывода нашей стартовой популяции. И да начнётся.. ЕСТЕСТВЕННЫЙ ОТБОР!!!11
    
    for p in range(epoch):                    #Это наш основной цикл. Сейчас стоит 60 итераций. Т.е. мы ставим ограничение в 60 поколений.
                                        #За них мы должны успеть вырастить целое поколение мутантов-переростков. Мы всегда можем увеличить количество поколений и увеличить вероятность нахождения ответа. Или уменьшить, если наш механизм скрещиваний очень крутой, и мы очень быстро (за 20-30 поколений) находим ответ.
        for i in range(Line.pop_num):                #Заносим в первые 10 элементов массива "Отцы и дети" всю нашу входную популяцию.
            for j in range(Line.length):
                ParAndSons[i].A[j]=pop1.B[i].A[j]
    
        tt=0                                       #Счётчик, который нужён для реализации небанального скрещивания.
        for s in range(0,Line.pop_num,2):                    #Цикл. От 0 до 10 с шагом 2. Т.е. тут мы берём 5 пар родителей.
            for j in range(Line.length):                    #Как ты заметил, цикл из 30 итераций есть практически везде. Т.к. все операции мы проводим поэлементно (большая честь каждому нолику и каждой единичке).
                Mother.A[j]=pop1.B[tt+int(Line.pop_num/2)].A[j]      #Пусть мамами у нас будут последние 5 индивидов нашей популяции (т.к. они у нас в последствии всегда будут отранжированы (наши популяции), беря последние 5, мы тем самым берём лучших представителей и с ними работаем. Чего с посредственностей-то взять, ну.
                Father.A[j]=pop1.B[random.randint(0,Line.pop_num-1)].A[j] #А папами пусть будет любой случайный индивид из нашей популяции. (использовали рандом от 0 до 9). Кстати, если делать совсем по-умному, то надо и папу и маму выбирать случайным образом. Но вероятность выбора в качестве родителя у индивида должна быть тем выше, чем выше у него живучесть (fit). Предлагаю (после того как со всем остальным хорошенько разберёшься) тебе подумать о том, как это можно сделать. Ничего особенно сложного в этом и нет на самом деле.
    
            tt=tt+1    # Двигаем наш счётчик ручками.
    
            ran=random.random()
    
            if (ran>0.8):                          #А это наши механизмы скрещивания.
                for n in range(int(Line.length/6)):                 #Берём первые 5 элементов у папы и у мамы (для сына1 и сына2 соответственно).
                    Son1.A[n]=Father.A[n]
                    Son2.A[n]=Mother.A[n]
    
                for n in range(int(Line.length/6),Line.length):              #И берём остальные 25 элементов у мамы и у папы для сына1 и сына2 соответственно (крест-накрест)
    
                    Son1.A[n]=Mother.A[n]
                    Son2.A[n]=Father.A[n]
    
            if ((ran>0.6) & (ran <=0.8)):          #Тот же самый крест-накрест, только теперь самого тривиального вида.
                for n in range(int(Line.length/2)):                #Первые 15 у папы и вторые 15 у мамы для сына1.
                    Son1.A[n]=Father.A[n]          #И первые 15 у мамы и вторые 15 у папы для сына2.
                    Son2.A[n]=Mother.A[n]
                for n in range(int(Line.length/2)+1,Line.length):
                    Son1.A[n]=Mother.A[n]
                    Son2.A[n]=Father.A[n]
    
            if ((ran <0.6) & (ran >=0.4)):         #Крест накрест. Зеркален первому методу скрещивания. (только не первые 5 элементов берём, а последние)
                for n in range(int(Line.length*5/6)):
                    Son1.A[n]=Father.A[n]
                    Son2.A[n]=Mother.A[n]
                for n in range(int(Line.length*5/6),Line.length):
                    Son1.A[n] = Mother.A[n]
                    Son2.A[n] = Father.A[n]
    
            if ((ran <0.4) & (ran>=0.3)):          #Срединный крест-накрест + инверсия.
                for n in range(int(Line.length/2)):
                    Son1.A[n]=Father.A[int(Line.length/2)-1-n]
                    Son2.A[n]=Mother.A[int(Line.length/2)-1-n]
                for n in range(int(Line.length/2),Line.length):
                    Son1.A[n]=Mother.A[Line.length+int(Line.length/2)-1-n]
                    Son2.A[n]=Father.A[Line.length+int(Line.length/2)-1-n]
    
            if (ran<0.3):                          #Тут берём для сына1 первые 15 элементов папы + первые 15 элементов мамы.
                for n in range(int(Line.length/2)):                #А для сына2 берём вторые 15 элементов мамы + вторые 15 элементов папы.
                    Son1.A[n]=Father.A[n]
                    Son1.A[n+int(Line.length/2)]=Mother.A[n]
                    Son2.A[n]=Mother.A[n+int(Line.length/2)]
                    Son2.A[n+int(Line.length/2)]=Father.A[n+int(Line.length/2)]
    
            for i in range(Line.length):                    #Тут мы закидываем наших получившихся в результате скрещивания s-той пары родителей Сына1 и Сына2 во вторую половину массива "Отцы и дети".
                ParAndSons[Line.pop_num+s].A[i]=Son1.A[i]
                ParAndSons[Line.pop_num+1+s].A[i]=Son2.A[i]
    
        # for r in range(17,18):                #Это мутации. Чтобы доказать крутость нашего скрещивания мы минимизируем мутации.
        #     for w in range(30):               #Т.к. при большой вероятности мутации верное решение находится даже при совершенно неработающем механизме скрещивания.
        #         if random.random()<0.1:   #Поэтому мы мутируем только одного (17-го) индивида. Т.е. мы с вероятностью 0.00001
        #             if ParAndSons[r].A[w]==1: #инвертируем каждую из его 30 нулей и единиц.
        #                 ParAndSons[r].A[w]=0  #((При решении задачи с уравнением будем мутировать 3-5 индивидов с вероятностью 0.01-0.05 примерно.))
        #             if ParAndSons[r].A[w]==0:
        #                 ParAndSons[r].A[w]=1

        for r in range(Line.pop_num*2, 5):                
            for w in range(0,Line.length,2):   
                if random.random()<0.1:   
                    ParAndSons[r].A[w] = ParAndSons[r].A[w] + 20
                elif random.random()>0.2 and random.random()<0.4:
                    ParAndSons[r].A[w] = ParAndSons[r].A[w] - 20
                    # ParAndSons[r].A[w]=random.randint(Line.y1, Line.y2)  
                    

    
        for i in range(Line.pop_num*2):                     #Это важно. Далее мы будем ранжировать массив отцов и детей в порядке возрастания живучести (суммы (fit)).
            ParAndSons[i].fitness()             #Поэтому мы сначала должны посчитать для всех 20 индивидов в этом массиве это самое fit с помощью нашей клёвой функции fitness().
    
        for m in range(len(ParAndSons)-1,0,-1):             #Ранжирование (методом пузырька). Лёгкие всплывают наверх, а тяжёлые оказываются внизу. (вместо "len(ParAndSons)-1" можно просто написать 19, т.к. мы знаем длину нашего массива.) Напомню, что Range(19,0,-1)  означает, что мы в цикле идём от 19 до 0 с шагом "-1".
            for b in range(m):                              #Тут мы идём в цикле от 0 до "m" (а это счётчик предыдущего цикла). Т.е. каждая итерация внешнего цикла будет уменьшать и длину внутреннего цикла.
                if ParAndSons[b].fit > ParAndSons[b+1].fit: #Разобраться с методом пузырька проще всего нарисовав на бумаге ряд 31597 и проделать на нём письменно весь алгоритм, который выдаст гугл по запросу "ранжирование пузырьком".
                    mem = ParAndSons[b]                     #Мы используем переменную "mem" (от слова memory) чтобы хранить в ней одно значение в момент, когда мы взаимно меняем местами два элемента массива.
                    ParAndSons[b] = ParAndSons[b+1]
                    ParAndSons[b+1] = mem
    
        for i in range(Line.pop_num):                             #Это финал нашего основного цикла.
            for j in range(Line.length):                         #Тут мы перебрасываем лучших из массива "отцов и детей" (т.е. последние 10 индивидов)
                pop1.B[i].A[j]=ParAndSons[i].A[j]    #в массив нашей основной рабочей популяции pop1.
    
        pop1.info()                                     #Выводим нашу новую популяцию на экран.
                                                         #Отступаем строчку. И повторяем наш цикл ещё 59 раз. Итого мы выведем 60 популяций, причём каждая последующая будет лучше предыдущей.
    # print(pop1.B[0].A, pop1.B[0].fit)
    return  pop1.B[0]



doc = [213,  569,  856, 1004, 1155, 1301, 1454, 1603, 1756, 1905, 2054, 2205, 2354, 2505, 2655, 2806, 2955, 3106, 3256]


# HYPER PARAMETERS FOR GENETIC ALGHORITM.
POP_NUM=100
DELTAX=75 # VALUE OF H.
EPOCH=50 

image = cv2.imread('7.jpg')
for line in range(len(doc)-1):
    gen_line = geneticAlghoritm(y1=doc[line], y2=doc[line+1], image=image, pop_num=POP_NUM, deltaX=DELTAX, epoch=EPOCH)
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


cv2.imwrite("gen_line.jpg", image)


