import numpy as np
import torch
from models.segmentation import get_model

def calculate_nbr(nir_band, swir_band):
    """
    Normalized Burn Ratio.
    NIR: Near Infrared
    SWIR: Shortwave Infrared
    """
    nbr = (nir_band - swir_band) / (nir_band + swir_band + 1e-10)
    return nbr

class FireDetector:
    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = get_model(n_channels=3, n_classes=1).to(self.device) # 1 class for Fire/Burn
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def detect(self, image_tensor):
        """
        Deep learning based fire/smoke detection.
        """
        with torch.no_grad():
            output = self.model(image_tensor.to(self.device))
            mask = torch.sigmoid(output) > 0.5
        return mask.cpu().numpy()

    def detect_burn_scars(self, nir, swir, threshold=-0.1):
        """
        Detect burn scars using NBR.
        """
        nbr = calculate_nbr(nir, swir)
        # Low NBR values indicate burned areas
        burn_mask = nbr < threshold
        return burn_mask

if __name__ == "__main__":
    pass
