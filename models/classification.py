import torch
import torch.nn as nn
from torchvision import models

class LandUseClassifier(nn.Module):
    def __init__(self, n_classes=5):
        super().__init__()
        # Using a pre-trained ResNet as a backbone
        self.backbone = models.resnet50(pretrained=True)
        num_ftrs = self.backbone.fc.in_features
        self.backbone.fc = nn.Linear(num_ftrs, n_classes)
        
    def forward(self, x):
        return self.backbone(x)

def get_classifier(n_classes=5):
    return LandUseClassifier(n_classes)

if __name__ == "__main__":
    model = get_classifier()
    x = torch.randn(1, 3, 224, 224)
    logits = model(x)
    print(f"Classification output shape: {logits.shape}")
