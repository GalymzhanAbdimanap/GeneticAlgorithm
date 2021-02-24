from abc import abstractmethod, abstractproperty


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