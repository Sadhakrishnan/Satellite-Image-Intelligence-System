import numpy as np
import torch
from models.segmentation import get_model

def calculate_ndwi(green_band, nir_band):
    """
    Normalized Difference Water Index.
    Green: typically band 3 for Sentinel-2, band 3 for Landsat 8.
    NIR: typically band 8 for Sentinel-2, band 5 for Landsat 8.
    """
    ndwi = (green_band - nir_band) / (green_band + nir_band + 1e-10)
    return ndwi

class FloodDetector:
    def __init__(self, model_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = get_model(n_channels=3, n_classes=1).to(self.device)
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()

    def detect(self, image_tensor):
        """
        Detect floods using deep learning model.
        """
        with torch.no_grad():
            output = self.model(image_tensor.to(self.device))
            mask = torch.sigmoid(output) > 0.5
        return mask.cpu().numpy()

    def detect_ndwi(self, green, nir, threshold=0.1):
        """
        Detect floods using NDWI.
        """
        ndwi = calculate_ndwi(green, nir)
        flood_mask = ndwi > threshold
        return flood_mask

if __name__ == "__main__":
    # Example usage
    pass
