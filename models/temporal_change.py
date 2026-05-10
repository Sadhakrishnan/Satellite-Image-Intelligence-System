import torch
import torch.nn as nn
from .segmentation import UNet

class SiameseUNet(nn.Module):
    """
    Siamese Network for change detection using two images from different time periods.
    """
    def __init__(self, n_channels, n_classes):
        super().__init__()
        self.encoder = UNet(n_channels, n_classes) # Shared encoder
        # Simple change detection head
        self.change_head = nn.Sequential(
            nn.Conv2d(n_classes * 2, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(64, 1, kernel_size=1),
            nn.Sigmoid()
        )

    def forward(self, img1, img2):
        feat1 = self.encoder(img1)
        feat2 = self.encoder(img2)
        
        # Concatenate features
        combined = torch.cat([feat1, feat2], dim=1)
        change_mask = self.change_head(combined)
        return change_mask

def detect_change_simple(img1, img2, threshold=0.1):
    """
    Pixel-level difference thresholding.
    """
    diff = torch.abs(img1 - img2)
    change_mask = (torch.mean(diff, dim=1, keepdim=True) > threshold).float()
    return change_mask

if __name__ == "__main__":
    # Test simple change
    x1 = torch.randn(1, 3, 512, 512)
    x2 = torch.randn(1, 3, 512, 512)
    mask = detect_change_simple(x1, x2)
    print(f"Simple change mask shape: {mask.shape}")
    
    # Test Siamese
    model = SiameseUNet(3, 16)
    mask = model(x1, x2)
    print(f"Siamese change mask shape: {mask.shape}")
