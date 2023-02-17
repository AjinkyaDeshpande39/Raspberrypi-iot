#  TCGA dataset
import torch
import torch.nn as nn
import numpy as np
import torchvision
from torchvision import models
from torchvision.transforms import transforms


import os
import shutil
from PIL import Image
import random
import matplotlib.pyplot as plt

from ModelFileEfficientNetb0 import getModel
torch.manual_seed(0)
torch.cuda.manual_seed(0)
# %matplotlib inline
random.seed(0)

import cv2

def predictType(img_path, labels):
    labels = torch.tensor([labels])
    transform_test = transforms.Compose([transforms.ToTensor(),
                                transforms.Resize([224,224]),
                                ])
    img = Image.open(img_path)
    img = img.convert("RGB")
    img = transform_test(img)
    img = torch.unsqueeze(img, 0)
    
    Model = getModel()
    model_path = "/home/pi/Ajinkya/EfficientNetB0 no augmentationFold4.pth"
    Model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))
    criterion = nn.CrossEntropyLoss()
    Model.eval()
    with torch.no_grad():
        # calculate outputs by running images through the network
        outputs = Model(img)
        loss = criterion(outputs, labels)
        # the class with the highest energy is what we choose as prediction
        _, predicted = torch.max(outputs.data, 1)
        outputs = nn.functional.softmax(outputs, dim=-1)

    Model.train()
    cancerType = torch.argmax(outputs[0]).item()
    return(cancerType, outputs, loss.item())

if __name__=="__main__":
    img_path = "/home/pi/Ajinkya/Grade2.png"
    cancerType, outputs, loss = predictType(img_path,torch.tensor([2]))
    print("Predicted type =",cancerType, " Probabilities=",outputs, " loss=",loss)

