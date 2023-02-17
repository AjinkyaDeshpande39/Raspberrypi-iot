import torch.nn as nn
from torchvision import models
class Classifier(nn.Module):
    def __init__(self, effnetb0):
        super().__init__()
        self.effnetb0 = effnetb0
        self.fc_in_features = 1280
        self.effnetb0.classifier = nn.Linear(self.fc_in_features, 3)

    def forward(self,x):
        x = self.effnetb0(x)
        return(x)
def getModel():
    model = models.efficientnet_b0(pretrained=True)
    device = "cpu"
    for param in model.parameters():
        param.requires_grad = False

    Model = Classifier(model)
    Model.to(device)

    return(Model)

