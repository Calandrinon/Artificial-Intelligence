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
                    self.__maleImages.append(Image.open(self.__pathToDirectory + "/" + directory + "/" + image))
                elif directory == "Women":
                    self.__femaleImages.append(Image.open(self.__pathToDirectory + "/" + directory + "/" + image))
                else:
                    self.__thingsImages.append(Image.open(self.__pathToDirectory + "/" + directory + "/" + image))
        
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
someMen[0].show()

someWomen = imageReader.getImagesOfWomen()
someWomen[0].show()

someThings = imageReader.getImagesOfThings()
someThings[0].show()