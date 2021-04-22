import csv

class Repository:

    def __init__(self):
        self.__labelled_points = []
        self.__unlabelled_points = []
        self.readTheDataset('dataset.csv')
        print("Labelled dataset:")
        print(self.__labelled_points)
        print("Unlabelled dataset:")
        print(self.__unlabelled_points)


    def readTheDataset(self, filename): 
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.__labelled_points.append(row)
                self.__unlabelled_points.append([row[1], row[2]])
        

    def getTheLabelledPoints(self):
        return self.__labelled_points


    def getTheUnlabelledPoints(self):
        return self.__unlabelled_points