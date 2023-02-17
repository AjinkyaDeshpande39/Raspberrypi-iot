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
from glob import glob

from PIL import Image, ImageTk
from time import time
from classification import *


dir_path = "/home/pi/Ajinkya"

b = sorted(glob("{}/*png".format(dir_path)))
t = 0
for idx,img_path in enumerate(b):
    t1 = time()
    label = img_path.split("/")[-1].split(".")[0][-3]
    cancerType, outputs, loss = predictType(img_path,int(label))
    t2 = time()
    t += t2-t1
    print(img_path, cancerType)

idx+=1
print("average inference time = {0:.3f} sec".format(t/idx))
