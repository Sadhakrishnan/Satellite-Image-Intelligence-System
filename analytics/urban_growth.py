import numpy as np
import torch

class UrbanGrowthAnalyzer:
    def __init__(self):
        pass

    def analyze_growth(self, urban_mask_t1, urban_mask_t2):
        """
        Compares two urban masks to detect growth.
        urban_mask: Binary mask where 1 is urban, 0 is other.
        """
        # New urban areas: 1 in t2 but 0 in t1
        growth_mask = (urban_mask_t2 == 1) & (urban_mask_t1 == 0)
        
        area_t1 = np.sum(urban_mask_t1)
        area_t2 = np.sum(urban_mask_t2)
        growth_area = np.sum(growth_mask)
        
        growth_percent = (growth_area / (area_t1 + 1e-10)) * 100
        
        return {
            "growth_percent": float(growth_percent),
            "area_t1": int(area_t1),
            "area_t2": int(area_t2),
            "growth_area": int(growth_area),
            "growth_mask": growth_mask
        }

if __name__ == "__main__":
    # Test
    t1 = np.zeros((100, 100))
    t1[20:40, 20:40] = 1
    t2 = np.zeros((100, 100))
    t2[20:50, 20:50] = 1
    
    analyzer = UrbanGrowthAnalyzer()
    results = analyzer.analyze_growth(t1, t2)
    print(f"Urban growth: {results['growth_percent']:.2f}%")
