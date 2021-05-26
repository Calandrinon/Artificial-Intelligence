import torch 
import torch.nn as nn 
import torch.optim as optim
import time
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, models, transforms
from PIL import Image
import os

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

class ImageClassifierDataset(Dataset):
    def __init__(self, image_list, image_classes):
        self.images = []
        self.labels = []
        self.classes = list(set(image_classes))
        self.class_to_label = {c: i for i, c in enumerate(self.classes)}
        self.image_size = 224
        self.transforms = transforms.Compose([
            transforms.Resize(self.image_size),
            transforms.CenterCrop(self.image_size),
            transforms.ToTensor(),
            transforms.Normalize((0.5,0.5,0.5), (0.5,0.5,0.5))
            ])

        for image, image_class in zip(image_list, image_classes):
            transformed_image = self.transforms(image)
            self.images.append(transformed_image)
            label = self.class_to_label[image_class]
            self.labels.append(label)
    
    
    def __getitem__(self, index):
        return self.images[index], self.labels[index]
        

    def __len__(self):
        return len(self.images)


class LabelledImage:
    def __init__(self, image, label):
        self.__image = image
        self.__label = label 

    
    def getImage(self):
        return self.__image 
    

    def getLabel(self):
        return self.__label 


class ImageReader:

    def __init__(self, pathToDirectory):
        self.__pathToDirectory = pathToDirectory 
        self.__maleImages = []
        self.__femaleImages = []
        self.__thingsImages = []
        self.__readImages()


    def __readImages(self):
        directories = os.listdir(self.__pathToDirectory)
        for directory in directories:
            listOfImages = os.listdir(self.__pathToDirectory + "/" + directory) 
            for image in listOfImages:
                if directory == "Men":
                    labelledImage = LabelledImage(Image.open(self.__pathToDirectory + "/" + directory + "/" + image), "man")
                    self.__maleImages.append(labelledImage)
                elif directory == "Women":
                    labelledImage = LabelledImage(Image.open(self.__pathToDirectory + "/" + directory + "/" + image), "woman")
                    self.__femaleImages.append(labelledImage)
                else:
                    labelledImage = LabelledImage(Image.open(self.__pathToDirectory + "/" + directory + "/" + image), "thing")
                    self.__thingsImages.append(labelledImage)
        
        print(" ============================================= Men ============================================= ")
        print(self.__maleImages)

        print(" ============================================= Women ============================================= ")
        print(self.__femaleImages)
        
        print(" ============================================= Things ============================================= ")
        print(self.__thingsImages)


    def getImagesOfMen(self):
        return self.__maleImages

    def getImagesOfWomen(self):
        return self.__femaleImages

    def getImagesOfThings(self):
        return self.__thingsImages


imageReader = ImageReader("FacesDataset")
someMen = imageReader.getImagesOfMen()
someMen[2].getImage().show()
print(someMen[2].getLabel())

someWomen = imageReader.getImagesOfWomen()
someWomen[-2].getImage().show()
print(someWomen[-2].getLabel())

someThings = imageReader.getImagesOfThings()
someThings[-1].getImage().show()
print(someThings[-1].getLabel())