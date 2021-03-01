from abc import abstractmethod, abstractproperty


class GeneticAlgorithm():
    """Genetic Algorithm Interface."""

    @abstractmethod
    def create_population(self):
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